"""Build a separate XAX byte-array JNI smoke DEX/library, with no app hooks."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from .managed_transport import make_semantics, TRANSPORT_DESCRIPTOR, TRANSPORT_METHOD
from .smoke_build import require_pinned_checkout
from .store_evidence import root_reachable_closure
from .router_call_plan import make_xax_bound_router_call_graph
from .dex_methods import inspect_methods
from scripts.probe_android_integration import XAX_COMMIT


def build_transport(checkout: Path, output: Path) -> dict:
    checkout = require_pinned_checkout(checkout)
    (output / 'evidence.json').unlink(missing_ok=True)
    sys.path.insert(0, str(checkout / 'compiler/src'))
    from xax_android import compile_android_shared, inspect_android_elf
    from xax_android_managed import lower_android_managed_class
    from xax_compiler import (Kind, StoreReader, android_arm64_shared_target, android_export_symbol,
                              object_with_refs, verify_store, write_store)
    from xax_dex import emit_dex039_bridge

    transport = make_semantics()
    router = make_xax_bound_router_call_graph(return_exception_status=False)
    router_export = android_export_symbol(router['function'], b'youtubehideads_xax_router_call')
    target = android_arm64_shared_target()
    module = object_with_refs(Kind.MODULE, (transport['callback'], transport['export'],
                                           transport['carrier'], router['function'], router_export, target))
    root = object_with_refs(Kind.PROGRAM_ROOT, (module,))
    objects = root_reachable_closure(root, (*transport['objects'], *router['objects'],
                                          router_export, target, module, root))
    store = write_store(root.cid, objects)
    reader = StoreReader(store)
    verify_store(reader)
    shared = compile_android_shared(reader, (transport['export'], router_export),
                                    target_object=target, soname=b'libxaxapp.so')
    dex = emit_dex039_bridge(lower_android_managed_class(transport['carrier']))
    methods = inspect_methods(dex, required_classes={TRANSPORT_DESCRIPTOR})
    if not methods[TRANSPORT_DESCRIPTOR].get(TRANSPORT_METHOD, {}).get('code_units'):
        raise ValueError('XAX_TRANSPORT_FORWARDER_MISSING')
    inspect_android_elf(shared.data)
    output.mkdir(parents=True, exist_ok=True)
    artifacts = {'transport.xax-store': store, 'classes.dex': dex, 'libxaxapp.so': shared.data}
    for name, content in artifacts.items():
        (output / name).write_bytes(content)
    report = {'status': 'XAX_TRANSPORT_COMPILED', 'xax_commit': XAX_COMMIT,
              'store_root': root.cid.hex(), 'class': TRANSPORT_DESCRIPTOR,
              'method': TRANSPORT_METHOD, 'jni_export': transport['jni_symbol'],
              'router_export': 'youtubehideads_xax_router_call',
              'router_requires_pre_resolved_class_and_method': True,
              'router_exception_status': 'CALLER_CHECKS_LIVE_JNI_STATE',
              'artifacts': {name: hashlib.sha256(data).hexdigest() for name, data in artifacts.items()},
              'compiler_execution': 'UPSTREAM_BOOTSTRAP',
              'android_executed': False, 'brainfuck_invoked': False,
              'apk_built': False, 'youtube_hooks': False,
              'redistribution_authorized': False}
    (output / 'evidence.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xax-source', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path('build/xax-transport'))
    args = parser.parse_args()
    print(json.dumps(build_transport(args.xax_source, args.out), indent=2))


if __name__ == '__main__':
    main()
