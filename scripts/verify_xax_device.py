"""Test-only ART/BF and XAX JNI calls, with class/method lookup in a C oracle."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

from scripts.probe_android_integration import XAX_COMMIT
from scripts.verify_brainfuckc_device import inputs
from toolchain.brainfuck.build import FEATURES
from toolchain.brainfuck.core import interpret, load
from toolchain.brainfuck.host_link import verify_jar
from toolchain.brainfuck.router import verify_router, selector_map
from toolchain.xax.link_d8 import validate_policy_dex
from toolchain.xax.verify_apk import inspect_dex, inspect_module_apk


def artifacts(apk: Path, policies: Path, transport: Path, harness: Path, native_probe: Path) -> dict[str, bytes]:
    verify_jar(policies / 'brainfuck-policies.jar', policies / 'policies.json')
    verify_router(policies / 'brainfuck-router.jar', policies / 'router.json')
    link = json.loads(apk.with_suffix('.evidence.json').read_text())
    for path, key in ((apk, 'apk_sha256'),
                      (policies / 'brainfuck-policies.jar', 'bf_jar_sha256'),
                      (policies / 'brainfuck-router.jar', 'bf_router_jar_sha256')):
        if hashlib.sha256(path.read_bytes()).hexdigest() != link[key]:
            raise ValueError(f'linked input hash mismatch: {path.name}')
    inspect_module_apk(apk, mode='linked_router_smoke')
    report = json.loads((transport / 'evidence.json').read_text())
    if report['xax_commit'] != XAX_COMMIT or report['status'] != 'XAX_TRANSPORT_COMPILED':
        raise ValueError('unverified XAX transport compiler report')
    for name, digest in report['artifacts'].items():
        if name not in {'transport.xax-store', 'classes.dex', 'libxaxapp.so'}:
            raise ValueError('unexpected transport artifact')
        if hashlib.sha256((transport / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'XAX transport hash mismatch: {name}')
    if set(report['artifacts']) != {'transport.xax-store', 'classes.dex', 'libxaxapp.so'}:
        raise ValueError('incomplete transport artifacts')
    files = {'transport.dex': (transport / 'classes.dex').read_bytes(),
             'libxaxapp.so': (transport / 'libxaxapp.so').read_bytes(),
             'libxaxprobe.so': native_probe.read_bytes(),
             'harness.dex': harness.read_bytes()}
    inspect_dex(files['harness.dex'])
    blobs = []
    with zipfile.ZipFile(apk) as archive:
        for name in archive.namelist():
            if name.startswith('classes') and name.endswith('.dex'):
                data = archive.read(name)
                if any(cls.startswith('Lorg/youtubehideads/bf/') for cls in inspect_dex(data)['class_descriptors']):
                    blobs.append(data)
    validate_policy_dex(blobs, with_router=True)
    for index, data in enumerate(blobs):
        files[f'policies-{index}.dex'] = data
    return files


def corpus() -> tuple[bytes, int]:
    selectors = selector_map()
    lines = []
    for path in sorted(FEATURES.rglob('*.bf')):
        program = load(path)
        for data in inputs(program):
            expected = interpret(program, data).hex() or '-'
            lines.append(f'{program.name} {data.hex() or "-"} {expected}\n')
            routed = bytes((selectors[program.name],)) + data
            lines.append(f'dispatch_all {routed.hex()} {expected}\n')
    return ''.join(lines).encode('ascii'), len(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', type=Path, required=True)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--apk', type=Path, required=True)
    parser.add_argument('--policies', type=Path, required=True)
    parser.add_argument('--transport', type=Path, required=True)
    parser.add_argument('--harness', type=Path, required=True)
    parser.add_argument('--native-probe', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path('build/xax-device'))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    result_file = args.out / 'device-result.json'
    result_file.unlink(missing_ok=True)
    files = artifacts(args.apk, args.policies, args.transport, args.harness, args.native_probe)
    wire, count = corpus()
    adb = [str(args.adb), '-s', args.serial]

    def run(*command, **kwargs):
        result = subprocess.run(adb + list(command), capture_output=True, timeout=120, **kwargs)
        if result.returncode:
            raise RuntimeError((result.stderr + result.stdout).decode(errors='replace'))
        return result.stdout.decode().strip()

    abi = run('shell', 'getprop', 'ro.product.cpu.abilist')
    if 'arm64-v8a' not in abi.split(','):
        raise ValueError('ARM64 device required')
    remote = '/data/local/tmp/youtubehideads_xax'
    run('shell', 'mkdir', '-p', remote)
    for name, data in files.items():
        path = args.out / name
        path.write_bytes(data)
        target = remote + '/' + name
        run('shell', f'if [ -f {target} ]; then chmod 600 {target}; fi')
        run('push', str(path), target)
        if run('shell', 'sha256sum', target).split()[0] != hashlib.sha256(data).hexdigest():
            raise ValueError(f'ADB transport mismatch: {name}')
        run('shell', 'chmod', '444', target)
    dex = ':'.join(remote + '/' + name for name in files if name.endswith('.dex'))
    stdout = run('shell', '-T', f'CLASSPATH={dex} app_process -Djava.library.path={remote} '
                 '/system/bin XaxTransportProbe', input=wire)
    if stdout != f'PASS transport=257 bf={count} xax_calls={count // 2}':
        raise ValueError(f'ART comparison mismatch: {stdout}')
    report = {'status': 'PASS', 'stdout': stdout, 'bf_comparisons': count,
              'transport_identity_cases': 257, 'xax_commit': XAX_COMMIT,
              'android_release': run('shell', 'getprop', 'ro.build.version.release'),
              'android_sdk': run('shell', 'getprop', 'ro.build.version.sdk'), 'abi': abi,
              'artifacts': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
              'vectors_sha256': hashlib.sha256(wire).hexdigest(),
              'xax_calls_bf': True, 'xax_bf_comparisons': count // 2,
              'class_and_method_lookup': 'TEST_ONLY_C_ORACLE',
              'xax_runtime_class_provenance_checks': False, 'java_test_calls_bf': True,
              'xax_jni_echo_executed': True, 'apk_installed': False, 'youtube_hooks': False}
    result_file.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(stdout)


if __name__ == '__main__':
    main()
