"""Canonical-XAX JVM graph helpers shared by the module platform hooks."""
from __future__ import annotations
from xax_android_sdk import parse_jvm_method_descriptor
from xax_compiler import (Operation as O, bits_type, foreign_function_symbol,
    jvm_interface_entry_type, opaque_identity_type)
from xax_graph_builder import GraphBuilder
from xax_jvm import jvm_reference_type



class JvmGraph:
    def __init__(self):
        self.graph = GraphBuilder()
        self.types = {}

    def block(self, *descriptors):
        return self.graph.block(*(self.type_(d) for d in descriptors))

    def finish(self, parameters, returns):
        fn = self.graph.function(tuple(self.type_(d) for d in parameters), tuple(self.type_(d) for d in returns))
        objects = tuple(self.graph.objects.values())
        self.graph = GraphBuilder()
        self.graph.track(*objects)
        return fn

    def type_(self, descriptor):
        if descriptor not in self.types:
            if descriptor in {'Z', 'B', 'C', 'S', 'I', 'J'}:
                value = bits_type({'Z': 1, 'B': 8, 'C': 16, 'S': 16, 'I': 32, 'J': 64}[descriptor])
            else:
                value = jvm_reference_type(descriptor.encode())
                self.graph.track(opaque_identity_type(b'jvm-ref:' + descriptor.encode()))
            self.graph.track(value)
            self.types[descriptor] = value
        return self.types[descriptor]

    def call(self, block, abi, owner, member, args=()):
        parameters, result = parse_jvm_method_descriptor(member[member.index('('):])
        inputs = ((f'L{owner};',) if abi in {'jvm-invokevirtual', 'jvm-invokeinterface'} else ()) + parameters
        outputs = () if result == 'V' else (self.type_(result),)
        if len(args) != len(inputs):
            raise ValueError(f'wrong argument count for {owner}.{member}')
        def argument_type(value):
            source = self.graph.blocks[value.block]
            return source.parameter_types[value.index] if value.tag == 0 else source.nodes[value.index].result_types[value.result]
        declaration = foreign_function_symbol(owner.encode(), member.encode(),
            tuple(argument_type(value) for value in args), outputs, abi=abi.encode())
        values = block.op(O.CALL_FOREIGN, args, outputs, entity=declaration)
        return values[0] if values else None

    def virtual(self, block, owner, member, *args):
        return self.call(block, 'jvm-invokevirtual', owner, member, args)

    def interface(self, block, owner, member, *args):
        return self.call(block, 'jvm-invokeinterface', owner, member, args)

    def static(self, block, owner, member, *args):
        return self.call(block, 'jvm-invokestatic', owner, member, args)

    def special(self, block, abi, owner, member, inputs, result, *args):
        outputs = () if result == 'V' else (self.type_(result),)
        declaration = foreign_function_symbol(owner.encode(), member.encode(),
            tuple(self.type_(item) for item in inputs), outputs, abi=abi.encode())
        values = block.op(O.CALL_FOREIGN, args, outputs, entity=declaration)
        return values[0] if values else None

    def text(self, block, value):
        return self.special(block, 'jvm-ldc', 'java/lang/String', value, (), 'Ljava/lang/String;')

    def cast(self, block, value, source, destination):
        return self.special(block, 'jvm-checkcast', destination.removeprefix('L').removesuffix(';')
                       if not destination.startswith('[') else destination,
                       'checkcast', (source,), destination, value)

    def integer(self, block, value):
        return block.const(self.type_('I'), value & 0xffffffff)

    def new(self, block, owner, descriptor, *args):
        parameters, _ = parse_jvm_method_descriptor(descriptor)
        return self.special(block, 'jvm-new', owner, '<init>' + descriptor, parameters, f'L{owner};', *args)

    def array(self, block, component, values=()):
        descriptor = '[' + component
        result = self.special(block, 'jvm-newarray', component, 'newarray', ('I',), descriptor, self.integer(block, len(values)))
        for index, value in enumerate(values):
            self.special(block, 'jvm-arraystore', descriptor, 'store', (descriptor, 'I', component), 'V',
                    result, self.integer(block, index), value)
        return result

    def callback(self, block, function, owner, member):
        signature = jvm_interface_entry_type(owner.encode(), member.encode())
        self.graph.track(opaque_identity_type(b'code-entry:jvm-interface:' + owner.encode() + b'.' + member.encode()))
        return block.op1(O.FUNCTION_ADDRESS, (), signature, entity=function)

    def as_view(self, block, value, source):
        return self.cast(block, value, source, 'Landroid/view/View;')

    def direct(self, block, function, args, returns=()):
        values = block.op(O.CALL_DIRECT, args, tuple(self.type_(d) for d in returns), entity=function)
        return values[0] if values else None

    def element(self, block, array, descriptor, index):
        return self.special(block, 'jvm-arrayload', descriptor, 'load', (descriptor, 'I'), descriptor[1:],
                            array, self.integer(block, index))

    def object(self, block, value, descriptor):
        return self.cast(block, value, descriptor, 'Ljava/lang/Object;')

    def equal(self, block, left, right):
        from xax_compiler import IntCompare
        return block.op1(O.INT_COMPARE, (left, right), self.type_('Z'), attributes=(IntCompare.EQ,))

    def log(self, block, message):
        return self.static(block, 'android/util/Log', 'i(Ljava/lang/String;Ljava/lang/String;)I',
                           self.text(block, 'YouTubeHideAds'), self.text(block, message))

