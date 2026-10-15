"""Controlled libxposed lifecycle smoke build using a PINNED EXTERNAL XAX compiler.

Build-tool code, never part of the Android runtime. The constructed XAX objects
are canonical semantic graphs/carriers, NOT source-language text. This bounded
smoke build imports an upstream test-only Activity fixture solely to exercise
its packaging path; it does NOT implement the project manager, link Brainfuck,
or hook YouTube. Do not redistribute XAX-derived artifacts without a license
review. This module is intentionally not callable without the exact XAX checkout.

API provenance: upstream XAX @ 9e44eedfc241d25bb5062b38af105f75234000e2,
compiler/benchmarks/bench_android_libxposed_managed.py and
compiler/src/{xax_build,xax_libxposed,xax_jni,xax_manifest}.py.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from scripts.probe_android_integration import XAX_COMMIT


class XAXUnavailable(RuntimeError):
    pass


def require_pinned_checkout(path: Path) -> Path:
    path = path.resolve()
    if not (path / 'compiler/src/xax_compiler.py').is_file():
        raise XAXUnavailable('Missing XAX compiler/src; supply an external checkout')
    r = subprocess.run(['git', '-C', str(path), 'rev-parse', 'HEAD'],
                       capture_output=True, text=True, timeout=10)
    if r.returncode or r.stdout.strip() != XAX_COMMIT:
        raise XAXUnavailable('XAX git SHA does not equal documented pinned revision')
    status = subprocess.run(['git', '-C', str(path), 'status', '--porcelain'],
                            capture_output=True, text=True, timeout=10)
    if status.returncode or status.stdout.strip():
        raise XAXUnavailable('XAX checkout must be clean, including untracked sources')
    return path


def build_smoke(xax_checkout: Path, output: Path) -> dict:
    """Construct + verify a canonical XAX graph and emit a research-only APK.

    No handwritten Android Java/Kotlin/C feature code. No YouTube hooks. The
    Activity fixture comes from the pinned toolchain's own test harness and is
    *not* proposed as the production Activity implementation.
    """
    xax_checkout = require_pinned_checkout(xax_checkout)
    (output / 'lifecycle-smoke-evidence.json').unlink(missing_ok=True)
    # XAX's bootstrap is external, with compiler/ as import root for benchmarks.
    sys.path.insert(0, str(xax_checkout / 'compiler'))
    sys.path.insert(0, str(xax_checkout / 'compiler/src'))

    from benchmarks.bench_android_managed_bridge import ui_activity_fixture
    from xax_build import (ArtifactKind, build, build_profile, build_request,
                           package, resolve_packages, snapshot_store, trust_policy)
    from xax_compiler import (Block, Kind, Terminator, android_arm64_shared_target,
                              android_export_symbol, function, graph_fragment,
                              object_with_refs, write_store, StoreReader, verify_store)
    from xax_jni import (JniReferenceKind, jni_env_pointer_type,
                          jni_reference_type, jni_short_native_symbol,
                          jni_type_objects)
    from xax_libxposed import (LibxposedManagedEntryDescription,
                                LibxposedModuleDescription,
                                libxposed_managed_entry_semantics,
                                libxposed_module_semantics,
                                lower_libxposed_managed_entry)
    from xax_manifest import AndroidManifestSpec, android_manifest_semantics

    ui = ui_activity_fixture()  # external smoke-only UI; not app feature logic
    managed = libxposed_managed_entry_semantics(LibxposedManagedEntryDescription())
    spec = lower_libxposed_managed_entry(managed)
    env = jni_env_pointer_type()
    specs = (
        (JniReferenceKind.BORROWED, b'xax.generated.XaxModule', b'module:xax.generated'),
        (JniReferenceKind.BORROWED,
         b'io.github.libxposed.api.XposedModuleInterface$ModuleLoadedParam', b'libxposed:102'),
        (JniReferenceKind.BORROWED,
         b'io.github.libxposed.api.XposedModuleInterface$PackageReadyParam', b'libxposed:102'),
    )
    typed = [jni_reference_type(kind, name, loader_domain=domain)
             for kind, name, domain in specs]
    callbacks = []
    graphs = []
    exports = []
    for suffix, argument_type in (('xaxOnModuleLoaded', typed[1]),
                                  ('xaxOnPackageReady', typed[2])):
        params = (env, typed[0], argument_type)
        graph = graph_fragment((Block(params, (), Terminator.return_(())),))
        callback = function(graph, params, ())
        symbol = jni_short_native_symbol(spec.class_descriptor, suffix)
        graphs.append(graph)
        callbacks.append(callback)
        exports.append(android_export_symbol(callback, symbol))

    # No hook installation: only a controlled lifecycle smoke test.
    # A separate managed package ID is required; never impersonate YouTube.
    manifest = android_manifest_semantics(AndroidManifestSpec(
        'org.youtubehideads.module', 'xax.generated.XaxActivity',
        min_sdk=28, target_sdk=35, version_code=1, launcher=True))
    metadata = libxposed_module_semantics(LibxposedModuleDescription(
        min_api_version=101, target_api_version=102, static_scope=True,
        java_entries=('xax.generated.XaxModule',), scopes=('com.example.target',)))
    module = object_with_refs(Kind.MODULE, (
        ui['activity_callback'], ui['listener_callback'], *callbacks,
        ui['activity_export'], ui['listener_export'], *exports,
        ui['ui_semantics'], manifest, metadata, managed,
    ))
    package_root = package(b'youtubehideads-lifecycle-smoke', (module,),
                           build_entries=((b'apk', ui['activity_callback']),))
    target, profile, policy = android_arm64_shared_target(), build_profile(), trust_policy()
    request = build_request(package_root, b'apk', target, profile,
                            requested_artifacts=(ArtifactKind.ANDROID_UNSIGNED_APK,))
    objects = (*tuple(ui['reader'].objects()), *jni_type_objects(specs),
               *graphs, *callbacks, *exports, ui['activity_export'],
               ui['listener_export'], ui['ui_semantics'], manifest,
               metadata, managed, module, package_root, target, profile,
               policy, request)
    resolution = resolve_packages(request, objects, policy,
                                   b'youtubehideads-lifecycle-smoke-resolver-v1')
    reader = snapshot_store(resolution, objects)
    # Store is XAX's actual binary canonical store: never a JSON/text source stand-in.
    store_bytes = write_store(resolution.snapshot.cid, tuple(reader.objects()))
    verify_store(StoreReader(store_bytes))
    result = build(reader, request.cid)

    from .verify_apk import inspect_module_apk
    evidence = inspect_module_apk(result.artifact, mode='smoke')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'lifecycle-smoke.canonical-store').write_bytes(store_bytes)
    (output / 'lifecycle-smoke-unsigned.apk').write_bytes(result.artifact)
    report = {
        'status': 'STRUCTURAL_SMOKE_ONLY',
        'xax_commit': XAX_COMMIT,
        'source_language': 'canonical XAX semantic objects',
        'store_root': resolution.snapshot.cid.hex(),
        'store_sha256': hashlib.sha256(store_bytes).hexdigest(),
        'build_request': request.cid.hex(),
        'apk_sha256': hashlib.sha256(result.artifact).hexdigest(),
        'apk_verifier': evidence,
        'signed': False,
        'device_tested': False,
        'managed_transport_included': False,
        'brainfuck_dex_linked': False,
        'youtube_hooks': False,
        'redistribution_authorized': False,
    }
    (output / 'lifecycle-smoke-evidence.json').write_text(
        json.dumps(report, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--xax-source', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path('build/xax-smoke'))
    parser.add_argument('--local-research-only', action='store_true')
    args = parser.parse_args()
    if not args.local_research_only:
        parser.error('--local-research-only required (XAX redistribution license unresolved)')
    try:
        print(json.dumps(build_smoke(args.xax_source, args.out), indent=2))
    except XAXUnavailable as exc:
        parser.exit(2, f'XAX_BLOCKED: {exc}\n')


if __name__ == '__main__':
    main()
