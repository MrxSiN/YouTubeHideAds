"""Pinned XAX JNI typed-call *plan* for the actual BF dispatcher.

This is a semantic type/ABI capability check, NOT an XAX graph or an Android
implementation. Source verified against MrxSiN/XAX at the pinned revision,
compiler/src/xax_jni.py. No hand-written Java/C source is used as application
logic; the separate tests/jni harness exercises the exact JNI functions on a
JVM while the canonical Android XAX executable graph remains blocked.
"""
from __future__ import annotations

from dataclasses import dataclass

from toolchain.brainfuck.router import ROUTER_CLASS

ROUTER_METHOD = 'run'
ROUTER_SIGNATURE = '([B)[B'
ROUTER_CLASS_DESCRIPTOR = 'L' + ROUTER_CLASS + ';'
# Module classes are defined by the module classloader. Primitive arrays have
# bootstrap type identity; never use boot classloader to look up the BF class.
BF_MODULE_LOADER = b'module:youtubehideads'
PRIMITIVE_ARRAY_LOADER = b'android.boot'


@dataclass(frozen=True)
class RouterCallIdentity:
    owner: str = ROUTER_CLASS
    method: str = ROUTER_METHOD
    signature: str = ROUTER_SIGNATURE
    module_loader: bytes = BF_MODULE_LOADER
    input_loader: bytes = PRIMITIVE_ARRAY_LOADER

    def __post_init__(self):
        if (self.owner, self.method, self.signature, self.module_loader, self.input_loader) != (
            ROUTER_CLASS, ROUTER_METHOD, ROUTER_SIGNATURE,
            BF_MODULE_LOADER, PRIMITIVE_ARRAY_LOADER
        ):
            raise ValueError('ROUTER_JNI_ABI_FROZEN')


def make_xax_call_plan():
    """Ask *upstream XAX* to build the JNI-typed method/call/stack-pack carriers.

    Does NOT claim to resolve the BF class at runtime. The caller still needs
    a loader-correct class lookup, exception-aware success branching, local-ref cleanup,
    an XAX graph using these objects, and verified framework attachment.
    """
    try:
        from xax_jni import (
            JniReferenceKind, JniReferenceArgumentSpec, jni_method_call_plan,
            jni_get_static_method_id_contract, jni_argument_pack_plan,
            jni_stack_method_call_contract,
        )
    except ImportError as error:
        raise RuntimeError('PINNED_XAX_COMPILER_NOT_IMPORTED') from error
    identity = RouterCallIdentity()
    argument = JniReferenceArgumentSpec(
        '[B', kind=JniReferenceKind.BORROWED,
        loader_domain=identity.input_loader, nullable=False,
    )
    call = jni_method_call_plan(
        identity.owner, identity.method, identity.signature,
        dispatch='static', loader_domain=identity.module_loader,
    )
    pack = jni_argument_pack_plan(
        identity.signature, reference_arguments=(argument,),
        expected_reference_loader_domains=(identity.input_loader,),
    )
    method_id = jni_get_static_method_id_contract(
        JniReferenceKind.LOCAL,
        owner=identity.owner, name=identity.method,
        descriptor=identity.signature, loader_domain=identity.module_loader,
    )
    call_contract = jni_stack_method_call_contract(
        call, pack, class_kind=JniReferenceKind.LOCAL,
        track_exception_state=True,
    )
    if call.function_name != 'CallStaticObjectMethodA' or pack.total_bytes != 8:
        raise RuntimeError('XAX_JNI_CALL_PLAN_MISMATCH')
    return {
        'owner': identity.owner,
        'signature': identity.signature,
        'jni_operation': call.function_name,
        'jvalue_bytes': pack.total_bytes,
        'method_id_contract': method_id,
        'call_contract': call_contract,
        'method_plan': call,
        'argument_pack': pack,
        'xax_graph_built': False,
        'android_executed': False,
    }


