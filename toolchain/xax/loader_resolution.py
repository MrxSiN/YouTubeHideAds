"""Bounded XAX typed-JNI plan and call graph for loader-correct router lookup.

Every object here is build-time XAX semantic construction. It is NOT platform
feature code and does not ship a managed Java/C fallback. An external XAX
compiler is required to build/typecheck the graph. No XAX graph in this file
claims to create a Java String, resolve ClassLoader.loadClass, refine the
returned Class to a module-scoped jclass, or handle the error branch end-to-end.

Pinned upstream basis: XAX compiler/src/xax_jni.py, JNI 1.6 call contracts.
"""
from __future__ import annotations

from dataclasses import dataclass
from .router_call_plan import ROUTER_CLASS, ROUTER_METHOD, ROUTER_SIGNATURE, BF_MODULE_LOADER, PRIMITIVE_ARRAY_LOADER

BOOT_CLASSLOADER = b'android.boot'
CLASS_LOADER_OWNER = 'java/lang/ClassLoader'
LOAD_CLASS_METHOD = 'loadClass'
LOAD_CLASS_DESCRIPTOR = '(Ljava/lang/String;)Ljava/lang/Class;'
ROUTER_BINARY_CLASS_NAME = ROUTER_CLASS.replace('/', '.')


@dataclass(frozen=True)
class LoaderResolutionIdentity:
    owner: str = CLASS_LOADER_OWNER
    method: str = LOAD_CLASS_METHOD
    descriptor: str = LOAD_CLASS_DESCRIPTOR
    class_name: str = ROUTER_BINARY_CLASS_NAME
    boot_loader: bytes = BOOT_CLASSLOADER
    router_loader: bytes = BF_MODULE_LOADER

    def __post_init__(self):
        if (self.owner, self.method, self.descriptor,
                self.class_name, self.boot_loader, self.router_loader) != (
            CLASS_LOADER_OWNER, LOAD_CLASS_METHOD, LOAD_CLASS_DESCRIPTOR,
            ROUTER_BINARY_CLASS_NAME, BOOT_CLASSLOADER, BF_MODULE_LOADER):
            raise ValueError('XAX_LOADER_RESOLUTION_IDENTITY_FROZEN')


def make_xax_loader_call_plan():
    """Use real upstream XAX to describe a virtual ClassLoader.loadClass call.

    No runtime lookup is done here; the Java String and methodID are assumed
    pre-resolved. A returned Class is generic until separately classloader-
    validated, so it cannot be silently passed as the BF router jclass.
    """
    try:
        from xax_jni import (
            JniReferenceKind, JniReferenceArgumentSpec,
            jni_method_call_plan, jni_get_method_id_contract,
            jni_argument_pack_plan, jni_stack_method_call_contract,
        )
    except ImportError as exc:
        raise RuntimeError('PINNED_XAX_COMPILER_NOT_IMPORTED') from exc
    identity = LoaderResolutionIdentity()
    arg = JniReferenceArgumentSpec('Ljava/lang/String;',
                                   kind=JniReferenceKind.BORROWED,
                                   loader_domain=identity.boot_loader,
                                   nullable=False)
    method = jni_method_call_plan(identity.owner, identity.method,
                                   identity.descriptor, dispatch='virtual',
                                   receiver_kind=JniReferenceKind.BORROWED,
                                   loader_domain=identity.boot_loader)
    pack = jni_argument_pack_plan(identity.descriptor,
        reference_arguments=(arg,),
        expected_reference_loader_domains=(identity.boot_loader,))
    resolver = jni_get_method_id_contract(
        JniReferenceKind.LOCAL, owner=identity.owner,
        name=identity.method, descriptor=identity.descriptor,
        loader_domain=identity.boot_loader)
    contract = jni_stack_method_call_contract(
        method, pack, receiver_kind=JniReferenceKind.BORROWED,
        track_exception_state=True)
    if method.function_name != 'CallObjectMethodA' or pack.total_bytes != 8:
        raise RuntimeError('XAX_LOADER_PLAN_MISMATCH')
    return {'method': method, 'pack': pack, 'contract': contract,
            'method_resolution_contract': resolver,
            'returns_generic_class_not_typed_router_class': True,
            'classloader_resolution_executed': False,
            'exception_branch_implemented': False}


