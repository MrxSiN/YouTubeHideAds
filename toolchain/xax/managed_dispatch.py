"""Build a canonical XAX managed call to the source-attested BF router."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from .smoke_build import require_pinned_checkout
from .store_evidence import root_reachable_closure
from .router_call_plan import ROUTER_CLASS, ROUTER_METHOD, ROUTER_SIGNATURE
from toolchain.brainfuck.router import verify_router
from scripts.probe_android_integration import XAX_COMMIT


def build_dispatch(checkout: Path, policies: Path, output: Path) -> dict:
    (output / 'evidence.json').unlink(missing_ok=True)
    checkout = require_pinned_checkout(checkout)
    verify_router(policies / 'brainfuck-router.jar', policies / 'router.json')
    # The upstream checkout tracks .pyc files; imports must not dirty its pin.
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(checkout / 'compiler/src'))
    from xax_compiler import (Kind, Operation, StoreReader, jvm_classfile_general_target,
        object_with_refs, opaque_identity_type, verify_store, write_store)
    from xax_graph_builder import GraphBuilder
    from xax_jvm import compile_jvm_bound_target, jvm_reference_type, jvm_static

    array = jvm_reference_type(b'[B')
    router = jvm_static(ROUTER_CLASS.encode(), (ROUTER_METHOD + ROUTER_SIGNATURE).encode(),
                        (array,), (array,))
    graph = GraphBuilder()
    block = graph.block(array)
    block.ret(block.op1(Operation.CALL_FOREIGN, block.params, array, entity=router))
    entry = graph.function((array,), (array,))
    target = jvm_classfile_general_target()
    module = object_with_refs(Kind.MODULE, (entry, target))
    root = object_with_refs(Kind.PROGRAM_ROOT, (module,))
    objects = root_reachable_closure(root, (*graph.objects.values(),
        opaque_identity_type(b'jvm-ref:[B'), target, module, root))
    store = write_store(root.cid, objects)
    reader = StoreReader(store)
    verify_store(reader)
    image = compile_jvm_bound_target(reader, entry.cid, target)
    output.mkdir(parents=True, exist_ok=True)
    files = {'dispatch.xax-store': store, 'dispatch.jar': image.jar}
    for name, data in files.items():
        (output / name).write_bytes(data)
    report = {'status': 'XAX_MANAGED_DISPATCH_COMPILED', 'xax_commit': XAX_COMMIT,
              'store_root': root.cid.hex(), 'function_cid': entry.cid.hex(),
              'class_name': image.class_name.replace('/', '.'),
              'method': image.entry_method, 'descriptor': ROUTER_SIGNATURE,
              'invocation': 'JVM_INVOKESTATIC', 'target_class': ROUTER_CLASS,
              'target_method': ROUTER_METHOD + ROUTER_SIGNATURE,
              'bf_router_sha256': hashlib.sha256((policies / 'brainfuck-router.jar').read_bytes()).hexdigest(),
              'artifacts': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
              'compiler_execution': 'UPSTREAM_BOOTSTRAP', 'android_executed': False,
              'jni_required': False, 'youtube_hooks': False}
    (output / 'evidence.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xax-source', type=Path, required=True)
    parser.add_argument('--policies', type=Path, default=Path('generated'))
    parser.add_argument('--out', type=Path, default=Path('build/xax-managed-dispatch'))
    args = parser.parse_args()
    print(json.dumps(build_dispatch(args.xax_source, args.policies, args.out), indent=2))


if __name__ == '__main__':
    main()
