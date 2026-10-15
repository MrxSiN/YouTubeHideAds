"""Canonical XAX ad interception, typed DexKit discovery and BF fact transport.

Substring calls expose individual facts. Only ad_component.bf combines them
into a classification; the host accepts exactly the authorized one-byte reply.
"""
import json
from toolchain.brainfuck.build import ROOT
from toolchain.brainfuck.router import selector_map
from .module_graph import API

STATE = 'org/youtubehideads/module/AdBindings'
CHAIN = f'L{API}XposedInterface$Chain;'
HOOKER = API + 'XposedInterface$Hooker'
INTERCEPT = 'intercept(' + CHAIN + ')Ljava/lang/Object;'
DK = 'org/luckypray/dexkit/'
PROBES = json.loads((ROOT / 'contracts/ad_component_inputs.json').read_text())['inputs'][2:]


def bindings(j, b):
    return j.special(b, 'jvm-getstatic', STATE, 'values:[Ljava/lang/Object;', (), '[Ljava/lang/Object;')


def slot(j, b, index, descriptor):
    obj = j.element(b, bindings(j, b), '[Ljava/lang/Object;', index)
    return obj if descriptor == 'Ljava/lang/Object;' else j.cast(b, obj, 'Ljava/lang/Object;', descriptor)


def store(j, b, index, value, descriptor):
    j.special(b, 'jvm-arraystore', '[Ljava/lang/Object;', 'store', ('[Ljava/lang/Object;', 'I', 'Ljava/lang/Object;'),
              'V', bindings(j, b), j.integer(b, index), j.object(b, value, descriptor))


def record(j, b, index):
    counters = slot(j, b, 3, 'Ljava/util/concurrent/atomic/AtomicLongArray;')
    count = j.virtual(b, 'java/util/concurrent/atomic/AtomicLongArray', 'incrementAndGet(I)J', counters, j.integer(b, index))
    # Counters avoid logging user content, URLs, or every renderer on the hot path.
    first = j.equal(b, count, b.const(j.type_('J'), 1))
    log, done = j.block(), j.block()
    b.cbr(first, log, (), done, ())
    j.log(log, ('Video ad suppressed', 'Ad component replaced', 'Premium offer collapsed', 'Fullscreen promotion blocked')[index])
    log.br(done)
    return done


# Slot 5 holds settings_snapshot.bf output; bytes 5..8 are the master-gated switches.
SNAPSHOT = 5
VIDEO, COMPONENTS, PREMIUM, FULLSCREEN = 5, 6, 7, 8


def switch(j, b, index):
    return j.element(b, slot(j, b, SNAPSHOT, '[B'), '[B', index)


def classify(j, b, value, enabled):
    facts = [switch(j, b, enabled), b.const(j.type_('B'), 1)]
    from xax_compiler import Operation as O
    for probe in PROBES:
        found = j.virtual(b, 'java/lang/String', 'contains(Ljava/lang/CharSequence;)Z', value,
                          j.cast(b, j.text(b, probe), 'Ljava/lang/String;', 'Ljava/lang/CharSequence;'))
        facts.append(b.op1(O.INT_ZERO_EXTEND, (found,), j.type_('B')))
    reply = j.static(b, 'org/youtubehideads/bf/classify_ad_component', 'run([B)[B', j.array(b, 'B', facts))
    return j.static(b, 'java/util/Arrays', 'equals([B[B)Z', reply, j.array(b, 'B', (b.const(j.type_('B'), 1),)))


