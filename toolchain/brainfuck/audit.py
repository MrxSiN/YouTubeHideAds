"""Generate a machine-readable honesty/provenance audit of compiled BF owners.

This script is not Android feature logic. It deliberately reports missing XAX
rather than treating planned host operations as implemented.
"""
import json
from pathlib import Path
from .build import FEATURES,ROOT
from .core import load


def audit():
    owners=[]
    for path in sorted(FEATURES.rglob('*.bf')):
        p=load(path)
        owners.append({'feature':p.name,'path':str(path.relative_to(ROOT)),
                       'source_sha256':p.digest,'commands':len(p.code),
                       'verified_interpreter':True,'android_hook_verified':False})
    if not owners:
        raise RuntimeError('no feature Brainfuck program')
    hidden=[]
    for ext in ('*.java','*.kt','*.c','*.cpp','*.py'):
        for file in ROOT.rglob(ext):
            rel=file.relative_to(ROOT)
            if any(part in {'generated','tests','.git','build','dist'} for part in rel.parts):continue
            if rel.parts[0]=='toolchain':continue
            # These are explicit off-device diagnostics/build gates, NEVER
            # bundled into Android/XAX application runtime artifacts.
            if rel.as_posix() in {'scripts/probe_android_integration.py',
                            'scripts/verify_brainfuckc_device.py',
                            'scripts/verify_xax_device.py',
                            'scripts/verify_managed_dispatch_device.py',
                            'scripts/verify_module_device.py',
                            'scripts/verify_linkage.py'}:continue
            hidden.append(str(rel))
    if hidden:raise RuntimeError('unexpected non-BF app sources: '+str(hidden))
    return {'policy_count':len(owners),'language_boundary':'policy BF / platform XAX / off-device Python tooling',
            'scope':'POLICY_SOURCE_OWNERS_ONLY',
            'xax_semantic_store':None,'android_apk_build':None,'device_verification':None,
            'owners':owners}

if __name__=='__main__':
    report=audit()
    dest=ROOT/'generated'/'language_audit.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(f'AUDIT: {len(report["owners"])} policy source owners; integration evidence not inspected -> {dest}')
