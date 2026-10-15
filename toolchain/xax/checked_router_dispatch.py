"""XAX-only *composed* JNI router invocation with a derived exception gate.

The existing router-call subroutine returns ``ExceptionCheck`` as a byte. The
existing five-condition safety gate deliberately rejects any status other than
exactly one. Here a direct XAX call carries the real router exception status
into that gate: ``ExceptionCheck == 0`` is converted to the gate's first input.
The other four conditions are still explicitly supplied and MUST be established
by a real module runtime, not by hardcoded values.

This is NOT an Android callback. It has a pre-resolved typed jclass/method ID,
no verified app classloader, no frame validator, and no lifecycle/hook/seek.
It must only be considered structurally verified after running the pinned XAX
compiler's canonical writer/verifier; the off-device oracle below is not that.
"""
from __future__ import annotations

from .dispatch_guard import CONDITIONS, reference_dispatch_gate
from .router_call_plan import RouterCallIdentity

EXTERNAL_PROOFS = CONDITIONS[1:]


def reference_invocation_gate(exception_check: int, external_flags: tuple[int, ...]) -> int:
    """Off-device test oracle for the exact *composition*, no feature decision.

    JNI ExceptionCheck convention: zero means no pending exception. A result
    with a pending exception (nonzero) MUST NOT authorize use of the returned
    byte array even if every externally supplied proof is true.
    """
    if (type(exception_check) is not int or not 0 <= exception_check <= 255
            or type(external_flags) is not tuple or len(external_flags) != len(EXTERNAL_PROOFS)
            or any(type(v) is not int or not 0 <= v <= 255 for v in external_flags)):
        raise ValueError('XAX_INVOCATION_GATE_INVALID_INPUT')
    return reference_dispatch_gate((int(exception_check == 0), *external_flags))


def make_xax_checked_router_dispatch_graph(router: dict, guard: dict) -> dict:
    """Compose upstream XAX ``CALL_DIRECT`` edges, type effects and owners.

    Inputs: the existing router call's seven typed inputs, then four host proof
    bytes (binary class name, defining loader, nonnull method ID, reply frame).
    Outputs: the guard bit, the (untrusted unless bit is 1) local byte-array
    reference, its local owner, the input class owner, exception state, and JNI
    effect.  The XAX return retains every proof token, never silently drops it.

    The host MUST branch on the returned gate bit BEFORE inspecting the array.
    No native hook or Android method is emitted by this construction function.
    """
    from xax_compiler import IntCompare, Operation, bits_type
    from xax_graph_builder import GraphBuilder
    from xax_jni import (
        JniReferenceKind, JniExceptionState, jni_class_reference_type,
        jni_env_pointer_type, jni_exception_state_type, jni_memory_effect_type,
        jni_reference_type, jni_reference_owner_type, jni_typed_method_id_type,
        jni_type_objects,
    )
    identity = RouterCallIdentity()
    b8, b1 = bits_type(8), bits_type(1)
    env = jni_env_pointer_type()
    clazz = jni_class_reference_type(JniReferenceKind.LOCAL,
        owner=identity.owner, loader_domain=identity.module_loader)
    local_owner = jni_reference_owner_type(JniReferenceKind.LOCAL)
    method_id = jni_typed_method_id_type(identity.owner, identity.method,
        identity.signature, is_static=True, loader_domain=identity.module_loader)
    request = jni_reference_type(JniReferenceKind.BORROWED, b'[B',
        loader_domain=identity.input_loader, nullable=False)
    clean = jni_exception_state_type(JniExceptionState.CLEAN)
    maybe = jni_exception_state_type(JniExceptionState.MAYBE_PENDING)
    external_effect = jni_memory_effect_type()
    result_array = jni_reference_type(JniReferenceKind.LOCAL, b'[B')
    # Match make_xax_bound_router_call_graph's precise interface. In particular,
    # the input class owner and result owner must flow through the call intact.
    call_parameters = (env, clazz, local_owner, method_id, request, clean, external_effect)
    call_results = (result_array, local_owner, local_owner, b8, maybe, external_effect)
    inputs = (*call_parameters, *(b8 for _ in EXTERNAL_PROOFS))
    outputs = (b8, result_array, local_owner, local_owner, maybe, external_effect)

    builder = GraphBuilder()
    block = builder.block(*inputs)
    returned = block.op(Operation.CALL_DIRECT, block.params[:7], call_results,
                        entity=router['function'])
    no_exception = block.op1(Operation.INT_COMPARE,
        (returned[3], block.const(b8, 0)), b1, attributes=(IntCompare.EQ,))
    clear = block.op1(Operation.INT_ZERO_EXTEND, (no_exception,), b8)
    allowed = block.op1(Operation.CALL_DIRECT,
        (clear, *block.params[7:]), b8, entity=guard['function'])
    block.ret(allowed, returned[0], returned[1], returned[2], returned[4], returned[5])
    function = builder.function(inputs, outputs)
    graph = next(o for o in builder.objects.values()
                 if o.cid in function.references and o.kind.name == 'GRAPH_FRAGMENT')
    closure = jni_type_objects(
        reference_specs=((JniReferenceKind.LOCAL, identity.owner.replace('/', '.').encode(),
                          identity.module_loader),
                         (JniReferenceKind.BORROWED, b'[B', identity.input_loader, False),
                         (JniReferenceKind.LOCAL, b'[B')),
        method_specs=((identity.owner, identity.method, identity.signature,
                       True, identity.module_loader),),
    )
    objects = {o.cid: o for o in (*builder.objects.values(), *closure)}
    # The *actual* semantic graph must carry these direct-call dependencies.
    expected = {router['function'].cid, guard['function'].cid}
    if not expected.issubset(set(graph.references)):
        raise RuntimeError('XAX_COMPOSED_DIRECT_CALL_EDGE_MISSING')
    return {
        'graph': graph, 'function': function,
        'objects': tuple(objects[k] for k in sorted(objects)),
        'direct_call_targets': (router['function'].cid.hex(), guard['function'].cid.hex()),
        'jni_exception_status_derived_from_call': True,
        'other_proofs_untrusted': EXTERNAL_PROOFS,
        'class_provenance_implemented': False,
        'android_callback_exported': False,
        'android_execution_verified': False,
    }
