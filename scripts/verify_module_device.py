"""Exercise the real module's settings entry/page in YouTube without changing its data."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time
import xml.etree.ElementTree as ET

from toolchain.brainfuck.build import ROOT
from toolchain.xax.module_graph import MODULE_CLASS, YOUTUBE


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', type=Path, required=True)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--build', type=Path, default=ROOT / 'build/module')
    parser.add_argument('--out', type=Path, default=ROOT / 'build/module-device')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    result_file = args.out / 'device-result.json'
    result_file.unlink(missing_ok=True)
    build = json.loads((args.build / 'build-result.json').read_text())
    apk = Path(build['apk'])
    digest = hashlib.sha256(apk.read_bytes()).hexdigest()
    if digest != build['apk_sha256']:
        raise ValueError('module APK differs from build evidence')
    adb = [str(args.adb), '-s', args.serial]

    def run(*command, binary=False):
        result = subprocess.run(adb + list(command), capture_output=True, timeout=30)
        if result.returncode:
            raise RuntimeError((result.stdout + result.stderr).decode(errors='replace'))
        return result.stdout if binary else result.stdout.decode().strip()

    package = MODULE_CLASS.rsplit('.', 1)[0]
    installed = run('shell', 'pm', 'path', package).splitlines()
    if len(installed) != 1 or not installed[0].startswith('package:'):
        raise ValueError('expected one installed module base APK')
    if run('shell', 'sha256sum', installed[0][8:]).split()[0] != digest:
        raise ValueError('installed module does not match the tested build')
    remote_xml = '/data/local/tmp/youtubehideads-module-verification.xml'

    def tree():
        run('shell', 'uiautomator', 'dump', remote_xml)
        return ET.fromstring(run('shell', 'cat', remote_xml))

    def entries(root):
        return [node for node in root.iter('node') if node.get('content-desc') == 'YouTubeHideAds']

    def wait_for(predicate):
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            root = tree()
            if predicate(root):
                return root
            time.sleep(0.25)
        raise AssertionError('expected module page/entry did not become visible')

    def tap(node):
        bounds = list(map(int, re.findall(r'\d+', node.get('bounds', ''))))
        if len(bounds) != 4 or bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
            raise ValueError('no visible click target')
        run('shell', 'input', 'tap', str((bounds[0] + bounds[2]) // 2), str((bounds[1] + bounds[3]) // 2))

    def page(root):
        return any(node.get('text') == 'Module connected inside YouTube.' for node in root.iter('node'))

    run('shell', 'am', 'start', '-W', '-n', YOUTUBE + '/com.google.android.apps.youtube.app.application.Shell_SettingsActivity')
    settings = wait_for(lambda root: len(entries(root)) == 1)
    pid = run('shell', 'pidof', YOUTUBE)
    if not pid.isdigit():
        raise ValueError('expected one YouTube main process')
    (args.out / 'settings.png').write_bytes(run('exec-out', 'screencap', '-p', binary=True))
    for cycle in range(3):
        tap(entries(settings)[0])
        opened = wait_for(page)
        if cycle == 0:
            (args.out / 'page.png').write_bytes(run('exec-out', 'screencap', '-p', binary=True))
            ET.ElementTree(opened).write(args.out / 'page.xml', encoding='utf-8', xml_declaration=True)
        if cycle == 1:
            run('shell', 'input', 'keyevent', '4')
        else:
            back = next(node for node in opened.iter('node')
                        if node.get('text', '').casefold() == 'back to youtube settings')
            tap(back)
        settings = wait_for(lambda root: not page(root) and len(entries(root)) == 1)
        if run('shell', 'pidof', YOUTUBE) != pid:
            raise AssertionError('YouTube process restarted during module page navigation')
    ET.ElementTree(settings).write(args.out / 'settings.xml', encoding='utf-8', xml_declaration=True)
    log = run('logcat', '-d', '--pid=' + pid, '-v', 'brief')
    class_name = build['xax_class'].replace('/', '.')
    if f'Hooker [{class_name}] crashed' in log:
        raise AssertionError('module hook failed under Vector protection')
    checks = {
        'module_loaded_in_youtube': f'Loaded module {package} successfully' in log,
        'lifecycle_hook_installed': 'YouTube lifecycle hook installed' in log,
        'one_toolbar_entry_after_each_cycle': len(entries(settings)) == 1,
        'page_open_close_cycles': 3,
        'system_back_works': True,
        'brainfuck_executed_in_youtube': 'Brainfuck policy self-check passed' in log,
        'no_brainfuck_self_check_failure': 'Brainfuck policy self-check FAILED' not in log,
        'youtube_process_survived': run('shell', 'pidof', YOUTUBE) == pid,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    relevant_log = '\n'.join(line for line in log.splitlines() if 'YouTubeHideAds' in line or class_name in line)
    (args.out / 'module.log').write_text(relevant_log + '\n')
    launcher = run('shell', 'cmd', 'package', 'resolve-activity', '--brief', '-a',
                   'android.intent.action.MAIN', '-c', 'android.intent.category.LAUNCHER', '-p', package)
    if 'No activity found' not in launcher:
        raise AssertionError('module unexpectedly has a launcher Activity')
    report = {'status': 'PASS', 'apk_sha256': digest, 'build': build, 'checks': checks,
              'launcher_resolution': launcher, 'page_owned_by': YOUTUBE,
              'youtube_version': run('shell', 'dumpsys', 'package', YOUTUBE).split('versionName=', 1)[1].split()[0],
              'android_sdk': run('shell', 'getprop', 'ro.build.version.sdk'),
              'module_left_installed': True, 'advertisement_suppression_tested': False,
              'sponsorblock_tested': False}
    result_file.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
