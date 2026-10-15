"""Source-preserving ahead-of-time Brainfuck router, NOT a host-side policy.

This build-time constructor only selects among complete annotated .bf command
streams. The actual branch selector, input consumption, and result emission are
Brainfuck operations within one generated JVM `run([B)[B` class. Each policy is
included verbatim. This is not the Android XAX caller or a hook implementation.
"""
from __future__ import annotations

import hashlib
import json
import os
import zipfile
from pathlib import Path

from .build import ROOT, FEATURES
from .core import BFError, Program, load, parse_source, program_fuel
from .host_abi import ABIError, FEATURE_IDS, Request, Reply, checked_reply, load_programs, validate_request
from .jvm import compile_class

ROUTER_NAME = 'dispatch_all'
ROUTER_CLASS = 'org/youtubehideads/bf/dispatch_all'
ROUTER_ENTRY = ROUTER_CLASS + '.class'


def selector_map() -> dict[str, int]:
    """Single-byte, stable router selectors ordered by the frozen BFH1 IDs."""
    ordered = sorted(FEATURE_IDS, key=lambda name: FEATURE_IDS[name])
    if len(ordered) >= 255 or len(set(FEATURE_IDS.values())) != len(ordered):
        raise ABIError('ROUTER_SELECTOR_IDS_INVALID')
    return {name: index + 1 for index, name in enumerate(ordered)}


def _pointer_proof(code: str) -> int:
    """A branch is safe to inline only if loops are pointer-balanced.

    All body cells are at/above the new branch's cell 3.  The graph is not
    reinterpreted or translated into host-language semantics.
    """
    offset = low = 0
    stack: list[int] = []
    for command in code:
        if command == '>':
            offset += 1
        elif command == '<':
            offset -= 1
        elif command == '[':
            stack.append(offset)
        elif command == ']':
            if not stack or stack.pop() != offset:
                raise ABIError('ROUTER_UNBALANCED_LOOP_POINTER')
        low = min(low, offset)
    if stack or low < 0:
        raise ABIError('ROUTER_BODY_POINTER_ESCAPE')
    return offset


def source_and_manifest() -> tuple[str, dict]:
    names = sorted(FEATURE_IDS, key=lambda name: FEATURE_IDS[name])
    by_name = {p.name: (p, path) for path in sorted(FEATURES.rglob('*.bf')) for p in [load(path)]}
    if set(by_name) != set(names) or len(by_name) != len(list(FEATURES.rglob('*.bf'))):
        raise ABIError('ROUTER_REGISTRY_MISMATCH')
    selectors = selector_map()
    largest_fuel = max(program_fuel(program) for program, _ in by_name.values())
    parts = [
        '# @feature dispatch_all',
        '# @purpose BF-owned selector routes a single payload to an unchanged BF policy body',
        '# @abi bf-host-v1',
        f'# @fuel {largest_fuel}',
        f'# @inputs selector byte 1..{len(names)} followed by exact selected-policy input bytes',
        '# @outputs the selected policy original action bytes, unframed',
        '# @cells cell0 selector cell1 scratch cell2 branch flag cell3+ isolated payload',
        '# @invariant all branches and source bodies execute only Brainfuck commands',
        '# @safety invalid selectors emit no bytes; the host must reject empty outputs',
        '# @section selector',
        ',',  # 1-byte selector in cell 0. Other commas come only from policy bodies.
    ]
    policies = {}
    for name in names:
        policy, path = by_name[name]
        shift = _pointer_proof(policy.code)
        selector = selectors[name]
        # Starting at cell0, duplicate immutable selector into cell1 via cell2.
        # cell1 then becomes selector-N; cell2 is 1 exactly if the difference is 0.
        # Only in that branch does execution consume payload from stdin.
        prefix = '[->+>+<<]>>[-<<+>>]<<>' + '-' * selector + '>+<[[-]>-<]>[->'
        # A branch executes once: gate 1 is cleared before body; body starts at
        # cell3, and restores the pointer to cell2 for the closing bracket.
        suffix = '<' * (shift + 1) + ']<<'
        parts.extend((f'# @section selector_{selector}_{name}', prefix,
                      f'# @note next {len(policy.code)} executable commands are an exact copy of {path.relative_to(ROOT)}',
                      policy.code, suffix))
        policies[name] = {
            'selector': selector, 'feature_id': FEATURE_IDS[name],
            'source': str(path.relative_to(ROOT)), 'source_sha256': policy.digest,
            'source_commands': len(policy.code), 'body_pointer_delta': shift,
            'fuel_limit': program_fuel(policy),
        }
    source = '\n'.join(parts) + '\n'
    router = parse_source(source)
    manifest = {
        'schema': 'brainfuck-inline-router-v1',
        'class': ROUTER_CLASS,
        'method': 'run([B)[B',
        'source_sha256': router.digest,
        'source_bytes_sha256': hashlib.sha256(source.encode('utf-8')).hexdigest(),
        'policies': policies,
        'invalid_selector': 'empty output (reject)',
        'android_runtime_tested': False,
    }
    return source, manifest


