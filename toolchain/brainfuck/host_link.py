"""Off-device Brainfuck/JVM/host-ABI linkage test oracle.

Never shipped with an Android module. It verifies deterministic compiled class
identity, runs actual generated JVM machine code, and applies protocol checks.
The real Android caller must be implemented through verified XAX semantic state.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import zipfile

from .build import ROOT, FEATURES
from .core import load, program_fuel
from .host_abi import (
    ABIError, FEATURE_IDS, Reply, Request, checked_reply, load_programs, validate_request,
)
from .jvm import compile_class


def verify_jar(jar: Path, manifest_path: Path, *, optimized: bool = False) -> dict[str, dict]:
    """Reject source/JAR drift and unknown classes; do not trust manifests alone."""
    registry = json.loads(manifest_path.read_text(encoding='utf-8'))
    if set(registry) != set(FEATURE_IDS):
        raise ABIError('JAR_REGISTRY_MISMATCH')
    expected_names = set()
    with zipfile.ZipFile(jar) as archive:
        for name, manifest in registry.items():
            p = (ROOT / manifest['source']).resolve()
            if not p.is_file() or not p.is_relative_to(FEATURES.resolve()):
                raise ABIError('INVALID_SOURCE_PATH')
            program = load(p)
            if program.name != name or program.digest != manifest['sha256'] or \
               program_fuel(program) != manifest.get('fuel_limit'):
                raise ABIError('JAR_SOURCE_DIGEST_MISMATCH')
            class_name = f'org/youtubehideads/bf/{name}'
            if manifest['class'] != class_name or manifest['method'] != 'run([B)[B':
                raise ABIError('JAR_INTERFACE_MISMATCH')
            expected_names.add(class_name + '.class')
            compiled = compile_class(program, class_name, optimize=optimized)
            try:
                actual = archive.read(class_name+'.class')
            except KeyError:
                raise ABIError('MISSING_COMPILED_POLICY') from None
            if actual != compiled:
                raise ABIError('STALE_OR_TAMPERED_CLASS')
        if set(archive.namelist()) != expected_names:
            raise ABIError('UNEXPECTED_JAR_CONTENTS')
    return registry


def exercise_aot_frames(frames: list[bytes], *, jar: Path, manifest: Path,
                        optimized: bool = False, active_generation: int = 1) -> list[bytes]:
    """Run real compiled BF classes on JVM and return checked wire responses.

    Works only on development machines with Java/Javac. No Android feature
    policy is implemented in the harness, and no hook/seek is executed.
    """
    verify_jar(jar, manifest, optimized=optimized)
    programs = load_programs()
    decoded = [Request.unpack(frame) for frame in frames]
    for req in decoded:
        validate_request(req, programs)
    id_to_name = {v: k for k,v in FEATURE_IDS.items()}
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp)
        runner = ROOT/'tests/jvm/Runner.java'
        p = subprocess.run(['javac','-d',str(cp),str(runner)],capture_output=True,text=True)
        if p.returncode:
            raise ABIError('JAVA_RUNNER_BUILD_FAILED')
        payload=''.join(f'{id_to_name[req.feature_id]} {req.data.hex()}\n' for req in decoded)+'END\n'
        result=subprocess.run(['java','-cp',str(cp)+os.pathsep+str(jar),'Runner'],input=payload,
                              text=True,capture_output=True)
        if result.returncode:
            raise ABIError('JVM_EXECUTION_FAILED')
    lines = result.stdout.splitlines()
    if len(lines) != len(decoded):
        raise ABIError('JVM_OUTPUT_COUNT_MISMATCH')
    replies=[]
    for req,line in zip(decoded,lines):
        if not line.startswith('OK '):
            raise ABIError('JVM_POLICY_EXECUTION_ERROR')
        try:
            b=bytes.fromhex(line[3:])
        except ValueError as e:
            raise ABIError('MALFORMED_JVM_RESULT') from e
        if not b or len(b) != (9 if b[0] == 4 else 1):
            raise ABIError('JVM_POLICY_OUTPUT_LENGTH')
        rep=Reply(req.feature_id,req.generation,b[0],b[1:])
        checked_reply(req,rep,active_generation=active_generation)
        replies.append(rep.pack())
    return replies
