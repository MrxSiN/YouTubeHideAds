"""XAX semantic dispatcher safety gate; *not* an Android callback.

This is platform-integrity routing, NOT application classification.  The guard
receives independently proven JNI/loader conditions and denies a router action
unless each required condition is satisfied.  The caller must actually obtain
those proofs; passing literal `1` values does not establish provenance.

Source form uses only the pinned XAX semantic graph constructors (GraphBuilder),
never a text-based XAX dialect or a handwritten application bridge.  Until the
external XAX checkout constructs and verifies it, this remains uncompiled XAX
construction source, not an executable platform gate.
"""
from __future__ import annotations

CONDITIONS = (
    'jni_exception_clear',
    'class_binary_name_verified',
    'defining_loader_verified',
    'method_id_nonnull_verified',
    'result_frame_verified',
)


def reference_dispatch_gate(flags: tuple[int, ...]) -> int:
    """OFF-DEVICE test oracle for the XAX routing gate (no feature policy)."""
    if len(flags) != len(CONDITIONS) or any(type(x) is not int or not 0 <= x <= 255 for x in flags):
        raise ValueError('DISPATCH_GUARD_INVALID_INPUT')
    return int(all(x == 1 for x in flags))


def make_xax_dispatch_guard_graph() -> dict:
    """Build a genuine XAX five-stage, fail-closed conditional control flow.

    Each input is one JNI-boundary proof status in {0,1}.  The XAX graph requires
    EXACTLY 1 for each, rejecting 2..255 as well as zero.  An exception still
    pending MUST enter as `jni_exception_clear=0`; the caller cannot treat a
    previously observed status as a proof for a subsequent JNI invocation.
    This routine produces a narrow 'may-use-validated-reply' bit; it performs
    no player action or ad classifier computation.
    """
    from xax_compiler import IntCompare, Operation, bits_type
    from xax_graph_builder import GraphBuilder

    b8 = bits_type(8)
    b1 = bits_type(1)
    builder = GraphBuilder()
    checks = [builder.block(*(b8,) * len(CONDITIONS))]
    # No fall-through by default; all bad values converge to denied.
    denied = builder.block()
    approved = builder.block()
    for index in range(1, len(CONDITIONS)):
        checks.append(builder.block(*(b8,) * len(CONDITIONS)))
    for index, block in enumerate(checks):
        is_one = block.op1(Operation.INT_COMPARE,
            (block.params[index], block.const(b8, 1)),
            b1, attributes=(IntCompare.EQ,))
        if index + 1 < len(checks):
            block.cbr(is_one, checks[index + 1], block.params, denied, ())
        else:
            block.cbr(is_one, approved, (), denied, ())
    denied.ret(denied.const(b8, 0))
    approved.ret(approved.const(b8, 1))
    routine = builder.function((b8,) * len(CONDITIONS), (b8,))
    # `GraphBuilder` tracks every node's types and constants, and the produced
    # graph/function. No ad-policy branch exists in this routine.
    graph = next(obj for obj in builder.objects.values()
                 if obj.cid in routine.references and obj.kind.name == 'GRAPH_FRAGMENT')
    objects = tuple(builder.objects[cid] for cid in sorted(builder.objects))
    return {
        'graph': graph,
        'function': routine,
        'objects': objects,
        'ordered_conditions': CONDITIONS,
        'untrusted_caller_conditions': True,
        'exception_dependent_branch_present': True,
        'classloader_provenance_implemented': False,
        'android_exported': False,
        'android_execution_verified': False,
    }