def build_router(out: Path, *, optimize: bool = False) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    source, manifest = source_and_manifest()
    program = parse_source(source)
    data = compile_class(program, ROUTER_CLASS, optimize=optimize)
    jar = out / 'brainfuck-router.jar'
    with zipfile.ZipFile(jar, 'w') as z:
        meta = zipfile.ZipInfo(ROUTER_ENTRY, (1980, 1, 1, 0, 0, 0))
        meta.compress_type = zipfile.ZIP_DEFLATED
        meta.external_attr = 0o644 << 16
        z.writestr(meta, data)
    (out / 'router.bf').write_text(source, encoding='utf-8', newline='\n')
    (out / 'router.json').write_text(json.dumps(manifest, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print(f'{len(manifest["policies"])} BF-owned branches -> {jar} sha256={hashlib.sha256(jar.read_bytes()).hexdigest()}')
    return jar


def verify_router(jar: Path, manifest_path: Path, *, optimize: bool = False) -> dict:
    actual = json.loads(manifest_path.read_text(encoding='utf-8'))
    source, expected = source_and_manifest()
    if actual != expected:
        raise ABIError('ROUTER_MANIFEST_MISMATCH')
    bf_file = manifest_path.with_name('router.bf')
    if not bf_file.is_file() or bf_file.read_bytes() != source.encode('utf-8'):
        raise ABIError('ROUTER_SOURCE_FILE_MISMATCH')
    with zipfile.ZipFile(jar) as archive:
        if archive.namelist() != [ROUTER_ENTRY]:
            raise ABIError('ROUTER_JAR_CONTENTS_INVALID')
        if archive.read(ROUTER_ENTRY) != compile_class(parse_source(source), ROUTER_CLASS, optimize=optimize):
            raise ABIError('ROUTER_CLASS_TAMPERED')
    return actual


def exercise_router_frames(frames: list[bytes], *, jar: Path, manifest: Path,
                           optimized: bool = False, active_generation: int = 1) -> list[bytes]:
    """Actually invoke the generated BF router on desktop JVM with a test-only runner."""
    import subprocess
    import tempfile
    verify_router(jar, manifest, optimize=optimized)
    programs = load_programs()
    selectors = selector_map()
    reverse = {FEATURE_IDS[name]: index for name, index in selectors.items()}
    requests = [Request.unpack(frame) for frame in frames]
    for request in requests:
        validate_request(request, programs)
        if request.generation != active_generation:
            raise ABIError('STALE_GENERATION')
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        result = subprocess.run(['javac', '-d', str(root), str(ROOT / 'tests/jvm/Runner.java')],
                                capture_output=True, text=True)
        if result.returncode:
            raise ABIError('JAVA_RUNNER_BUILD_FAILED')
        stdin = ''.join('dispatch_all ' + (bytes((reverse[r.feature_id],)) + r.data).hex() + '\n'
                        for r in requests) + 'END\n'
        result = subprocess.run(['java', '-cp', str(root) + os.pathsep + str(jar), 'Runner'],
                                input=stdin, capture_output=True, text=True)
        if result.returncode:
            raise ABIError('ROUTER_JVM_EXECUTION_FAILED')
    lines = result.stdout.splitlines()
    if len(lines) != len(requests):
        raise ABIError('ROUTER_JVM_OUTPUT_COUNT_MISMATCH')
    replies = []
    for request, line in zip(requests, lines):
        if not line.startswith('OK '):
            raise ABIError('ROUTER_JVM_POLICY_FAILED')
        try:
            raw = bytes.fromhex(line[3:])
        except ValueError as exc:
            raise ABIError('ROUTER_JVM_INVALID_HEX') from exc
        if not raw or len(raw) != (9 if raw[0] == 4 else 1):
            raise ABIError('ROUTER_JVM_INVALID_OUTPUT')
        reply = Reply(request.feature_id, request.generation, raw[0], raw[1:])
        checked_reply(request, reply, active_generation=active_generation)
        replies.append(reply.pack())
    return replies


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, default=ROOT/'generated')
    p.add_argument('--optimize', action='store_true')
    args = p.parse_args()
    build_router(args.out, optimize=args.optimize)