def make_xax_bound_loader_call_graph():
    """Construct one XAX graph for a pre-resolved loadClass method and String.

    XAX outputs a local java.lang.Class reference, its owner, the queryable
    exception status, and effects. Never claim its Class is already verified
    to be the Brainfuck router or authorize static dispatch using it.
    """
    from xax_compiler import (Block, Node, Operation, Terminator, ValueRef,
        bits_type, android_arm64_shared_target, function, graph_fragment,
        memory_effect_type, stack_owner_type)
    from xax_jni import (JniReferenceKind, JniExceptionState,
        jni_env_pointer_type, jni_memory_effect_type,
        jni_reference_type, jni_exception_state_type,
        jni_reference_owner_type, jni_env_table_load_node,
        jni_native_function_load_node, jni_argument_pack_nodes,
        jni_exception_check_state_contract, jni_type_objects)
    identity = LoaderResolutionIdentity()
    planned = make_xax_loader_call_plan()
    method, pack_plan = planned['method'], planned['pack']
    target = android_arm64_shared_target()
    env = jni_env_pointer_type()
    loader = jni_reference_type(JniReferenceKind.BORROWED,
        b'java.lang.ClassLoader', loader_domain=identity.boot_loader)
    name = jni_reference_type(JniReferenceKind.BORROWED,
        b'java.lang.String', loader_domain=identity.boot_loader,
        nullable=False)
    clean = jni_exception_state_type(JniExceptionState.CLEAN)
    maybe = jni_exception_state_type(JniExceptionState.MAYBE_PENDING)
    effect = jni_memory_effect_type()
    params = (env, loader, method.method_id_type, name, clean, effect)
    prefix = (
        jni_env_table_load_node(target, ValueRef.parameter(0, 0),
                                ValueRef.parameter(0, 5)),
        jni_native_function_load_node(target, ValueRef.node_result(0, 0, 0),
                ValueRef.node_result(0, 0, 1), method.function_name),
    )
    pack = jni_argument_pack_nodes(pack_plan, (ValueRef.parameter(0, 3),),
                                   target=target, start_node_index=2)
    index = 2 + len(pack.nodes)
    call = Node(Operation.CALL_INDIRECT,
        (ValueRef.node_result(0, 1, 0), ValueRef.parameter(0, 0),
         ValueRef.parameter(0, 1), ValueRef.parameter(0, 2),
         pack.pointer, ValueRef.parameter(0, 4), pack.owner, pack.effect,
         ValueRef.node_result(0, 1, 1)),
        (*method.result_types, maybe, stack_owner_type(),
         memory_effect_type(), effect), entity=planned['contract'])
    end = Node(Operation.STACK_END,
        (ValueRef.node_result(0, index, 3),
         ValueRef.node_result(0, index, 4)), ())
    check_contract = jni_exception_check_state_contract()
    check_load = jni_native_function_load_node(
        target, ValueRef.node_result(0, 0, 0),
        ValueRef.node_result(0, index, 5), 'ExceptionCheck')
    checked = Node(Operation.CALL_INDIRECT,
        (ValueRef.node_result(0, index + 2, 0),
         ValueRef.parameter(0, 0), ValueRef.node_result(0, index, 2),
         ValueRef.node_result(0, index + 2, 1)),
        (bits_type(8), maybe, effect), entity=check_contract)
    outputs = (*method.result_types, bits_type(8), maybe, effect)
    ret = tuple(ValueRef.node_result(0, index, i) for i in (0, 1)) + \
        tuple(ValueRef.node_result(0, index + 3, i) for i in (0, 1, 2))
    graph = graph_fragment((Block(params,
        prefix + pack.nodes + (call, end, check_load, checked),
        Terminator.return_(ret)),))
    fn = function(graph, params, outputs)
    types = jni_type_objects(
        reference_specs=(
            (JniReferenceKind.BORROWED, b'java.lang.ClassLoader', identity.boot_loader),
            (JniReferenceKind.BORROWED, b'java.lang.String', identity.boot_loader, False),
            (JniReferenceKind.LOCAL, b'java.lang.Class'),
        ),
        method_specs=((identity.owner, identity.method, identity.descriptor,
                       False, identity.boot_loader),),
    )
    objects = {o.cid: o for o in (
        target, graph, fn, planned['contract'],
        planned['method_resolution_contract'], check_contract,
        *pack.semantic_objects, *types,
    )}
    return {'graph': graph, 'function': fn,
            'objects': tuple(objects[k] for k in sorted(objects)),
            'jni_operation': method.function_name,
            'exception_check_present': True,
            'jclass_refinement_implemented': False,
            'class_name_string_creation_implemented': False,
            'android_execution_verified': False}
