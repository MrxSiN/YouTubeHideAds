"""Fail-closed canonical-store evidence for opt-in, external XAX graph research.

This module is build tooling, never an Android feature host. Constructing
SemanticObjects is not an executed JNI call or an installable APK. Only an
actual pinned XAX store writer and verifier can establish this structural
milestone. Do not emit a success report when graph dependency closure fails.
"""
from __future__ import annotations

import hashlib


class GraphClosureError(RuntimeError):
    pass


def object_closure(objects):
    """Deduplicate by CID and require all XAX reference dependencies present."""
    indexed = {}
    for obj in objects:
        if obj.cid in indexed and indexed[obj.cid] != obj:
            raise GraphClosureError('XAX_CID_OBJECT_CONFLICT:' + obj.cid.hex())
        indexed[obj.cid] = obj
    missing = {reference for obj in indexed.values() for reference in obj.references
               if reference not in indexed}
    if missing:
        raise GraphClosureError('XAX_MISSING_REFERENCE_CIDS:' + ','.join(
            item.hex() for item in sorted(missing)))
    return tuple(indexed[cid] for cid in sorted(indexed))


def root_reachable_closure(root, objects):
    """Exact canonical root-reachable closure (reject missing/conflicting objects).

    Graph constructors can offer auxiliary helper contracts not referenced by
    the entry graph. Do not write such unreachable objects to a canonical store.
    Walk CIDs without substituting or fabricating any semantic dependencies.
    """
    indexed = {}
    for obj in objects:
        if obj.cid in indexed and indexed[obj.cid] != obj:
            raise GraphClosureError('XAX_CID_OBJECT_CONFLICT:' + obj.cid.hex())
        indexed[obj.cid] = obj
    if root.cid not in indexed or indexed[root.cid] != root:
        raise GraphClosureError('XAX_ROOT_NOT_PRESENT')
    reachable = {}
    pending = [root.cid]
    while pending:
        cid = pending.pop()
        if cid in reachable:
            continue
        obj = indexed.get(cid)
        if obj is None:
            raise GraphClosureError('XAX_MISSING_REACHABLE_REFERENCE:' + cid.hex())
        reachable[cid] = obj
        pending.extend(obj.references)
    return tuple(reachable[cid] for cid in sorted(reachable))



def require_composed_edges(router, guard, composed):
    """Reject disconnected semantic call graphs before invoking XAX writer.

    This only checks content-addressed references. XAX's real graph verifier
    must still establish CALL_DIRECT operand types and proof/effect linearity.
    """
    targets = (router['function'].cid, guard['function'].cid)
    if targets[0] == targets[1] or not set(targets).issubset(set(composed['graph'].references)):
        raise GraphClosureError('XAX_COMPOSED_DISPATCH_CALL_EDGES_MISSING')

def verify_canonical_graph_store(*graph_reports):
    """Write/read/verify one canonical XAX store containing four subroutines and the composed caller.

    This is a real external-toolchain check; there are no substituted encoders
    or hardcoded fake CIDs. The generated binary store has no Android host
    export and is never mislabeled as an APK.
    """
    if len(graph_reports) != 5:
        raise ValueError('XAX_FIVE_GRAPHS_REQUIRED')
    loader, method, router, guard, composed = graph_reports
    require_composed_edges(router, guard, composed)
    from xax_compiler import (Kind, object_with_refs, write_store,
                              StoreReader, verify_store)
    functions = tuple(item['function'] for item in graph_reports)
    module = object_with_refs(Kind.MODULE, functions)
    root = object_with_refs(Kind.PROGRAM_ROOT, (module,))
    all_objects = [module, root]
    for report in graph_reports:
        all_objects.extend(report['objects'])
        all_objects.extend((report['graph'], report['function']))
    closed = root_reachable_closure(root, all_objects)
    data = write_store(root.cid, closed)
    verify_store(StoreReader(data))
    return {
        'status': 'XAX_CANONICAL_GRAPH_STORE_VERIFIED_ONLY',
        'root_cid': root.cid.hex(),
        'object_count': len(closed),
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'binary': data,
        'android_compiled': False,
        'android_executed': False,
    }