def make_ad_install(j):
    # Void methods devoted to ad activation/layout: suppress before side effects.
    b = j.block(CHAIN)
    chain = b.params[0]
    reply = j.static(b, 'org/youtubehideads/bf/dispatch_all', 'run([B)[B',
        j.array(b, 'B', (b.const(j.type_('B'), selector_map()['suppress_video_slot']), switch(j, b, VIDEO),
                         *(b.const(j.type_('B'), n) for n in (1, 1, 0)))))
    allowed = j.static(b, 'java/util/Arrays', 'equals([B[B)Z', reply, j.array(b, 'B', (b.const(j.type_('B'), 1),)))
    suppress, passthrough = j.block(), j.block()
    b.cbr(allowed, suppress, (), passthrough, ())
    record(j, suppress, 0).ret(slot(j, suppress, 4, 'Ljava/lang/Object;'))
    passthrough.ret(j.interface(passthrough, API + 'XposedInterface$Chain', 'proceed()Ljava/lang/Object;', chain))
    video = j.finish((CHAIN,), ('Ljava/lang/Object;',))

    # Retain the parser's original cleanup/side effects, replacing only its result.
    b = j.block(CHAIN)
    chain = b.params[0]
    result = j.interface(b, API + 'XposedInterface$Chain', 'proceed()Ljava/lang/Object;', chain)
    context = j.interface(b, API + 'XposedInterface$Chain', 'getArg(I)Ljava/lang/Object;', chain, j.integer(b, 1))
    path = j.virtual(b, 'java/lang/reflect/Field', 'get(Ljava/lang/Object;)Ljava/lang/Object;',
                     slot(j, b, 0, 'Ljava/lang/reflect/Field;'), context)
    have_path = j.static(b, 'java/util/Objects', 'nonNull(Ljava/lang/Object;)Z', path)
    inspect, done = j.block(), j.block()
    b.cbr(have_path, inspect, (), done, ())
    path_string = j.static(inspect, 'java/lang/String', 'valueOf(Ljava/lang/Object;)Ljava/lang/String;', path)
    allowed = classify(j, inspect, path_string, COMPONENTS)
    suppress = j.block()
    inspect.cbr(allowed, suppress, (), done, ())
    original_context = j.interface(suppress, API + 'XposedInterface$Chain', 'getArg(I)Ljava/lang/Object;', chain, j.integer(suppress, 0))
    empty_builder = j.virtual(suppress, 'java/lang/reflect/Method', 'invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;',
        slot(j, suppress, 1, 'Ljava/lang/reflect/Method;'), slot(j, suppress, 4, 'Ljava/lang/Object;'),
        j.array(suppress, 'Ljava/lang/Object;', (original_context,)))
    empty = j.virtual(suppress, 'java/lang/reflect/Field', 'get(Ljava/lang/Object;)Ljava/lang/Object;',
                      slot(j, suppress, 2, 'Ljava/lang/reflect/Field;'), empty_builder)
    record(j, suppress, 1).ret(empty)
    done.ret(result)
    component = j.finish((CHAIN,), ('Ljava/lang/Object;',))

    b = j.block(CHAIN)
    chain = b.params[0]
    result = j.interface(b, API + 'XposedInterface$Chain', 'proceed()Ljava/lang/Object;', chain)
    receiver = j.interface(b, API + 'XposedInterface$Chain', 'getThisObject()Ljava/lang/Object;', chain)
    reply = j.static(b, 'org/youtubehideads/bf/dispatch_all', 'run([B)[B', j.array(b, 'B',
        (b.const(j.type_('B'), selector_map()['suppress_premium_upsell']), switch(j, b, PREMIUM),
         *(b.const(j.type_('B'), n) for n in (1, 1)))))
    allowed = j.static(b, 'java/util/Arrays', 'equals([B[B)Z', reply, j.array(b, 'B', (b.const(j.type_('B'), 1),)))
    suppress, done = j.block(), j.block()
    b.cbr(allowed, suppress, (), done, ())
    zero = j.static(suppress, 'java/lang/Integer', 'valueOf(I)Ljava/lang/Integer;', j.integer(suppress, 0))
    args = j.array(suppress, 'Ljava/lang/Object;', (j.object(suppress, zero, 'Ljava/lang/Integer;'),)*2)
    j.virtual(suppress, 'java/lang/reflect/Method', 'invoke(Ljava/lang/Object;[Ljava/lang/Object;)Ljava/lang/Object;',
              slot(j, suppress, 6, 'Ljava/lang/reflect/Method;'), receiver, args)
    j.virtual(suppress, 'android/view/View', 'setVisibility(I)V', j.cast(suppress, receiver, 'Ljava/lang/Object;', 'Landroid/view/View;'), j.integer(suppress, 8))
    record(j, suppress, 2).br(done)
    done.ret(result)
    premium = j.finish((CHAIN,), ('Ljava/lang/Object;',))

    # This is invoked only at the unique verified byte[] dialog builder.
    b = j.block(CHAIN)
    chain = b.params[0]
    raw = j.cast(b, j.interface(b, API + 'XposedInterface$Chain', 'getArg(I)Ljava/lang/Object;', chain, j.integer(b, 0)),
                 'Ljava/lang/Object;', '[B')
    exists = j.static(b, 'java/util/Objects', 'nonNull(Ljava/lang/Object;)Z', j.object(b, raw, '[B'))
    inspect, done = j.block(), j.block()
    b.cbr(exists, inspect, (), done, ())
    payload = j.new(inspect, 'java/lang/String', '([BLjava/lang/String;)V', raw, j.text(inspect, 'ISO-8859-1'))
    allowed = classify(j, inspect, payload, FULLSCREEN)
    suppress = j.block()
    inspect.cbr(allowed, suppress, (), done, ())
    end = record(j, suppress, 3)
    end.ret(slot(j, end, 4, 'Ljava/lang/Object;'))
    done.ret(j.interface(done, API + 'XposedInterface$Chain', 'proceed()Ljava/lang/Object;', chain))
    fullscreen = j.finish((CHAIN,), ('Ljava/lang/Object;',))

    # Installers share immutable structural bindings, published before any hook.
    b = j.block(f'L{API}XposedInterface;', f'L{API}XposedModuleInterface$PackageReadyParam;')
    module, param = b.params
    loaded = j.cast(b, param, f'L{API}XposedModuleInterface$PackageReadyParam;', f'L{API}XposedModuleInterface$PackageLoadedParam;')
    state = j.special(b, 'jvm-newarray', 'Ljava/lang/Object;', 'newarray', ('I',), '[Ljava/lang/Object;', j.integer(b, 8))
    j.special(b, 'jvm-putstatic', STATE, 'values:[Ljava/lang/Object;', ('[Ljava/lang/Object;',), 'V', state)
    counters = j.new(b, 'java/util/concurrent/atomic/AtomicLongArray', '(I)V', j.integer(b, 8))
    store(j, b, 3, counters, 'Ljava/util/concurrent/atomic/AtomicLongArray;')
    # Until YouTube shows an Activity, hooks use Brainfuck's defaults (every preference absent).
    defaults = j.static(b, 'org/youtubehideads/bf/settings_snapshot', 'run([B)[B',
                        j.special(b, 'jvm-newarray', 'B', 'newarray', ('I',), '[B', j.integer(b, 10)))
    store(j, b, SNAPSHOT, defaults, '[B')

    info = j.interface(b, API + 'XposedInterface', 'getModuleApplicationInfo()Landroid/content/pm/ApplicationInfo;', module)
    apk = j.special(b, 'jvm-getfield', 'android/content/pm/ApplicationInfo', 'sourceDir:Ljava/lang/String;',
                    ('Landroid/content/pm/ApplicationInfo;',), 'Ljava/lang/String;', info)
    lib = j.virtual(b, 'java/lang/String', 'concat(Ljava/lang/String;)Ljava/lang/String;', apk, j.text(b, '!/lib/arm64-v8a/libdexkit.so'))
    j.static(b, 'java/lang/System', 'load(Ljava/lang/String;)V', lib)
    info = j.interface(b, API + 'XposedModuleInterface$PackageLoadedParam', 'getApplicationInfo()Landroid/content/pm/ApplicationInfo;', loaded)
    apk = j.special(b, 'jvm-getfield', 'android/content/pm/ApplicationInfo', 'sourceDir:Ljava/lang/String;',
                    ('Landroid/content/pm/ApplicationInfo;',), 'Ljava/lang/String;', info)
    loader = j.interface(b, API + 'XposedModuleInterface$PackageReadyParam', 'getClassLoader()Ljava/lang/ClassLoader;', param)
    bridge = j.static(b, DK + 'DexKitBridge', 'create(Ljava/lang/String;)L' + DK + 'DexKitBridge;', apk)
    j.virtual(b, DK + 'DexKitBridge', 'setThreadNum(I)V', bridge, j.integer(b, 2))

    def install(block, method, function, name, counter):
        builder = j.interface(block, API + 'XposedInterface', 'hook(Ljava/lang/reflect/Executable;)L' + API + 'XposedInterface$HookBuilder;',
                              module, j.cast(block, method, 'Ljava/lang/reflect/Method;', 'Ljava/lang/reflect/Executable;'))
        mode = j.special(block, 'jvm-getstatic', API + 'XposedInterface$ExceptionMode', 'PROTECTIVE:L' + API + 'XposedInterface$ExceptionMode;', (), f'L{API}XposedInterface$ExceptionMode;')
        builder = j.interface(block, API + 'XposedInterface$HookBuilder', 'setExceptionMode(L' + API + 'XposedInterface$ExceptionMode;)L' + API + 'XposedInterface$HookBuilder;', builder, mode)
        hooker = j.callback(block, function, HOOKER, INTERCEPT)
        j.interface(block, API + 'XposedInterface$HookBuilder', 'intercept(L' + HOOKER + ';)L' + API + 'XposedInterface$HookHandle;', builder, hooker)
        j.virtual(block, 'java/util/concurrent/atomic/AtomicLongArray', 'incrementAndGet(I)J', counters, j.integer(block, counter))
        j.log(block, name + ' hook installed')

    def query(block, strings=(), *, descriptor=None, return_type=None, count=None, declared=None, name=None, flags=None):
        matcher = (j.static(block, DK + 'query/matchers/MethodMatcher', 'create(Ljava/lang/String;)L' + DK + 'query/matchers/MethodMatcher;', j.text(block, descriptor))
                   if descriptor else j.new(block, DK + 'query/matchers/MethodMatcher', '()V'))
        if strings:
            j.virtual(block, DK + 'query/matchers/MethodMatcher', 'usingStrings([Ljava/lang/String;)L' + DK + 'query/matchers/MethodMatcher;', matcher,
                      j.array(block, 'Ljava/lang/String;', tuple(j.text(block, s) for s in strings)))
        for member, value in (('returnType', return_type), ('declaredClass', declared), ('name', name)):
            if value:
                j.virtual(block, DK + 'query/matchers/MethodMatcher', member + '(Ljava/lang/String;)L' + DK + 'query/matchers/MethodMatcher;', matcher, j.text(block, value))
        for member, value in (('paramCount', count), ('accessFlags', flags)):
            if value is not None:
                j.virtual(block, DK + 'query/matchers/MethodMatcher', member + '(I)L' + DK + 'query/matchers/MethodMatcher;', matcher, j.integer(block, value))
        finder = j.new(block, DK + 'query/FindMethod', '()V')
        j.virtual(block, DK + 'query/FindMethod', 'matcher(L' + DK + 'query/matchers/MethodMatcher;)L' + DK + 'query/FindMethod;', finder, matcher)
        found = j.virtual(block, DK + 'DexKitBridge', 'findMethod(L' + DK + 'query/FindMethod;)L' + DK + 'result/MethodDataList;', bridge, finder)
        return j.cast(block, found, f'L{DK}result/MethodDataList;', 'Ljava/util/List;')

    def require_unique(block, found, failure, label):
        size = j.interface(block, 'java/util/List', 'size()I', found)
        unique = j.equal(block, size, j.integer(block, 1))
        resolved, reject = j.block(), j.block()
        block.cbr(unique, resolved, (), reject, ())
        j.log(reject, label + ' unresolved/ambiguous; left unchanged')
        reject.br(failure)
        data = j.cast(resolved, j.interface(resolved, 'java/util/List', 'get(I)Ljava/lang/Object;', found, j.integer(resolved, 0)),
                      'Ljava/lang/Object;', f'L{DK}result/MethodData;')
        method = j.virtual(resolved, DK + 'result/MethodData', 'getMethodInstance(Ljava/lang/ClassLoader;)Ljava/lang/reflect/Method;', data, loader)
        return resolved, data, method

    for name, strings, count in (
        ('Video ad activation', ("TriggerBundle doesn't have the required metadata specified by the trigger ", 'Ping migration no associated ping bindings for activated trigger: '), 1),
        ('Player ad layout', ('Bootstrapped layout construction resulted in non PlayerBytesLayout. PlayerAds count: ',), 1)):
        next_hook = j.block()
        found = query(b, strings, return_type='void', count=count)
        resolved, _, method = require_unique(b, found, next_hook, name)
        install(resolved, method, video, name, 4)
        resolved.br(next_hook)
        b = next_hook

    after_component = j.block()
    found = query(b, ('Element missing correct type extension', 'Element missing type'), count=6)
    b, data, parser = require_unique(b, found, after_component, 'Component parser')
    parameters = j.virtual(b, 'java/lang/reflect/Method', 'getParameterTypes()[Ljava/lang/Class;', parser)
    context_class = j.element(b, parameters, '[Ljava/lang/Class;', 1)
    # Exactly one StringBuilder field is the structural path, regardless of obfuscated name.
    fields = j.virtual(b, 'java/lang/Class', 'getDeclaredFields()[Ljava/lang/reflect/Field;', context_class)
    length = j.special(b, 'jvm-arraylength', '[Ljava/lang/reflect/Field;', 'length', ('[Ljava/lang/reflect/Field;',), 'I', fields)
    loop, field_body, field_next, fields_done = j.block('I', 'I', 'Ljava/lang/Object;'), j.block(), j.block('I', 'Ljava/lang/Object;'), j.block('I', 'Ljava/lang/Object;')
    b.br(loop, j.integer(b, 0), j.integer(b, 0), slot(j, b, 4, 'Ljava/lang/Object;'))
    from xax_compiler import Operation as O, IntCompare
    index, matches, path_field = loop.params
    more = loop.op1(O.INT_COMPARE, (index, length), j.type_('Z'), attributes=(IntCompare.ULT,))
    loop.cbr(more, field_body, (), fields_done, (matches, path_field))
    field = j.special(field_body, 'jvm-arrayload', '[Ljava/lang/reflect/Field;', 'load', ('[Ljava/lang/reflect/Field;', 'I'), 'Ljava/lang/reflect/Field;', fields, index)
    field_type = j.virtual(field_body, 'java/lang/reflect/Field', 'getType()Ljava/lang/Class;', field)
    field_name = j.virtual(field_body, 'java/lang/Class', 'getName()Ljava/lang/String;', field_type)
    is_path = j.virtual(field_body, 'java/lang/String', 'equals(Ljava/lang/Object;)Z', field_name, j.object(field_body, j.text(field_body, 'java.lang.StringBuilder'), 'Ljava/lang/String;'))
    hit = j.block()
    field_body.cbr(is_path, hit, (), field_next, (matches, path_field))
    increment = hit.op1(O.ADD_WRAP, (matches, j.integer(hit, 1)), j.type_('I'))
    hit.br(field_next, increment, j.object(hit, field, 'Ljava/lang/reflect/Field;'))
    nxt = field_next.op1(O.ADD_WRAP, (index, j.integer(field_next, 1)), j.type_('I'))
    field_next.br(loop, nxt, *field_next.params)
    path_ok = j.equal(fields_done, fields_done.params[0], j.integer(fields_done, 1))
    path_ready = j.block()
    fields_done.cbr(path_ok, path_ready, (), after_component, ())
    path_field = j.cast(path_ready, fields_done.params[1], 'Ljava/lang/Object;', 'Ljava/lang/reflect/Field;')
    j.virtual(path_ready, 'java/lang/reflect/Field', 'setAccessible(Z)V', path_field, path_ready.const(j.type_('Z'), 1))
    store(j, path_ready, 0, path_field, 'Ljava/lang/reflect/Field;')
    # Constructor string + private no-arg signature uniquely identifies EmptyComponent.
    matcher = query(path_ready, ('EmptyComponent',), count=0, name='<init>', flags=2)
    size = j.interface(path_ready, 'java/util/List', 'size()I', matcher)
    unique = j.equal(path_ready, size, j.integer(path_ready, 1))
    empty_ready = j.block()
    path_ready.cbr(unique, empty_ready, (), after_component, ())
    constructor = j.cast(empty_ready, j.interface(empty_ready, 'java/util/List', 'get(I)Ljava/lang/Object;', matcher, j.integer(empty_ready, 0)), 'Ljava/lang/Object;', f'L{DK}result/MethodData;')
    empty_class_name = j.virtual(empty_ready, DK + 'result/MethodData', 'getClassName()Ljava/lang/String;', constructor)
    empty_class = j.virtual(empty_ready, 'java/lang/ClassLoader', 'loadClass(Ljava/lang/String;)Ljava/lang/Class;', loader, empty_class_name)
    # DexKit narrows factory by owner, static access and one parameter; reflection validates exact parameter type below.
    factory_matcher = j.new(empty_ready, DK + 'query/matchers/MethodMatcher', '()V')
    j.virtual(empty_ready, DK + 'query/matchers/MethodMatcher', 'declaredClass(Ljava/lang/String;)L' + DK + 'query/matchers/MethodMatcher;', factory_matcher, empty_class_name)
    j.virtual(empty_ready, DK + 'query/matchers/MethodMatcher', 'accessFlags(I)L' + DK + 'query/matchers/MethodMatcher;', factory_matcher, j.integer(empty_ready, 9))
    j.virtual(empty_ready, DK + 'query/matchers/MethodMatcher', 'paramCount(I)L' + DK + 'query/matchers/MethodMatcher;', factory_matcher, j.integer(empty_ready, 1))
    finder = j.new(empty_ready, DK + 'query/FindMethod', '()V')
    j.virtual(empty_ready, DK + 'query/FindMethod', 'matcher(L' + DK + 'query/matchers/MethodMatcher;)L' + DK + 'query/FindMethod;', finder, factory_matcher)
    factories = j.virtual(empty_ready, DK + 'DexKitBridge', 'findMethod(L' + DK + 'query/FindMethod;)L' + DK + 'result/MethodDataList;', bridge, finder)
    b, _, factory = require_unique(empty_ready, j.cast(empty_ready, factories, f'L{DK}result/MethodDataList;', 'Ljava/util/List;'), after_component, 'Empty component factory')
    factory_params = j.virtual(b, 'java/lang/reflect/Method', 'getParameterTypes()[Ljava/lang/Class;', factory)
    first_class = j.element(b, parameters, '[Ljava/lang/Class;', 0)
    factory_first = j.element(b, factory_params, '[Ljava/lang/Class;', 0)
    same = j.virtual(b, 'java/lang/Class', 'equals(Ljava/lang/Object;)Z', first_class, j.object(b, factory_first, 'Ljava/lang/Class;'))
    valid_factory = j.block()
    b.cbr(same, valid_factory, (), after_component, ())
    b = valid_factory
    return_class = j.virtual(b, 'java/lang/reflect/Method', 'getReturnType()Ljava/lang/Class;', factory)
    fields = j.virtual(b, 'java/lang/Class', 'getDeclaredFields()[Ljava/lang/reflect/Field;', return_class)
    length = j.special(b, 'jvm-arraylength', '[Ljava/lang/reflect/Field;', 'length', ('[Ljava/lang/reflect/Field;',), 'I', fields)
    single = j.equal(b, length, j.integer(b, 1))
    valid_field = j.block()
    b.cbr(single, valid_field, (), after_component, ())
    b = valid_field
    field = j.element(b, fields, '[Ljava/lang/reflect/Field;', 0)
    field_type = j.virtual(b, 'java/lang/reflect/Field', 'getType()Ljava/lang/Class;', field)
    parser_return = j.virtual(b, 'java/lang/reflect/Method', 'getReturnType()Ljava/lang/Class;', parser)
    compatible = j.virtual(b, 'java/lang/Class', 'isAssignableFrom(Ljava/lang/Class;)Z', parser_return, field_type)
    component_ready = j.block()
    b.cbr(compatible, component_ready, (), after_component, ())
    b = component_ready
    store(j, b, 1, factory, 'Ljava/lang/reflect/Method;')
    store(j, b, 2, field, 'Ljava/lang/reflect/Field;')
    install(b, parser, component, 'Ad component', 5)
    b.br(after_component)
    b = after_component

    # Named view class plus full descriptor; unknown versions simply leave it alone.
    after_premium = j.block()
    found = query(b, descriptor='Lcom/google/android/apps/youtube/app/red/presenter/CompactYpcOfferModuleView;->onMeasure(II)V')
    b, _, method = require_unique(b, found, after_premium, 'Premium offer')
    view_class = j.static(b, 'java/lang/Class', 'forName(Ljava/lang/String;)Ljava/lang/Class;', j.text(b, 'android.view.View'))
    int_class = j.special(b, 'jvm-getstatic', 'java/lang/Integer', 'TYPE:Ljava/lang/Class;', (), 'Ljava/lang/Class;')
    measure = j.virtual(b, 'java/lang/Class', 'getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;', view_class, j.text(b, 'setMeasuredDimension'), j.array(b, 'Ljava/lang/Class;', (int_class, int_class)))
    j.virtual(b, 'java/lang/reflect/Method', 'setAccessible(Z)V', measure, b.const(j.type_('Z'), 1))
    store(j, b, 6, measure, 'Ljava/lang/reflect/Method;')
    install(b, method, premium, 'Premium offer', 6)
    b.br(after_premium)
    b = after_premium
    after_fullscreen = j.block()
    matcher = j.new(b, DK + 'query/matchers/MethodMatcher', '()V')
    for member, value in (('returnType', 'void'),):
        j.virtual(b, DK + 'query/matchers/MethodMatcher', member + '(Ljava/lang/String;)L' + DK + 'query/matchers/MethodMatcher;', matcher, j.text(b, value))
    params = j.array(b, 'Ljava/lang/String;', (j.text(b, 'byte[]'), j.cast(b, slot(j, b, 4, 'Ljava/lang/Object;'), 'Ljava/lang/Object;', 'Ljava/lang/String;')))
    j.virtual(b, DK + 'query/matchers/MethodMatcher', 'paramTypes([Ljava/lang/String;)L' + DK + 'query/matchers/MethodMatcher;', matcher, params)
    j.virtual(b, DK + 'query/matchers/MethodMatcher', 'accessFlags(I)L' + DK + 'query/matchers/MethodMatcher;', matcher, j.integer(b, 17))
    invoke = j.new(b, DK + 'query/matchers/MethodMatcher', '()V')
    j.virtual(b, DK + 'query/matchers/MethodMatcher', 'name(Ljava/lang/String;)L' + DK + 'query/matchers/MethodMatcher;', invoke, j.text(b, 'show'))
    j.virtual(b, DK + 'query/matchers/MethodMatcher', 'paramCount(I)L' + DK + 'query/matchers/MethodMatcher;', invoke, j.integer(b, 0))
    j.virtual(b, DK + 'query/matchers/MethodMatcher', 'returnType(Ljava/lang/String;)L' + DK + 'query/matchers/MethodMatcher;', invoke, j.text(b, 'void'))
    j.virtual(b, DK + 'query/matchers/MethodMatcher', 'addInvoke(L' + DK + 'query/matchers/MethodMatcher;)L' + DK + 'query/matchers/MethodMatcher;', matcher, invoke)
    j.virtual(b, DK + 'query/matchers/MethodMatcher', 'addInvoke(Ljava/lang/String;)L' + DK + 'query/matchers/MethodMatcher;', matcher, j.text(b, 'Landroid/app/Activity;->isDestroyed()Z'))
    finder = j.new(b, DK + 'query/FindMethod', '()V')
    j.virtual(b, DK + 'query/FindMethod', 'matcher(L' + DK + 'query/matchers/MethodMatcher;)L' + DK + 'query/FindMethod;', finder, matcher)
    found = j.virtual(b, DK + 'DexKitBridge', 'findMethod(L' + DK + 'query/FindMethod;)L' + DK + 'result/MethodDataList;', bridge, finder)
    b, _, method = require_unique(b, j.cast(b, found, f'L{DK}result/MethodDataList;', 'Ljava/util/List;'), after_fullscreen, 'Fullscreen dialog')
    install(b, method, fullscreen, 'Fullscreen dialog', 7)
    b.br(after_fullscreen)
    b = after_fullscreen
    j.virtual(b, DK + 'DexKitBridge', 'close()V', bridge)
    j.log(b, 'Ad hook discovery finished')
    b.ret()
    return j.finish((f'L{API}XposedInterface;', f'L{API}XposedModuleInterface$PackageReadyParam;'), ())
