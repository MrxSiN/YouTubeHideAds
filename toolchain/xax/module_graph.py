"""Author the module's platform callbacks as canonical XAX semantic graphs."""
from __future__ import annotations

YOUTUBE = 'com.google.android.youtube'
# shortcut: SettingsActivity/toolbar verified on YouTube 21.41.525; extend discovery if this surface changes.
SETTINGS_ACTIVITY = 'com.google.android.apps.youtube.app.settings.SettingsActivity'
MODULE_CLASS = 'org.youtubehideads.module.Module'
ENTRY_TAG = 'org.youtubehideads.settings.entry'
API = 'io/github/libxposed/api/'


def make_module_graph():
    from xax_compiler import Operation as O
    from .jvm_graph import JvmGraph
    j = JvmGraph()
    graph = j.graph
    type_, virtual, interface, static = j.type_, j.virtual, j.interface, j.static
    special, text, cast, integer, new, array, callback, as_view = (
        j.special, j.text, j.cast, j.integer, j.new, j.array, j.callback, j.as_view)
    from .ad_graph import make_ad_install
    ad_install = make_ad_install(j)
    graph = j.graph

    def label(block, context, value, size):
        view = new(block, 'android/widget/TextView', '(Landroid/content/Context;)V', context)
        chars = cast(block, text(block, value), 'Ljava/lang/String;', 'Ljava/lang/CharSequence;')
        virtual(block, 'android/widget/TextView', 'setText(Ljava/lang/CharSequence;)V', view, chars)
        # setTextAppearance(int) uses the host theme's accessible platform styles.
        virtual(block, 'android/widget/TextView', 'setTextAppearance(I)V', view, integer(block, size))
        base = as_view(block, view, 'Landroid/widget/TextView;')
        virtual(block, 'android/view/View', 'setPadding(IIII)V', base,
                integer(block, 24), integer(block, 16), integer(block, 24), integer(block, 16))
        return base

    # The page is an Android Dialog owned by the YouTube Activity, not a module Activity.
    close = graph.block(type_('Landroid/view/View;'))
    tag = virtual(close, 'android/view/View', 'getTag()Ljava/lang/Object;', close.params[0])
    dialog = cast(close, tag, 'Ljava/lang/Object;', 'Landroid/app/Dialog;')
    virtual(close, 'android/app/Dialog', 'dismiss()V', dialog)
    close.ret()
    close_fn = j.finish(('Landroid/view/View;',), ())
    graph = j.graph

    click = graph.block(type_('Landroid/view/View;'))
    context = virtual(click, 'android/view/View', 'getContext()Landroid/content/Context;', click.params[0])
    dialog = new(click, 'android/app/Dialog', '(Landroid/content/Context;)V', context)
    virtual(click, 'android/app/Dialog', 'requestWindowFeature(I)Z', dialog, integer(click, 1))
    scroll = new(click, 'android/widget/ScrollView', '(Landroid/content/Context;)V', context)
    column = new(click, 'android/widget/LinearLayout', '(Landroid/content/Context;)V', context)
    virtual(click, 'android/widget/LinearLayout', 'setOrientation(I)V', column, integer(click, 1))
    column_group = cast(click, column, 'Landroid/widget/LinearLayout;', 'Landroid/view/ViewGroup;')
    for title, style in (('YouTubeHideAds', 16973890), ('Module connected inside YouTube.', 16973892),
                         ('Ad hooks resolve inside this YouTube process. Counters below show actual interceptions.', 16973892)):
        child = label(click, context, title, style)
        virtual(click, 'android/view/ViewGroup', 'addView(Landroid/view/View;)V', column_group, child)

    from .ad_graph import slot
    counts = virtual(click, 'java/util/concurrent/atomic/AtomicLongArray', 'toString()Ljava/lang/String;',
                     slot(j, click, 3, 'Ljava/util/concurrent/atomic/AtomicLongArray;'))
    info = new(click, 'android/widget/TextView', '(Landroid/content/Context;)V', context)
    virtual(click, 'android/widget/TextView', 'setText(Ljava/lang/CharSequence;)V', info,
            cast(click, counts, 'Ljava/lang/String;', 'Ljava/lang/CharSequence;'))
    virtual(click, 'android/view/ViewGroup', 'addView(Landroid/view/View;)V', column_group,
            as_view(click, info, 'Landroid/widget/TextView;'))
    child = label(click, context, 'Counts: video, components, Premium, fullscreen; installed: video, components, Premium, fullscreen.', 16973892)
    virtual(click, 'android/view/ViewGroup', 'addView(Landroid/view/View;)V', column_group, child)

    # This runs the real BF router inside YouTube. It is an engine self-check,
    # not a fabricated advertisement signal or a claim of live filtering.
    packet = array(click, 'B', tuple(click.const(type_('B'), value) for value in (1, 1, 1, 1, 0)))
    actual = static(click, 'org/youtubehideads/bf/dispatch_all', 'run([B)[B', packet)
    expected = array(click, 'B', (click.const(type_('B'), 1),))
    check = static(click, 'java/util/Arrays', 'equals([B[B)Z', actual, expected)
    valid, invalid = graph.block(), graph.block()
    click.cbr(check, valid, (), invalid, ())
    for block, status in ((valid, 'Brainfuck policy self-check passed'), (invalid, 'Brainfuck policy self-check FAILED')):
        static(block, 'android/util/Log', 'i(Ljava/lang/String;Ljava/lang/String;)I', text(block, 'YouTubeHideAds'), text(block, status))
    show = graph.block()
    valid.br(show)
    invalid.br(show)
    back = new(show, 'android/widget/Button', '(Landroid/content/Context;)V', context)
    chars = cast(show, text(show, 'Back to YouTube settings'), 'Ljava/lang/String;', 'Ljava/lang/CharSequence;')
    virtual(show, 'android/widget/Button', 'setText(Ljava/lang/CharSequence;)V', back, chars)
    back_view = as_view(show, back, 'Landroid/widget/Button;')
    virtual(show, 'android/view/View', 'setTag(Ljava/lang/Object;)V', back_view,
            cast(show, dialog, 'Landroid/app/Dialog;', 'Ljava/lang/Object;'))
    listener = callback(show, close_fn, 'android/view/View$OnClickListener', 'onClick(Landroid/view/View;)V')
    virtual(show, 'android/view/View', 'setOnClickListener(Landroid/view/View$OnClickListener;)V', back_view, listener)
    virtual(show, 'android/view/ViewGroup', 'addView(Landroid/view/View;)V', column_group, back_view)
    scroll_group = cast(show, scroll, 'Landroid/widget/ScrollView;', 'Landroid/view/ViewGroup;')
    virtual(show, 'android/view/ViewGroup', 'addView(Landroid/view/View;)V', scroll_group,
            as_view(show, column, 'Landroid/widget/LinearLayout;'))
    virtual(show, 'android/app/Dialog', 'setContentView(Landroid/view/View;)V', dialog,
            as_view(show, scroll, 'Landroid/widget/ScrollView;'))
    virtual(show, 'android/app/Dialog', 'show()V', dialog)
    window = virtual(show, 'android/app/Dialog', 'getWindow()Landroid/view/Window;', dialog)
    virtual(show, 'android/view/Window', 'setLayout(II)V', window, integer(show, -1), integer(show, -1))
    show.ret()
    click_fn = j.finish(('Landroid/view/View;',), ())
    graph = j.graph

    hook = graph.block(type_(f'L{API}XposedInterface$Chain;'))
    chain = hook.params[0]
    result = interface(hook, API + 'XposedInterface$Chain', 'proceed()Ljava/lang/Object;', chain)
    argument = interface(hook, API + 'XposedInterface$Chain', 'getArg(I)Ljava/lang/Object;', chain, integer(hook, 0))
    focused = virtual(hook, 'java/lang/Boolean', 'booleanValue()Z',
                      cast(hook, argument, 'Ljava/lang/Object;', 'Ljava/lang/Boolean;'))
    focus, done = graph.block(), graph.block()
    hook.cbr(focused, focus, (), done, ())
    receiver = interface(focus, API + 'XposedInterface$Chain', 'getThisObject()Ljava/lang/Object;', chain)
    activity = cast(focus, receiver, 'Ljava/lang/Object;', 'Landroid/app/Activity;')
    obj = cast(focus, activity, 'Landroid/app/Activity;', 'Ljava/lang/Object;')
    clazz = virtual(focus, 'java/lang/Object', 'getClass()Ljava/lang/Class;', obj)
    name = virtual(focus, 'java/lang/Class', 'getName()Ljava/lang/String;', clazz)
    match = virtual(focus, 'java/lang/String', 'equals(Ljava/lang/Object;)Z', name,
                    cast(focus, text(focus, SETTINGS_ACTIVITY), 'Ljava/lang/String;', 'Ljava/lang/Object;'))
    attach = graph.block()
    focus.cbr(match, attach, (), done, ())
    content = virtual(attach, 'android/app/Activity', 'findViewById(I)Landroid/view/View;', activity, integer(attach, 16908290))
    existing = virtual(attach, 'android/view/View', 'findViewWithTag(Ljava/lang/Object;)Landroid/view/View;', content,
                       cast(attach, text(attach, ENTRY_TAG), 'Ljava/lang/String;', 'Ljava/lang/Object;'))
    missing = static(attach, 'java/util/Objects', 'isNull(Ljava/lang/Object;)Z',
                     cast(attach, existing, 'Landroid/view/View;', 'Ljava/lang/Object;'))
    locate, add = graph.block(), graph.block()
    attach.cbr(missing, locate, (), done, ())
    resources = virtual(locate, 'android/app/Activity', 'getResources()Landroid/content/res/Resources;', activity)
    toolbar_id = virtual(locate, 'android/content/res/Resources', 'getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I',
                         resources, text(locate, 'toolbar'), text(locate, 'id'), text(locate, YOUTUBE))
    toolbar = virtual(locate, 'android/app/Activity', 'findViewById(I)Landroid/view/View;', activity, toolbar_id)
    have_toolbar = static(locate, 'java/util/Objects', 'nonNull(Ljava/lang/Object;)Z',
                          cast(locate, toolbar, 'Landroid/view/View;', 'Ljava/lang/Object;'))
    locate.cbr(have_toolbar, add, (), done, ())
    context = cast(add, activity, 'Landroid/app/Activity;', 'Landroid/content/Context;')
    button = new(add, 'android/widget/Button', '(Landroid/content/Context;)V', context)
    chars = cast(add, text(add, 'YouTubeHideAds'), 'Ljava/lang/String;', 'Ljava/lang/CharSequence;')
    virtual(add, 'android/widget/Button', 'setText(Ljava/lang/CharSequence;)V', button, chars)
    virtual(add, 'android/widget/Button', 'setAllCaps(Z)V', button, add.const(type_('Z'), 0))
    button_view = as_view(add, button, 'Landroid/widget/Button;')
    virtual(add, 'android/view/View', 'setContentDescription(Ljava/lang/CharSequence;)V', button_view, chars)
    virtual(add, 'android/view/View', 'setTag(Ljava/lang/Object;)V', button_view,
            cast(add, text(add, ENTRY_TAG), 'Ljava/lang/String;', 'Ljava/lang/Object;'))
    listener = callback(add, click_fn, 'android/view/View$OnClickListener', 'onClick(Landroid/view/View;)V')
    virtual(add, 'android/view/View', 'setOnClickListener(Landroid/view/View$OnClickListener;)V', button_view, listener)
    # Toolbar supplies its own layout parameters; no obfuscated AppCompat method
    # or copied support library is needed to add a platform View.
    virtual(add, 'android/view/ViewGroup', 'addView(Landroid/view/View;)V',
            cast(add, toolbar, 'Landroid/view/View;', 'Landroid/view/ViewGroup;'), button_view)
    static(add, 'android/util/Log', 'i(Ljava/lang/String;Ljava/lang/String;)I', text(add, 'YouTubeHideAds'), text(add, 'Settings entry attached'))
    add.br(done)
    done.ret(result)
    hook_fn = j.finish((f'L{API}XposedInterface$Chain;',), ('Ljava/lang/Object;',))
    graph = j.graph

    params = (type_(f'L{API}XposedInterface;'), type_(f'L{API}XposedModuleInterface$PackageReadyParam;'))
    entry = graph.block(*params)
    module, param = entry.params
    loaded = cast(entry, param, f'L{API}XposedModuleInterface$PackageReadyParam;', f'L{API}XposedModuleInterface$PackageLoadedParam;')
    first = interface(entry, API + 'XposedModuleInterface$PackageLoadedParam', 'isFirstPackage()Z', loaded)
    install, stop = graph.block(), graph.block()
    entry.cbr(first, install, (), stop, ())
    package = interface(install, API + 'XposedModuleInterface$PackageLoadedParam', 'getPackageName()Ljava/lang/String;', loaded)
    match = virtual(install, 'java/lang/String', 'equals(Ljava/lang/Object;)Z', package,
                    cast(install, text(install, YOUTUBE), 'Ljava/lang/String;', 'Ljava/lang/Object;'))
    ready = graph.block()
    install.cbr(match, ready, (), stop, ())
    clazz = static(ready, 'java/lang/Class', 'forName(Ljava/lang/String;)Ljava/lang/Class;', text(ready, 'android.app.Activity'))
    boolean_class = special(ready, 'jvm-getstatic', 'java/lang/Boolean', 'TYPE:Ljava/lang/Class;', (), 'Ljava/lang/Class;')
    method = virtual(ready, 'java/lang/Class', 'getDeclaredMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;',
                     clazz, text(ready, 'onWindowFocusChanged'), array(ready, 'Ljava/lang/Class;', (boolean_class,)))
    builder = interface(ready, API + 'XposedInterface', 'hook(Ljava/lang/reflect/Executable;)L' + API + 'XposedInterface$HookBuilder;',
                        module, cast(ready, method, 'Ljava/lang/reflect/Method;', 'Ljava/lang/reflect/Executable;'))
    mode = special(ready, 'jvm-getstatic', API + 'XposedInterface$ExceptionMode', 'PROTECTIVE:L' + API + 'XposedInterface$ExceptionMode;',
                   (), f'L{API}XposedInterface$ExceptionMode;')
    builder = interface(ready, API + 'XposedInterface$HookBuilder', 'setExceptionMode(L' + API + 'XposedInterface$ExceptionMode;)L' + API + 'XposedInterface$HookBuilder;', builder, mode)
    hooker = callback(ready, hook_fn, API + 'XposedInterface$Hooker', 'intercept(L' + API + 'XposedInterface$Chain;)Ljava/lang/Object;')
    interface(ready, API + 'XposedInterface$HookBuilder', 'intercept(L' + API + 'XposedInterface$Hooker;)L' + API + 'XposedInterface$HookHandle;', builder, hooker)
    static(ready, 'android/util/Log', 'i(Ljava/lang/String;Ljava/lang/String;)I', text(ready, 'YouTubeHideAds'), text(ready, 'YouTube lifecycle hook installed'))
    j.direct(ready, ad_install, (module, param))
    ready.br(stop)
    stop.ret()
    function = graph.function(params, ())
    return {'function': function, 'objects': tuple(graph.objects.values())}
