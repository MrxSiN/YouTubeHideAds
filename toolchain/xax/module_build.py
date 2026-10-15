"""Build the launcherless YouTube module from XAX graphs and fixed DEX ABI glue."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile

from scripts.probe_android_integration import XAX_COMMIT
from toolchain.brainfuck.build import ROOT
from toolchain.brainfuck.router import build_router, verify_router
from .module_graph import API, MODULE_CLASS, YOUTUBE, make_module_graph
from .smoke_build import require_pinned_checkout
from .store_evidence import root_reachable_closure


def build_module(checkout: Path, output: Path, java_home: Path, sdk: Path, api_aar: Path) -> dict:
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / 'build-result.json').unlink(missing_ok=True)
    checkout = require_pinned_checkout(checkout)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(checkout / 'compiler/src'))
    from xax_apk import ApkEntry, build_apk
    from xax_compiler import (Kind, StoreReader, jvm_classfile_general_target,
        object_with_refs, target as semantic_target, verify_store, write_store)
    from xax_dex import (DexAssembledMethod, DexBridgeSpec, DexInstruction, DexMethodRef,
        DexProto, emit_dex039_bridge, inspect_dex_references)
    from xax_jvm import compile_jvm_bound_target
    from xax_libxposed import LibxposedModuleDescription, emit_libxposed_metadata, libxposed_module_semantics
    from xax_vector import LibxposedApiTable, check_vector_module_apk, load_vector_pin

    pin = load_vector_pin()
    api_digest = hashlib.sha256(api_aar.read_bytes()).hexdigest()
    if api_digest != pin['libxposed_api']['aar_sha256']:
        raise ValueError('libxposed AAR does not match the pinned API-102 artifact')
    manifest_path = ROOT / 'app/AndroidManifest.xml'
    manifest_tree = ET.parse(manifest_path).getroot()
    application = manifest_tree.find('application')
    if (manifest_tree.get('package') != MODULE_CLASS.rsplit('.', 1)[0]
            or application is None or len(application)):
        raise ValueError('module manifest must have no standalone components')

    graph = make_module_graph()
    entry = graph['function']
    target = jvm_classfile_general_target()
    metadata = libxposed_module_semantics(LibxposedModuleDescription(
        min_api_version=102, target_api_version=102, static_scope=True,
        java_entries=(MODULE_CLASS,), scopes=(YOUTUBE,)))
    # Project-owned ABI lowering: one API-102 lifecycle method forwards its
    # exact receiver/parameter to the verified XAX function. No feature logic.
    abi = semantic_target(b'youtubehideads-managed-module-forwarder-v2\0AdBindings.values:[Ljava/lang/Object;\0onPackageReady\0'
                          + MODULE_CLASS.encode())
    module = object_with_refs(Kind.MODULE, (entry, target, metadata, abi))
    root = object_with_refs(Kind.PROGRAM_ROOT, (module,))
    objects = root_reachable_closure(root, (*graph['objects'], target, metadata, abi, module, root))
    store = write_store(root.cid, objects)
    reader = StoreReader(store)
    verify_store(reader)
    image = compile_jvm_bound_target(reader, entry.cid, target)
    (output / 'module.xax-store').write_bytes(store)
    (output / 'module-runtime.jar').write_bytes(image.jar)
    callback_descriptor = f'(L{API}XposedInterface;L{API}XposedModuleInterface$PackageReadyParam;)V'
    if (entry.cid, image.entry_method, callback_descriptor) not in image.methods:
        raise ValueError('module XAX entry does not match the fixed libxposed forwarding ABI')
    forward = DexAssembledMethod('onPackageReady',
        DexProto('V', (f'L{API}XposedModuleInterface$PackageReadyParam;',)), 2, (
            DexInstruction('invoke-static', (0, 1), DexMethodRef('L' + image.class_name + ';', image.entry_method,
                DexProto('V', (f'L{API}XposedInterface;', f'L{API}XposedModuleInterface$PackageReadyParam;')))),
            DexInstruction('return-void'),
        ))
    wrapper = emit_dex039_bridge(DexBridgeSpec('L' + MODULE_CLASS.replace('.', '/') + ';',
        f'L{API}XposedModule;', assembled_methods=(forward,)))
    view = inspect_dex_references(wrapper)
    if len(view.classes) != 1 or view.classes[0].superclass != f'L{API}XposedModule;':
        raise ValueError('invalid generated module entrypoint')

    policies = output / 'policies'
    build_router(policies)
    verify_router(policies / 'brainfuck-router.jar', policies / 'router.json')
    api_jar = output / 'libxposed-api-compile-only.jar'
    with zipfile.ZipFile(api_aar) as archive:
        api_jar.write_bytes(archive.read('classes.jar'))
    build_tools = sdk / 'build-tools/36.0.0'
    android_jar = sdk / 'platforms/android-37.0/android.jar'
    java, keytool = (java_home / 'bin' / (name + '.exe') for name in ('java', 'keytool'))

    def run(command):
        result = subprocess.run([str(value) for value in command], capture_output=True, text=True, timeout=120)
        if result.stderr:
            with (output / 'sdk-diagnostics.log').open('a', encoding='utf-8') as log:
                log.write(result.stderr)
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)
        return result.stdout.strip()

    dex_out = output / 'dex'
    dex_out.mkdir(exist_ok=True)
    # Only this builder's previous D8 outputs are replaced.
    for path in dex_out.glob('classes*.dex'):
        path.unlink()
    from .ad_build import ad_dependencies
    dependencies, native, ad_evidence = ad_dependencies(output, Path.home() / '.gradle/caches/modules-2/files-2.1')
    run((java, '-cp', build_tools / 'lib/d8.jar', 'com.android.tools.r8.D8', '--release', '--min-api', '28',
         '--lib', android_jar, '--lib', api_jar, '--output', dex_out,
         output / 'module-runtime.jar', policies / 'brainfuck-router.jar', *dependencies))
    base = output / 'manifest.apk'
    run((build_tools / 'aapt2.exe', 'link', '--manifest', manifest_path,
         '-I', android_jar, '-o', base))
    with zipfile.ZipFile(base) as archive:
        manifest = archive.read('AndroidManifest.xml')
    entries = [ApkEntry('AndroidManifest.xml', manifest), ApkEntry('classes.dex', wrapper)]
    from .link_d8 import collect_d8_outputs
    for index, data in enumerate(collect_d8_outputs(dex_out), 2):
        entries.append(ApkEntry(f'classes{index}.dex', data))
    entries.extend(ApkEntry(name, data) for name, data in emit_libxposed_metadata(metadata).items())
    entries.extend(ApkEntry(name, data, 16384) for name, data in native)
    unsigned = output / 'YouTubeHideAds-unsigned.apk'
    unsigned.write_bytes(build_apk(entries))
    vector = check_vector_module_apk(unsigned.read_bytes(), LibxposedApiTable(pin))
    if not vector.accepted:
        raise ValueError(f'libxposed module contract rejected: {vector.violations}')
    key = output / 'debug.keystore'
    if not key.exists():
        run((keytool, '-genkeypair', '-keystore', key, '-alias', 'androiddebugkey', '-storepass', 'android',
             '-keypass', 'android', '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000',
             '-dname', 'CN=Android Debug,O=Android,C=US'))
    apk = output / 'YouTubeHideAds-debug.apk'
    run((java, '-jar', build_tools / 'lib/apksigner.jar', 'sign', '--ks', key,
         '--ks-key-alias', 'androiddebugkey', '--ks-pass', 'pass:android', '--key-pass', 'pass:android',
         '--out', apk, unsigned))
    run((java, '-jar', build_tools / 'lib/apksigner.jar', 'verify', '--verbose', apk))
    report = {'status': 'MODULE_BUILT', 'xax_commit': XAX_COMMIT,
              'module_class': MODULE_CLASS, 'scope': [YOUTUBE], 'launcher_activity': False,
              'xax_class': image.class_name, 'xax_entry': image.entry_method,
              'store_root': root.cid.hex(), 'store_sha256': hashlib.sha256(store).hexdigest(),
              'apk': str(apk), 'apk_sha256': hashlib.sha256(apk.read_bytes()).hexdigest(),
              'api_aar_sha256': api_digest, 'vector_contract_accepted': vector.accepted,
              'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
              'lifecycle_adapter': 'PROJECT_DEX_FORWARDER_TO_CANONICAL_XAX',
              'signing': 'LOCAL_DEBUG_KEY', 'youtube_device_tested': False,
              'advertisement_hooks': True, 'ad_hook_families': ['video_activation', 'player_ad_layout', 'components', 'premium_offer', 'fullscreen_dialog'],
              'ad_runtime_evidence': ad_evidence, 'sponsorblock': False}
    (output / 'build-result.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xax-source', type=Path, required=True)
    parser.add_argument('--java-home', type=Path, required=True)
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--api-aar', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=ROOT / 'build/module')
    args = parser.parse_args()
    print(json.dumps(build_module(args.xax_source, args.out, args.java_home, args.sdk, args.api_aar), indent=2))


if __name__ == '__main__':
    main()
