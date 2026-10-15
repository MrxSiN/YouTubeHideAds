"""Build and exercise the canonical XAX -> BF managed call on Android ART."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from scripts.verify_xax_device import corpus
from toolchain.brainfuck.build import ROOT
from toolchain.brainfuck.router import build_router
from toolchain.xax.dex_methods import inspect_methods
from toolchain.xax.managed_dispatch import build_dispatch
from toolchain.xax.router_call_plan import ROUTER_CLASS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xax-source', type=Path, required=True)
    parser.add_argument('--java-home', type=Path, required=True)
    parser.add_argument('--build-tools', type=Path, required=True)
    parser.add_argument('--adb', type=Path, required=True)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--out', type=Path, default=ROOT / 'build/xax-managed-dispatch')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    result_file = args.out / 'device-result.json'
    result_file.unlink(missing_ok=True)
    policies = args.out / 'policies'
    build_router(policies)
    compiled = build_dispatch(args.xax_source, policies, args.out)
    suffix = '.exe' if os.name == 'nt' else ''
    java = args.java_home / 'bin' / ('java' + suffix)
    javac = args.java_home / 'bin' / ('javac' + suffix)
    harness = ROOT / 'tests/android/XaxManagedDispatchProbe.java'
    d8_jar = args.build_tools / 'lib/d8.jar'

    def run(command, **kwargs):
        result = subprocess.run([str(item) for item in command], capture_output=True, timeout=120, **kwargs)
        if result.returncode:
            raise RuntimeError((result.stderr + result.stdout).decode(errors='replace'))
        return result.stdout.decode().strip()

    with tempfile.TemporaryDirectory(dir=args.out) as folder:
        work = Path(folder)
        run((javac, '--release', '17', '-d', work, harness))
        run((java, '-cp', d8_jar, 'com.android.tools.r8.D8', '--release', '--min-api', '28',
             '--output', work, args.out / 'dispatch.jar', policies / 'brainfuck-router.jar',
             work / 'XaxManagedDispatchProbe.class'))
        dex = (work / 'classes.dex').read_bytes()
        if list(work.glob('classes*.dex')) != [work / 'classes.dex']:
            raise ValueError('expected one managed probe DEX')
    expected_classes = {'L' + compiled['class_name'].replace('.', '/') + ';',
                        'L' + ROUTER_CLASS + ';', 'LXaxManagedDispatchProbe;'}
    methods = inspect_methods(dex, required_classes=expected_classes)
    if not methods['L' + compiled['class_name'].replace('.', '/') + ';']['entry([B)[B']['code_units']:
        raise ValueError('missing XAX managed entry')
    dex_path = args.out / 'probe.dex'
    dex_path.write_bytes(dex)
    paired, _ = corpus()
    wire = b''.join(line + b'\n' for line in paired.splitlines() if line.startswith(b'dispatch_all '))
    count = len(wire.splitlines())
    (args.out / 'vectors.txt').write_bytes(wire)
    adb = [args.adb, '-s', args.serial]

    def device(*command, **kwargs):
        return run([*adb, *command], **kwargs)

    remote = '/data/local/tmp/youtubehideads_managed_dispatch'
    device('shell', 'mkdir', '-p', remote)
    target = remote + '/probe.dex'
    device('shell', f'if [ -f {target} ]; then chmod 600 {target}; fi')
    device('push', dex_path, target)
    digest = hashlib.sha256(dex).hexdigest()
    if device('shell', 'sha256sum', target).split()[0] != digest:
        raise ValueError('ADB DEX transport mismatch')
    device('shell', 'chmod', '444', target)
    stdout = device('shell', '-T', f'CLASSPATH={target} app_process /system/bin '
                    f'XaxManagedDispatchProbe {compiled["class_name"]}', input=wire)
    expected = f'PASS managed_xax_bf={count} invalid=4 recovery=1 native_libraries=0'
    if stdout != expected:
        raise ValueError(f'managed dispatch comparison mismatch: {stdout}')
    report = {'status': 'PASS', 'stdout': stdout, 'comparisons': count,
              'xax_build': compiled, 'dex_sha256': digest,
              'vectors_sha256': hashlib.sha256(wire).hexdigest(),
              'harness_sha256': hashlib.sha256(harness.read_bytes()).hexdigest(),
              'd8_sha256': hashlib.sha256(d8_jar.read_bytes()).hexdigest(),
              'android_release': device('shell', 'getprop', 'ro.build.version.release'),
              'android_sdk': device('shell', 'getprop', 'ro.build.version.sdk'),
              'model': device('shell', 'getprop', 'ro.product.model'),
              'jni_required': False, 'apk_installed': False, 'youtube_hooks': False,
              'scope': 'RAW_POLICY_CALL_ONLY_NOT_A_VALIDATED_HOST_ABI'}
    result_file.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(stdout)


if __name__ == '__main__':
    main()
