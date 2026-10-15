"""XAX-only JNI static-method lookup for the Brainfuck router.

The input Class MUST already have been checked for its exact binary name and
its defining module ClassLoader; this file cannot authorize that refinement.
The input C-string pointers MUST point to live NUL-terminated UTF-8 literals
``run`` and ``([B)[B``. Their allocation and lifetime are caller obligations.

This constructs a bounded canonical XAX graph once the pinned external XAX
compiler is supplied. It does not emit JNI application code in C/Java, compile
Android DEX, or claim that a null method ID is usable after a pending exception.
"""
from __future__ import annotations

from dataclasses import dataclass

from .router_call_plan import (ROUTER_CLASS, ROUTER_METHOD, ROUTER_SIGNATURE,
                                BF_MODULE_LOADER)


@dataclass(frozen=True)
class StaticMethodIdentity:
    owner: str = ROUTER_CLASS
    name: str = ROUTER_METHOD
    descriptor: str = ROUTER_SIGNATURE
    defining_loader: bytes = BF_MODULE_LOADER

    def __post_init__(self):
        if (self.owner, self.name, self.descriptor, self.defining_loader) != (
                ROUTER_CLASS, ROUTER_METHOD, ROUTER_SIGNATURE, BF_MODULE_LOADER):
            raise ValueError('XAX_STATIC_METHOD_IDENTITY_FROZEN')


def make_xax_static_method_resolution_plan():
    """Compute exact upstream XAX GetStaticMethodID and exception contracts."""
    try:
        from xax_jni import (JniReferenceKind, jni_get_static_method_id_contract,
                             jni_exception_check_contract, jni_typed_method_id_type)
    except ImportError as error:
        raise RuntimeError('PINNED_XAX_COMPILER_NOT_IMPORTED') from error
    identity = StaticMethodIdentity()
    contract = jni_get_static_method_id_contract(
        JniReferenceKind.LOCAL, owner=identity.owner, name=identity.name,
        descriptor=identity.descriptor, loader_domain=identity.defining_loader)
    method_id = jni_typed_method_id_type(
        identity.owner, identity.name, identity.descriptor,
        is_static=True, loader_domain=identity.defining_loader)
    return {
        'jni_operation': 'GetStaticMethodID',
        'owner': identity.owner, 'method': identity.name,
        'descriptor': identity.descriptor, 'loader': identity.defining_loader,
        'method_id_type': method_id, 'resolution_contract': contract,
        'exception_contract': jni_exception_check_contract(),
        'class_provenance_verified': False, 'name_literals_allocated': False,
        'pending_exception_handled': False, 'android_executed': False,
    }


def make_xax_bound_static_method_resolution_graph():
    """Construct prevalidated-Class -> typed method ID + raw exception flag.

    The graph passes the exact 7 JNI operands for GetStaticMethodID, threads
    the local Class owner, and queries ExceptionCheck using the updated memory
    frontier. No path treats the unguarded method ID as safe. The caller must
    prove a zero exception flag AND non-null ID before static dispatch.
    """
    from xax_compiler import (Block, Node, Operation, Terminator, ValueRef,
        bits_type, android_arm64_shared_target, function, graph_fragment)
    from xax_jni import (JniReferenceKind, jni_class_reference_type,
        jni_c_string_pointer_type, jni_env_pointer_type,
        jni_memory_effect_type, jni_reference_owner_type,
        jni_env_table_load_node, jni_native_function_load_node,
        jni_type_objects)

    identity = StaticMethodIdentity()
    planned = make_xax_static_method_resolution_plan()
    target = android_arm64_shared_target()
    env = jni_env_pointer_type()
    verified_class = jni_class_reference_type(JniReferenceKind.LOCAL,
        owner=identity.owner, loader_domain=identity.defining_loader)
    class_owner = jni_reference_owner_type(JniReferenceKind.LOCAL)
    string_pointer = jni_c_string_pointer_type()
    external_memory = jni_memory_effect_type()
    params = (env, verified_class, class_owner, string_pointer,
              string_pointer, external_memory)

    table = jni_env_table_load_node(target, ValueRef.parameter(0, 0),
                                    ValueRef.parameter(0, 5))
    resolution_fn = jni_native_function_load_node(target,
        ValueRef.node_result(0, 0, 0), ValueRef.node_result(0, 0, 1),
        planned['jni_operation'])
    resolved = Node(Operation.CALL_INDIRECT,
        (ValueRef.node_result(0, 1, 0), ValueRef.parameter(0, 0),
         ValueRef.parameter(0, 1), ValueRef.parameter(0, 2),
         ValueRef.parameter(0, 3), ValueRef.parameter(0, 4),
         ValueRef.node_result(0, 1, 1)),
        (planned['method_id_type'], class_owner, external_memory),
        entity=planned['resolution_contract'])
    check_fn = jni_native_function_load_node(target,
        ValueRef.node_result(0, 0, 0), ValueRef.node_result(0, 2, 2),
        'ExceptionCheck')
    checked = Node(Operation.CALL_INDIRECT,
        (ValueRef.node_result(0, 3, 0), ValueRef.parameter(0, 0),
         ValueRef.node_result(0, 3, 1)),
        (bits_type(8), external_memory), entity=planned['exception_contract'])
    outputs = (planned['method_id_type'], class_owner,
               bits_type(8), external_memory)
    graph = graph_fragment((Block(params, (table, resolution_fn, resolved,
        check_fn, checked), Terminator.return_((
        ValueRef.node_result(0, 2, 0), ValueRef.node_result(0, 2, 1),
        ValueRef.node_result(0, 4, 0), ValueRef.node_result(0, 4, 1))),),))
    routine = function(graph, params, outputs)
    types = jni_type_objects(
        reference_specs=((JniReferenceKind.LOCAL,
             identity.owner.replace('/', '.').encode(), identity.defining_loader),),
        method_specs=((identity.owner, identity.name,
             identity.descriptor, True, identity.defining_loader),),
    )
    objects = {obj.cid: obj for obj in (
        target, graph, routine, *types, planned['resolution_contract'],
        planned['exception_contract'])}
    return {
        'graph': graph, 'function': routine,
        'objects': tuple(objects[cid] for cid in sorted(objects)),
        'operation': planned['jni_operation'],
        'exception_check_present': True,
        'class_provenance_verified': False,
        'cstring_lifetime_verified': False,
        'method_id_nonnull_verified': False,
        'exception_branch_implemented': False,
        'android_execution_verified': False,
    }
