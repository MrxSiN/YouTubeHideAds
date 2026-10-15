"""XAX-only canonical managed/JNI byte-array transport smoke carrier.

Build-tool construction of real XAX semantic objects, when an exact upstream
checkout is installed. Does not implement feature policy, make YouTube hooks,
or call any Brainfuck class. The XAX export forwards an existing borrowed JNI
byte[] reference: no implicit allocation/copy or hidden platform policy.

Upstream reference at pinned revision:
  compiler/benchmarks/bench_android_managed.py (ADR-199)
  compiler/src/xax_android_managed.py (check_export_signature)
  compiler/src/xax_jni.py (_jni_reference_family)
"""
from __future__ import annotations
from dataclasses import dataclass

TRANSPORT_DESCRIPTOR = 'Lorg/youtubehideads/bridge/BinaryTransport;'
TRANSPORT_METHOD = 'roundTrip([B)[B'
TRANSPORT_LIBRARY = 'xaxapp'


@dataclass(frozen=True)
class TransportIdentity:
    owner: str = TRANSPORT_DESCRIPTOR
    method: str = 'roundTrip'
    descriptor: str = '([B)[B'
    library: str = TRANSPORT_LIBRARY

    def __post_init__(self):
        if (self.owner, self.method, self.descriptor, self.library) != (
            TRANSPORT_DESCRIPTOR, 'roundTrip', '([B)[B', TRANSPORT_LIBRARY
        ):
            raise ValueError('TRANSPORT_ABI_IS_FROZEN')


def make_semantics():
    """Create a canonical XAX graph and a managed-class target carrier.

    The bridge returns the *same borrowed byte-array handle* only. The caller
    retains its lifetime; this test intentionally has no data interpretation.
    GraphBuilder and the semantic carrier are actual XAX API constructs, not
    handwritten XAX text or an alternative application language.
    """
    try:
        from xax_android_managed import (AndroidManagedClass, AndroidManagedMethod,
                                         android_managed_class_semantics,
                                         check_export_signature)
        from xax_compiler import android_export_symbol, Kind
        from xax_graph_builder import GraphBuilder
        from xax_jni import (JniReferenceKind, jni_env_pointer_type,
                             jni_reference_type, jni_short_native_symbol,
                             jni_type_objects, _jni_reference_family)
    except ImportError as exc:
        raise RuntimeError('PINNED_XAX_COMPILER_NOT_IMPORTED') from exc

    identity = TransportIdentity()
    cls = AndroidManagedClass(identity.owner, methods=(
        AndroidManagedMethod(identity.method, identity.descriptor),
    ), native_library=identity.library)
    method = cls.methods[0]
    # Exact JNI reference families are dictated by upstream descriptor parsing.
    refs = ((JniReferenceKind.BORROWED, identity.owner[1:-1].replace('/', '.').encode(), b'module:youtubehideads'),
            (JniReferenceKind.BORROWED, _jni_reference_family('[B'), b'android.boot'))
    env = jni_env_pointer_type()
    this_ref = jni_reference_type(*refs[0][:2], loader_domain=refs[0][2])
    byte_array = jni_reference_type(*refs[1][:2], loader_domain=refs[1][2])
    graph = GraphBuilder()
    block = graph.block(env, this_ref, byte_array)
    block.ret(block.params[2])
    callback = graph.function((env, this_ref, byte_array), (byte_array,))
    symbol = jni_short_native_symbol(cls.class_descriptor, method.native_name)
    export = android_export_symbol(callback, symbol)
    carrier = android_managed_class_semantics(cls)
    semantic_objects = list(graph.objects.values())
    semantic_objects += list(jni_type_objects(refs))
    semantic_objects += [callback, export, carrier]
    resolved = {value.cid: value for value in semantic_objects}
    error = check_export_signature(method, cls.class_descriptor, callback, resolved.__getitem__)
    if error is not None:
        raise RuntimeError(f'XAX_TRANSPORT_SIGNATURE_REJECTED: {error}')
    return {
        'carrier': carrier,
        'callback': callback,
        'export': export,
        'objects': tuple(resolved.values()),
        'java_descriptor': cls.class_descriptor,
        'method_signature': TRANSPORT_METHOD,
        'jni_symbol': symbol.decode('ascii'),
        'kind': Kind.MODULE.name,
    }