def make_xax_bound_router_call_graph(*, return_exception_status=True):
    """Author a genuine XAX graph for a *pre-resolved* class and static method ID.

    The function is an internal semantic subroutine, not a runnable Android JNI
    export. Its caller MUST supply a valid loader-qualified local jclass,
    its live owner token, and the exact resolved typed jmethodID; a resolver
    and an exception-aware return adapter are still required. This graph
    calls CallStaticObjectMethodA, threads ownership/effects, and ends its
    stack allocation. It MUST NOT be emitted as a deployable callback yet.
    """
    from xax_compiler import (
        Block, Kind, Node, Operation, Terminator, ValueRef,
        android_arm64_shared_target, function, graph_fragment,
        bits_type, memory_effect_type, stack_owner_type,
    )
    from xax_jni import (
        JniReferenceKind, jni_class_reference_type, jni_env_pointer_type,
        jni_exception_state_type, JniExceptionState, jni_memory_effect_type,
        jni_reference_type, jni_reference_owner_type,
        jni_env_table_load_node, jni_native_function_load_node,
        jni_argument_pack_nodes, jni_exception_check_state_contract,
        jni_type_objects,
    )

    plan = make_xax_call_plan()
    target = android_arm64_shared_target()
    method = plan['method_plan']
    pack_plan = plan['argument_pack']
    contract = plan['call_contract']
    identity = RouterCallIdentity()
    env = jni_env_pointer_type()
    clazz = jni_class_reference_type(JniReferenceKind.LOCAL,
        owner=identity.owner, loader_domain=identity.module_loader)
    clazz_owner = jni_reference_owner_type(JniReferenceKind.LOCAL)
    input_array = jni_reference_type(JniReferenceKind.BORROWED, b'[B',
        loader_domain=identity.input_loader, nullable=False)
    clean = jni_exception_state_type(JniExceptionState.CLEAN)
    maybe = jni_exception_state_type(JniExceptionState.MAYBE_PENDING)
    jni_effect = jni_memory_effect_type()
    arguments = (env, clazz, clazz_owner, method.method_id_type,
                 input_array, clean, jni_effect)

    prefix = (
        jni_env_table_load_node(target, ValueRef.parameter(0, 0), ValueRef.parameter(0, 6)),
        jni_native_function_load_node(
            target, ValueRef.node_result(0, 0, 0), ValueRef.node_result(0, 0, 1),
            method.function_name,
        ),
    )
    pack = jni_argument_pack_nodes(pack_plan, (ValueRef.parameter(0, 4),),
                                   target=target, start_node_index=len(prefix))
    call_index = len(prefix) + len(pack.nodes)
    call_result_types = (*method.result_types, clazz_owner, maybe,
                         stack_owner_type(), memory_effect_type(), jni_effect)
    call = Node(Operation.CALL_INDIRECT,
        (ValueRef.node_result(0, 1, 0), ValueRef.parameter(0, 0),
         ValueRef.parameter(0, 1), ValueRef.parameter(0, 2),
         ValueRef.parameter(0, 3), pack.pointer, ValueRef.parameter(0, 5),
         pack.owner, pack.effect, ValueRef.node_result(0, 1, 1)),
        call_result_types, entity=contract)
    end = Node(Operation.STACK_END,
        (ValueRef.node_result(0, call_index, 4),
         ValueRef.node_result(0, call_index, 5)), ())
    # An indirect JNI call can leave a pending Java exception. Query its
    # status instead of presenting the result as an unconditional success.
    # This subroutine RETURNS that status to its caller, which must branch
    # before using the (possibly null) result. It does not clear exceptions.
    check_contract = jni_exception_check_state_contract()
    exception_load_index = call_index + 2  # call followed by STACK_END
    exception_load = jni_native_function_load_node(
        target, ValueRef.node_result(0, 0, 0),
        ValueRef.node_result(0, call_index, 6), 'ExceptionCheck')
    check_index = exception_load_index + 1
    checked = Node(Operation.CALL_INDIRECT,
        (ValueRef.node_result(0, exception_load_index, 0),
         ValueRef.parameter(0, 0), ValueRef.node_result(0, call_index, 3),
         ValueRef.node_result(0, exception_load_index, 1)),
        (bits_type(8), maybe, jni_effect), entity=check_contract)
    # The Android backend permits one machine return; that export's test caller
    # reads live JNI exception state instead of receiving a second status value.
    status_types = (bits_type(8),) if return_exception_status else ()
    status_values = (ValueRef.node_result(0, check_index, 0),) if return_exception_status else ()
    result_types = (*method.result_types, clazz_owner, *status_types, maybe, jni_effect)
    output_values = (
        *(ValueRef.node_result(0, call_index, i) for i in (0, 1, 2)),
        *status_values,
        *(ValueRef.node_result(0, check_index, i) for i in (1, 2)),
    )
    fragment = graph_fragment((Block(arguments,
        tuple(prefix) + pack.nodes + (call, end, exception_load, checked),
        Terminator.return_(output_values)),))
    routine = function(fragment, arguments, result_types)
    type_closure = jni_type_objects(
        reference_specs=(
            (JniReferenceKind.LOCAL, identity.owner.replace('/', '.').encode(), identity.module_loader),
            (JniReferenceKind.BORROWED, b'[B', identity.input_loader, False),
            (JniReferenceKind.LOCAL, b'[B'),
        ),
        method_specs=((identity.owner, identity.method, identity.signature,
                       True, identity.module_loader),),
    )
    objects = {obj.cid: obj for obj in (
        target, fragment, routine, contract, check_contract, plan['method_id_contract'],
        *pack.semantic_objects, *type_closure,
    )}
    return {
        'graph': fragment,
        'function': routine,
        'objects': tuple(objects[cid] for cid in sorted(objects)),
        'operation': method.function_name,
        'class_resolution_executed': False,
        'jni_exception_check_present': True,
        'exception_status_returned': return_exception_status,
        'pending_exception_handled': False,
        'android_execution_verified': False,
        'exported_as_android_callback': False,
    }
