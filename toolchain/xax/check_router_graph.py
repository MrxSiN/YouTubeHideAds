"""Opt-in external XAX semantic JNI graph probe; never emits/deploys an APK.

The XAX checkout is external and MUST match our frozen revision. Tests/jni is
only a desktop ABI oracle and never enters this graph or the Android build.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from toolchain.xax.smoke_build import require_pinned_checkout, XAXUnavailable
from toolchain.xax.router_call_plan import make_xax_bound_router_call_graph
from toolchain.xax.loader_resolution import make_xax_bound_loader_call_graph
from toolchain.xax.static_method_resolution import make_xax_bound_static_method_resolution_graph
from toolchain.xax.store_evidence import verify_canonical_graph_store, GraphClosureError
from toolchain.xax.dispatch_guard import make_xax_dispatch_guard_graph
from toolchain.xax.checked_router_dispatch import make_xax_checked_router_dispatch_graph


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--xax-source', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path('build/xax-router-call-plan.json'))
    parser.add_argument('--store', type=Path, default=None, help='Optional canonical binary XAX store output')
    args = parser.parse_args()
    try:
        pinned = require_pinned_checkout(args.xax_source)
    except XAXUnavailable as error:
        parser.exit(2, f'XAX_ROUTER_GRAPH_BLOCKED: {error}\n')
    sys.path.insert(0, str(pinned / 'compiler/src'))
    try:
        graph = make_xax_bound_router_call_graph()
        loader = make_xax_bound_loader_call_graph()
        method = make_xax_bound_static_method_resolution_graph()
        guard = make_xax_dispatch_guard_graph()
        composed = make_xax_checked_router_dispatch_graph(graph, guard)
        verified = verify_canonical_graph_store(loader, method, graph, guard, composed)
    except Exception as error:
        parser.exit(3, f'XAX_ROUTER_GRAPH_CONSTRUCTION_FAILED: {type(error).__name__}: {error}\n')
    result = {
        'status': verified['status'],
        'guard_graph_cid': guard['graph'].cid.hex(),
        'composed_graph_cid': composed['graph'].cid.hex(),
        'composed_function_cid': composed['function'].cid.hex(),
        'composed_direct_call_targets': list(composed['direct_call_targets']),
        'exception_clear_derived_from_router_call': composed['jni_exception_status_derived_from_call'],
        'composed_other_proofs_bound_to_runtime': False,
        'guard_function_cid': guard['function'].cid.hex(),
        'guard_exception_dependent_branch_present': guard['exception_dependent_branch_present'],
        'guard_proof_inputs_bound_to_runtime': False,
        'canonical_store_root_cid': verified['root_cid'],
        'canonical_store_sha256': verified['sha256'],
        'canonical_store_object_count': verified['object_count'],
        'graph_cid': graph['graph'].cid.hex(),
        'function_cid': graph['function'].cid.hex(),
        'operation': graph['operation'],
        'jni_exception_check_present': graph['jni_exception_check_present'],
        'loader_graph_cid': loader['graph'].cid.hex(),
        'loader_function_cid': loader['function'].cid.hex(),
        'loader_jni_operation': loader['jni_operation'],
        'loader_exception_check_present': loader['exception_check_present'],
        'static_method_resolution_graph_cid': method['graph'].cid.hex(),
        'static_method_resolution_function_cid': method['function'].cid.hex(),
        'static_method_resolution_exception_check_present': method['exception_check_present'],
        'static_method_resolution_exception_branch_implemented': False,
        'verified_defining_loader_required': True,
        'class_name_string_creation_implemented': False,
        'loader_class_refinement_implemented': False,
        'pre_resolved_jclass_and_jmethodid_required': True,
        'pending_exception_handled': False,
        'app_class_loader_resolution': False,
        'android_exported': False,
        'apk_built': False,
        'android_executed': False,
        'brainfuck_invoked_on_android': False,
        'test_only_c_bridge_packaged': False,
    }
    if args.store is not None:
        args.store.parent.mkdir(parents=True, exist_ok=True)
        args.store.write_bytes(verified['binary'])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
