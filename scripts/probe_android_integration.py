#!/usr/bin/env python3
"""Honest environment gate for future canonical XAX/Android integration.

No XAX text synthesis, Android APK generation, or assumed SDK tools. This probe
only examines present dependencies; it never marks an unexecuted test as passed.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

XAX_COMMIT='9e44eedfc241d25bb5062b38af105f75234000e2'

def _git_revision(root: Path) -> str | None:
    if not root.is_dir():return None
    try:
        run=subprocess.run(['git','-C',str(root),'rev-parse','HEAD'],text=True,capture_output=True,timeout=4)
        if run.returncode == 0:return run.stdout.strip()
    except (OSError,subprocess.TimeoutExpired):pass
    return None


def probe() -> dict:
    xax_dir=os.environ.get('XAX_SOURCE_DIR')
    root=Path(xax_dir).expanduser().resolve() if xax_dir else None
    revision=_git_revision(root) if root else None
    module_available=bool(root and (root/'compiler/src/xax_compiler.py').is_file()
                          and (root/'compiler/src/xax_build.py').is_file())
    tools={binary:shutil.which(binary) for binary in ('git','java','javac','adb','d8','sdkmanager')}
    sdk_dirs=[os.environ.get('ANDROID_SDK_ROOT'),os.environ.get('ANDROID_HOME')]
    sdk=next((str(Path(p).expanduser().resolve()) for p in sdk_dirs if p and Path(p).is_dir()),None)
    blockers=[]
    if revision!=XAX_COMMIT:blockers.append('PINNED_XAX_REVISION_NOT_PRESENT')
    if not module_available:blockers.append('PINNED_XAX_MODULES_NOT_PRESENT')
    if sdk is None:blockers.append('ANDROID_SDK_NOT_FOUND')
    if not tools['d8'] and not (sdk and any(list(Path(sdk).glob('build-tools/*/' + name))
                                           for name in ('d8', 'd8.bat'))):
        blockers.append('D8_NOT_FOUND')
    if not tools['adb'] and not (sdk and any((Path(sdk)/'platform-tools'/name).is_file()
                                            for name in ('adb', 'adb.exe'))):
        blockers.append('ADB_NOT_FOUND')
    # Pinned public repository currently lists license=null; an explicit upstream
    # grant must be reviewed. This check intentionally cannot be bypassed by an
    # arbitrary local environment string.
    blockers.append('XAX_REDISTRIBUTION_LICENSE_UNRESOLVED')
    # The installed page module is verified; these gates concern live ad actions.
    blockers.append('CANONICAL_XAX_AD_HOST_STORE_NOT_CONSTRUCTED')
    blockers.append('VALIDATED_BF_AD_HOST_NOT_CONNECTED')
    blockers.append('VALIDATED_XAX_AD_DISPATCH_NOT_IMPLEMENTED')
    # The verified managed call path uses ART resolution and does not need JNI.
    blockers.append('YOUTUBE_AD_RUNTIME_TEST_NOT_EXECUTED')
    return {'status':'BLOCKED','xax_required_revision':XAX_COMMIT,'xax_detected_revision':revision,
            'scope':'PRODUCTION_AD_HOST_ONLY',
            'xax_modules_present':module_available,'sdk_root':sdk,'tools':tools,'blockers':blockers,
            'android_apk_tested':False,'xposed_hooks_tested':False}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--require-ready',action='store_true',help='Exit nonzero if incomplete')
    args=parser.parse_args()
    result=probe()
    print(json.dumps(result,indent=2,sort_keys=True))
    if args.require_ready and result['status']!='READY':sys.exit(2)
