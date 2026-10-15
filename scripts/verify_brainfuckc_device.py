"""Run native BF policy comparisons in Android shell, never install an app."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess

from toolchain.brainfuck.brainfuckc import validate_image
from toolchain.brainfuck.build import FEATURES, ROOT
from toolchain.brainfuck.core import interpret, load


def inputs(program):
    name = program.name
    if name == 'select_sponsor_category' or name == 'sponsor_skip_pipeline':
        for mask in range(256):
            for selected in range(8):
                categories = bytes(v for i in range(8) for v in ((mask >> i) & 1, int(i == selected)))
                if name == 'select_sponsor_category':
                    yield categories
                else:
                    yield categories + bytes((1, 1, 1, 1, 1)) + (123456789).to_bytes(8, 'little')
        if name == 'sponsor_skip_pipeline':
            for flags in itertools.product((0, 1), repeat=5):
                yield bytes((1, 1)) + bytes(14) + bytes(flags) + ((1 << 63) - 1).to_bytes(8, 'little')
    elif name == 'authorize_seek':
        for flags in itertools.product((0, 1), repeat=6):
            for end in (1, 256, 1 << 40, (1 << 63) - 1):
                yield bytes(flags) + end.to_bytes(8, 'little')
    elif name == 'sponsor_time_window':
        limit = (1 << 63) - 1
        for values in ((0, 0, 1), (5, 4, 6), (5, 5, 6), (5, 6, 6),
                       (0, 1 << 40, 1 << 42), (limit-2, limit-1, limit), (0, limit, limit)):
            yield b''.join(v.to_bytes(8, 'little') for v in values)
    else:
        count = program.metadata['inputs'].count(' (0 or 1)')
        if not count:
            raise ValueError(f'no Boolean input schema for {name}')
        yield from (bytes(bits) for bits in itertools.product((0, 1), repeat=count))


def corpus(folder: Path) -> tuple[bytes, dict]:
    manifest = json.loads((folder / 'policies.json').read_text())
    lines = []
    counts = {}
    programs = [load(path) for path in sorted(FEATURES.rglob('*.bf'))]
    if set(manifest) != {p.name for p in programs}:
        raise ValueError('native manifest policy set mismatch')
    for program in programs:
        record = manifest[program.name]
        image = (folder / (program.name + '.elf')).read_bytes()
        validate_image(image)
        if record['source_sha256'] != program.digest or record['artifact_sha256'] != hashlib.sha256(image).hexdigest():
            raise ValueError(f'native source/artifact mismatch: {program.name}')
        counts[program.name] = 0
        for data in inputs(program):
            expected = interpret(program, data)
            lines.append(f'{program.name} {data.hex() or "-"} {expected.hex() or "-"}\n')
            counts[program.name] += 1
    return ''.join(lines).encode('ascii'), counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', type=Path, required=True)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--probe', type=Path, required=True, help='NDK-built tests/android/brainfuckc_probe.c')
    parser.add_argument('--out', type=Path, default=ROOT / 'build/brainfuckc')
    args = parser.parse_args()
    report = args.out / 'device-result.json'
    report.unlink(missing_ok=True)
    wire, counts = corpus(args.out)
    (args.out / 'vectors.txt').write_bytes(wire)
    adb = [str(args.adb), '-s', args.serial]

    def run(*command, **kwargs):
        result = subprocess.run(adb + list(command), capture_output=True, timeout=120, **kwargs)
        if result.returncode:
            raise RuntimeError(f'ADB {command[0]} failed ({result.returncode}): '
                               + (result.stderr + result.stdout).decode(errors='replace'))
        return result.stdout

    abi = run('shell', 'getprop', 'ro.product.cpu.abilist').decode().strip()
    if 'arm64-v8a' not in abi.split(','):
        raise ValueError(f'ARM64 device required, got {abi}')
    remote = '/data/local/tmp/youtubehideads_brainfuckc'
    run('shell', 'mkdir', '-p', remote)
    for path in [args.probe] + [args.out / (name + '.elf') for name in counts]:
        target = remote + '/' + ('probe' if path == args.probe else path.name)
        run('push', str(path), target)
        if run('shell', 'sha256sum', target).decode().split()[0] != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError(f'device transport hash mismatch: {path.name}')
    run('shell', 'chmod', '700', remote + '/probe')
    stdout = run('shell', '-T', remote + '/probe', remote, input=wire).decode().strip()
    expected = f'PASS {sum(counts.values())} native/reference comparisons'
    if stdout != expected:
        raise ValueError(f'native comparison report mismatch: {stdout}')
    evidence = {'status': 'PASS', 'abi': abi, 'comparisons': counts, 'stdout': stdout,
                'android_release': run('shell', 'getprop', 'ro.build.version.release').decode().strip(),
                'android_sdk': run('shell', 'getprop', 'ro.build.version.sdk').decode().strip(),
                'vectors_sha256': hashlib.sha256(wire).hexdigest(),
                'probe_sha256': hashlib.sha256(args.probe.read_bytes()).hexdigest(),
                'policy_manifest_sha256': hashlib.sha256((args.out / 'policies.json').read_bytes()).hexdigest(),
                'scope': 'ANDROID_SHELL_MMAP_CALLABLE_ONLY',
                'bionic_dlopen_tested': False, 'art_jni_tested': False,
                'xposed_tested': False, 'youtube_ad_removal_tested': False}
    report.write_text(json.dumps(evidence, indent=2, sort_keys=True) + '\n')
    print(stdout)


if __name__ == '__main__':
    main()
