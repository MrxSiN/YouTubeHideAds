"""Off-device D8 integration with a XAX-produced unsigned Android APK.

The XAX host APK and AOT Brainfuck JVM class files must already exist. D8 is
an external Android tool (not a project runtime implementation). This tool
places its DEX output into unused APK slots, and cannot make hooks invoke BF.
No signing, no SDK claims, no runtime proof and no application feature fallback.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile

from toolchain.brainfuck.host_link import verify_jar
from toolchain.brainfuck.router import ROUTER_CLASS, verify_router
from toolchain.xax.verify_apk import ArtifactError, inspect_dex, inspect_module_apk
from toolchain.xax.dex_methods import DexMethodsError, inspect_methods
from toolchain.brainfuck.host_abi import FEATURE_IDS


class LinkError(ValueError):
    pass


def source_archive(jar: Path, manifest: Path, optimize: bool) -> dict:
    try: return verify_jar(jar,manifest,optimized=optimize)
    except (OSError,ValueError,KeyError,zipfile.BadZipFile) as exc:
        raise LinkError(f'BF_SOURCE_JAR_VERIFICATION_FAILED: {exc}') from exc


def _dex_files(files: dict[str,bytes]) -> list[str]:
    def key(name): return 1 if name == 'classes.dex' else int(name[7:-4])
    return sorted((name for name in files if re.fullmatch(r'classes(?:[2-9]\d*)?\.dex',name)), key=key)


def validate_policy_dex(blobs: list[bytes], *, with_router: bool = False) -> dict:
    expected={f'Lorg/youtubehideads/bf/{name};' for name in FEATURE_IDS}
    if with_router:
        expected.add('L'+ROUTER_CLASS+';')
    seen={}
    summaries=[]
    for blob in blobs:
        try:
            view=inspect_dex(blob)
            requested=expected & set(view['class_descriptors'])
            if set(view['class_descriptors']) != requested:
                raise LinkError('UNEXPECTED_D8_COMPILED_CLASS')
            if requested:
                methods=inspect_methods(blob,required_classes=requested)
                for cls,sigs in methods.items():
                    if cls in seen: raise LinkError('DUPLICATE_BF_CLASS')
                    target=sigs.get('run([B)[B')
                    if not target or not target['code_units']:
                        raise LinkError('BF_RUN_METHOD_MISSING_OR_ABSTRACT')
                    seen[cls]=target
            summaries.append(view['sha256'])
        except (ArtifactError,DexMethodsError) as exc:
            raise LinkError(f'INVALID_D8_DEX: {exc}') from exc
    if set(seen)!=expected: raise LinkError('INCOMPLETE_D8_BRAINFUCK_CLASSES')
    return {'policy_class_count':len(seen)-int(with_router), 'router_class_count':int(with_router),'dex_sha256':summaries,
            'all_run_methods_have_code':True,'dex_execution_verified':False}


def collect_d8_outputs(output_dir: Path) -> list[bytes]:
    paths=sorted(output_dir.glob('classes*.dex'))
    expected=['classes.dex', *(f'classes{i}.dex' for i in range(2,len(paths)+1))]
    if [p.name for p in paths] != expected or not paths:
        raise LinkError('D8_EXPECTED_CONTIGUOUS_DEX_OUTPUT')
    if any(not p.is_file() for p in paths):raise LinkError('D8_NOT_REGULAR_FILE')
    return [p.read_bytes() for p in paths]


def merge_unsigned(base_apk: bytes, policy_dex: list[bytes], *, with_router: bool = False) -> bytes:
    """Stable ZIP composition. Always produces UNSIGNED bytes; never patch signatures."""
    if b'APK Sig Block 42' in base_apk:
        raise LinkError('APK_SIGNING_BLOCK_MODIFICATION_FORBIDDEN')
    try:
        with zipfile.ZipFile(io.BytesIO(base_apk)) as z:
            names=z.namelist()
            if len(names)!=len(set(names)):raise LinkError('APK_DUPLICATE_ENTRY')
            if any(name.startswith('/') or '..' in name.split('/') for name in names):
                raise LinkError('APK_UNSAFE_PATH')
            if any(re.fullmatch(r'META-INF/[^/]+\.(RSA|DSA|EC|SF)',name,re.I) for name in names):
                raise LinkError('SIGNED_APK_MODIFICATION_FORBIDDEN')
            original={name:z.read(name) for name in names}
            original_compression={name:z.getinfo(name).compress_type for name in names}
            if any(kind not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED) for kind in original_compression.values()):
                raise LinkError('APK_UNSUPPORTED_COMPRESSION')
    except (zipfile.BadZipFile,EOFError) as exc:
        raise LinkError('APK_NOT_ZIP') from exc
    existing=_dex_files(original)
    if not existing:raise LinkError('XAX_APK_HAS_NO_DEX')
    # Refuse to replace an existing class. Only append disjoint DEX namespaces.
    used_classes=set()
    for name in existing:
        try: descriptors=set(inspect_dex(original[name])['class_descriptors'])
        except ArtifactError as exc:raise LinkError(f'INVALID_XAX_DEX: {exc}') from exc
        if used_classes & descriptors:raise LinkError('XAX_DUPLICATE_CLASS')
        used_classes.update(descriptors)
    target_classes={f'Lorg/youtubehideads/bf/{name};' for name in FEATURE_IDS}
    if with_router: target_classes.add('L'+ROUTER_CLASS+';')
    if used_classes & target_classes:raise LinkError('POLICY_CLASSES_ALREADY_IN_BASE')
    validate_policy_dex(policy_dex, with_router=with_router)
    next_num=max(1 if name=='classes.dex' else int(name[7:-4]) for name in existing)+1
    for dex in policy_dex:
        name='classes.dex' if next_num==1 else f'classes{next_num}.dex'
        if name in original:raise LinkError('DEX_SLOT_COLLISION')
        original[name]=dex
        next_num+=1
    mem=io.BytesIO()
    with zipfile.ZipFile(mem,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as out:
        for name,data in sorted(original.items()):
            info=zipfile.ZipInfo(name,(1980,1,1,0,0,0))
            info.compress_type=original_compression.get(name,zipfile.ZIP_DEFLATED)
            info.external_attr=0o644<<16
            out.writestr(info,data)
    return mem.getvalue()


def build_linked_apk(*,base:Path,jar:Path,manifest:Path,d8:str,out:Path,
                     optimize:bool=False,router_jar:Path|None=None,
                     router_manifest:Path|None=None) -> dict:
    registry=source_archive(jar,manifest,optimize)
    if (router_jar is None) != (router_manifest is None):
        raise LinkError('ROUTER_JAR_AND_MANIFEST_REQUIRED_TOGETHER')
    with_router = router_jar is not None
    if with_router:
        try: verify_router(router_jar,router_manifest,optimize=optimize)
        except (OSError,ValueError,KeyError,zipfile.BadZipFile) as exc:
            raise LinkError(f'BF_ROUTER_JAR_VERIFICATION_FAILED: {exc}') from exc
    if not shutil.which(d8) and not Path(d8).is_file():raise LinkError('D8_MISSING')
    # The smoke-only APK deliberately cannot be relabelled as an integrated module.
    inspect_module_apk(base,mode='smoke')
    with tempfile.TemporaryDirectory(prefix='youtubehideads-d8-') as tmp:
        dest=Path(tmp)
        command=[d8,'--release','--min-api','28','--output',str(dest),str(jar)]
        if with_router: command.append(str(router_jar))
        try:
            run=subprocess.run(command,text=True,capture_output=True,timeout=120)
        except (OSError,subprocess.TimeoutExpired) as exc:
            raise LinkError(f'D8_EXECUTION_FAILED: {exc}') from exc
        if run.returncode:raise LinkError(f'D8_COMPILE_FAILED: {run.stderr[:1200]}')
        blobs=collect_d8_outputs(dest)
    policy_view=validate_policy_dex(blobs,with_router=with_router)
    composed=merge_unsigned(base.read_bytes(),blobs,with_router=with_router)
    # This remains a CONTROLLED-target smoke-only APK, not a YouTube module.
    # The BF classes are present but never called by its no-op host.
    view=inspect_module_apk(composed,mode='linked_router_smoke' if with_router else 'linked_smoke')
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(composed)
    report={'status':'BF_DEX_STRUCTURALLY_LINKED_HOST_NOT_CONNECTED',
            'base_apk_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),
            'bf_jar_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),
            'bf_router_jar_sha256':hashlib.sha256(router_jar.read_bytes()).hexdigest() if with_router else None,
            'bf_source_sha256':{name:info['sha256'] for name,info in sorted(registry.items())},
            'policy_dex':policy_view,'apk':view,'apk_sha256':hashlib.sha256(composed).hexdigest(),
            'signed':False,'android_runtime_tested':False,'xax_call_graph_reaches_bf':False,
            'youtube_hooked':False}
    out.with_suffix('.evidence.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--xax-smoke-apk',type=Path,required=True)
    parser.add_argument('--jar',type=Path,default=Path('generated/brainfuck-policies.jar'))
    parser.add_argument('--manifest',type=Path,default=Path('generated/policies.json'))
    parser.add_argument('--d8',default='d8')
    parser.add_argument('--router-jar',type=Path)
    parser.add_argument('--router-manifest',type=Path)
    parser.add_argument('--out',type=Path,default=Path('build/xax-lifecycle-smoke/linked-unsigned.apk'))
    parser.add_argument('--optimize',action='store_true')
    args=parser.parse_args()
    try: print(json.dumps(build_linked_apk(base=args.xax_smoke_apk,jar=args.jar,
               manifest=args.manifest,d8=args.d8,out=args.out,optimize=args.optimize,
               router_jar=args.router_jar,router_manifest=args.router_manifest),indent=2))
    except (LinkError,ArtifactError,OSError) as exc:
        parser.exit(2,f'BF_DEX_LINK_BLOCKED: {exc}\n')

if __name__=='__main__':main()
