"""Author the module's platform callbacks as canonical XAX semantic graphs."""
from __future__ import annotations

YOUTUBE = 'com.google.android.youtube'
# shortcut: SettingsActivity and its preference list verified on YouTube 21.41.525; extend discovery if this surface changes.
SETTINGS_ACTIVITY = 'com.google.android.apps.youtube.app.settings.SettingsActivity'
MODULE_CLASS = 'org.youtubehideads.module.Module'
ENTRY_TAG = 'org.youtubehideads.settings.entry'
PREFERENCES = 'youtubehideads'
VERSION = '0.3.0-dev'
API = 'io/github/libxposed/api/'

# Order is the settings_snapshot.bf input/output order. Text is presentation only.
SWITCHES = (
    ('hide_ads', 'Hide ads', 'Turn every ad filter on or off at once'),
    ('video_ads', 'Video ads', 'Skip ads that play before and during videos'),
    ('component_ads', 'Feed and search ads', 'Remove sponsored cards, ad shelves, shopping and promoted results'),
    ('premium_promotions', 'Premium promotions', 'Hide YouTube Premium offers'),
    ('fullscreen_promotions', 'Fullscreen promotions', 'Block full-screen promotional pop-ups'),
)

TEXT_SECONDARY = 16842808         # android.R.attr.textColorSecondary
ITEM_BACKGROUND = 16843534        # android.R.attr.selectableItemBackground
ITEM_BACKGROUND_ROUND = 16843868  # android.R.attr.selectableItemBackgroundBorderless


def make_module_graph():
    from .jvm_graph import JvmGraph
    from .ad_graph import make_ad_install, slot, store, SNAPSHOT
    j = JvmGraph()
    type_, virtual, interface, static = j.type_, j.virtual, j.interface, j.static
    special, text, cast, integer, new, array, callback, as_view = (
        j.special, j.text, j.cast, j.integer, j.new, j.array, j.callback, j.as_view)
    ad_install = make_ad_install(j)
    CONTEXT, VIEW, GROUP = 'Landroid/content/Context;', 'Landroid/view/View;', 'Landroid/view/ViewGroup;'

    def chars(block, value):
        return cast(block, value, 'Ljava/lang/String;', 'Ljava/lang/CharSequence;')

    def add(block, parent, child, source=VIEW):
        virtual(block, 'android/view/ViewGroup', 'addView(Landroid/view/View;)V',
                parent, child if source == VIEW else as_view(block, child, source))

    def preferences(block, context):
        return virtual(block, 'android/content/Context', 'getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;',
                       context, text(block, PREFERENCES), integer(block, 0))

    def editor(block, context):
        return interface(block, 'android/content/SharedPreferences', 'edit()Landroid/content/SharedPreferences$Editor;',
                         preferences(block, context))

    # --- refresh(Context): stored bits -> settings_snapshot.bf -> AdBindings slot 5.
    # Runs on Activity focus and after each toggle; hooks only read the published array.
    from xax_compiler import Operation as O
    b = j.block(CONTEXT)
    prefs = preferences(b, b.params[0])
    bits = []
    for key, _, _ in SWITCHES:
        for member in ('contains(Ljava/lang/String;)Z', 'getBoolean(Ljava/lang/String;Z)Z'):
            args = (text(b, key),) + ((b.const(type_('Z'), 0),) if 'getBoolean' in member else ())
            value = interface(b, 'android/content/SharedPreferences', member, prefs, *args)
            bits.append(b.op1(O.INT_ZERO_EXTEND, (value,), type_('B')))
    snapshot = static(b, 'org/youtubehideads/bf/settings_snapshot', 'run([B)[B', array(b, 'B', tuple(bits)))
    store(j, b, SNAPSHOT, snapshot, '[B')
    b.ret()
    refresh = j.finish((CONTEXT,), ())

    # --- dp(Context, int): integer density conversion, no float constants needed.
    b = j.block(CONTEXT, 'I')
    resources = virtual(b, 'android/content/Context', 'getResources()Landroid/content/res/Resources;', b.params[0])
    metrics = virtual(b, 'android/content/res/Resources', 'getDisplayMetrics()Landroid/util/DisplayMetrics;', resources)
    dpi = special(b, 'jvm-getfield', 'android/util/DisplayMetrics', 'densityDpi:I', ('Landroid/util/DisplayMetrics;',), 'I', metrics)
    product = static(b, 'java/lang/Math', 'multiplyExact(II)I', b.params[1], dpi)
    b.ret(static(b, 'java/lang/Math', 'floorDiv(II)I', product, integer(b, 160)))
    dp = j.finish((CONTEXT, 'I'), ('I',))

    def px(block, context, value):
        return j.direct(block, dp, (context, integer(block, value)), ('I',))

    def pad(block, view, context, left, top, right, bottom):
        virtual(block, 'android/view/View', 'setPadding(IIII)V', view,
                *(px(block, context, n) for n in (left, top, right, bottom)))

    # --- themed(Context, int attr): one Drawable or ColorStateList from YouTube's own theme.
    def themed(kind):
        b = j.block(CONTEXT, 'I')
        attrs = array(b, 'I', (b.params[1],))
        typed = virtual(b, 'android/content/Context', 'obtainStyledAttributes([I)Landroid/content/res/TypedArray;', b.params[0], attrs)
        if kind == 'drawable':
            value = virtual(b, 'android/content/res/TypedArray', 'getDrawable(I)Landroid/graphics/drawable/Drawable;', typed, integer(b, 0))
            result = 'Landroid/graphics/drawable/Drawable;'
        else:
            value = virtual(b, 'android/content/res/TypedArray', 'getColorStateList(I)Landroid/content/res/ColorStateList;', typed, integer(b, 0))
            result = 'Landroid/content/res/ColorStateList;'
        virtual(b, 'android/content/res/TypedArray', 'recycle()V', typed)
        b.ret(value)
        return j.finish((CONTEXT, 'I'), (result,))
    themed_drawable, themed_color = themed('drawable'), themed('color')

    def background(block, view, context, attr):
        drawable = j.direct(block, themed_drawable, (context, integer(block, attr)), ('Landroid/graphics/drawable/Drawable;',))
        virtual(block, 'android/view/View', 'setBackground(Landroid/graphics/drawable/Drawable;)V', view, drawable)

    def youtube_drawable(block, context, name):
        # YouTube's own outline icons, so the theme tints them like its other rows.
        resources = virtual(block, 'android/content/Context', 'getResources()Landroid/content/res/Resources;', context)
        ident = virtual(block, 'android/content/res/Resources', 'getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I',
                        resources, text(block, name), text(block, 'drawable'), text(block, YOUTUBE))
        return virtual(block, 'android/content/Context', 'getDrawable(I)Landroid/graphics/drawable/Drawable;', context, ident)

    def label(block, context, value, style):
        view = new(block, 'android/widget/TextView', '(Landroid/content/Context;)V', context)
        virtual(block, 'android/widget/TextView', 'setText(Ljava/lang/CharSequence;)V', view, chars(block, value))
        resources = virtual(block, 'android/content/Context', 'getResources()Landroid/content/res/Resources;', context)
        ident = virtual(block, 'android/content/res/Resources', 'getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I',
                        resources, text(block, 'TextAppearance.Material.' + style), text(block, 'style'), text(block, 'android'))
        virtual(block, 'android/widget/TextView', 'setTextAppearance(I)V', view, ident)
        return view

    def secondary(block, view, context):
        color = j.direct(block, themed_color, (context, integer(block, TEXT_SECONDARY)), ('Landroid/content/res/ColorStateList;',))
        virtual(block, 'android/widget/TextView', 'setTextColor(Landroid/content/res/ColorStateList;)V', view, color)

    # --- header(Context, String): bold section title, like "Account".
    b = j.block(CONTEXT, 'Ljava/lang/String;')
    context = b.params[0]
    view = label(b, context, b.params[1], 'Title')
    bold = special(b, 'jvm-getstatic', 'android/graphics/Typeface', 'DEFAULT_BOLD:Landroid/graphics/Typeface;', (), 'Landroid/graphics/Typeface;')
    virtual(b, 'android/widget/TextView', 'setTypeface(Landroid/graphics/Typeface;)V', view, bold)
    view = as_view(b, view, 'Landroid/widget/TextView;')
    pad(b, view, context, 16, 24, 16, 8)
    b.ret(view)
    header = j.finish((CONTEXT, 'Ljava/lang/String;'), (VIEW,))

    # --- text_block(Context, title, summary): title over secondary summary, YouTube row padding.
    b = j.block(CONTEXT, 'Ljava/lang/String;', 'Ljava/lang/String;')
    context = b.params[0]
    column = new(b, 'android/widget/LinearLayout', '(Landroid/content/Context;)V', context)
    virtual(b, 'android/widget/LinearLayout', 'setOrientation(I)V', column, integer(b, 1))
    group = cast(b, column, 'Landroid/widget/LinearLayout;', GROUP)
    add(b, group, label(b, context, b.params[1], 'Subhead'), 'Landroid/widget/TextView;')
    summary = label(b, context, b.params[2], 'Body1')
    secondary(b, summary, context)
    add(b, group, summary, 'Landroid/widget/TextView;')
    column_view = as_view(b, column, 'Landroid/widget/LinearLayout;')
    pad(b, column_view, context, 16, 16, 80, 16)
    b.ret(column_view)
    text_block = j.finish((CONTEXT, 'Ljava/lang/String;', 'Ljava/lang/String;'), (VIEW,))

    # --- Listeners. State travels in View tags; XAX callbacks capture nothing.
    # The pinned JVM lowering cannot bind a boolean callback parameter, so the switch's
    # own click listener reads isChecked() after the platform has flipped it.
    b = j.block(VIEW)
    view = b.params[0]
    button = cast(b, view, VIEW, 'Landroid/widget/CompoundButton;')
    checked = virtual(b, 'android/widget/CompoundButton', 'isChecked()Z', button)
    key = cast(b, virtual(b, 'android/view/View', 'getTag()Ljava/lang/Object;', view), 'Ljava/lang/Object;', 'Ljava/lang/String;')
    context = virtual(b, 'android/view/View', 'getContext()Landroid/content/Context;', view)
    edit = editor(b, context)
    edit = interface(b, 'android/content/SharedPreferences$Editor', 'putBoolean(Ljava/lang/String;Z)Landroid/content/SharedPreferences$Editor;', edit, key, checked)
    # commit() so the snapshot below reads the value just written.
    interface(b, 'android/content/SharedPreferences$Editor', 'commit()Z', edit)
    j.direct(b, refresh, (context,))
    b.ret()
    changed = j.finish((VIEW,), ())

    b = j.block(VIEW)
    target = cast(b, virtual(b, 'android/view/View', 'getTag()Ljava/lang/Object;', b.params[0]), 'Ljava/lang/Object;', VIEW)
    virtual(b, 'android/view/View', 'performClick()Z', target)
    b.ret()
    toggle = j.finish((VIEW,), ())

    b = j.block(VIEW)
    dialog = cast(b, virtual(b, 'android/view/View', 'getTag()Ljava/lang/Object;', b.params[0]), 'Ljava/lang/Object;', 'Landroid/app/Dialog;')
    virtual(b, 'android/app/Dialog', 'dismiss()V', dialog)
    b.ret()
    close = j.finish((VIEW,), ())

    b = j.block(VIEW)
    context = virtual(b, 'android/view/View', 'getContext()Landroid/content/Context;', b.params[0])
    interface(b, 'android/content/SharedPreferences$Editor', 'commit()Z',
              interface(b, 'android/content/SharedPreferences$Editor', 'clear()Landroid/content/SharedPreferences$Editor;', editor(b, context)))
    j.direct(b, refresh, (context,))
    j.log(b, 'Settings reset to defaults')
    dialog = cast(b, virtual(b, 'android/view/View', 'getTag()Ljava/lang/Object;', b.params[0]), 'Ljava/lang/Object;', 'Landroid/app/Dialog;')
    virtual(b, 'android/app/Dialog', 'dismiss()V', dialog)
    b.ret()
    reset = j.finish((VIEW,), ())

    # --- switch_row(Context, key, title, summary, checked): YouTube's title/summary/switch row.
    b = j.block(CONTEXT, 'Ljava/lang/String;', 'Ljava/lang/String;', 'Ljava/lang/String;', 'Z')
    context, key, title, summary, checked = b.params
    row = new(b, 'android/widget/FrameLayout', '(Landroid/content/Context;)V', context)
    row_view = as_view(b, row, 'Landroid/widget/FrameLayout;')
    row_group = cast(b, row, 'Landroid/widget/FrameLayout;', GROUP)
    add(b, row_group, j.direct(b, text_block, (context, title, summary), (VIEW,)))
    toggle_view = new(b, 'android/widget/Switch', '(Landroid/content/Context;)V', context)
    compound = cast(b, toggle_view, 'Landroid/widget/Switch;', 'Landroid/widget/CompoundButton;')
    virtual(b, 'android/widget/CompoundButton', 'setChecked(Z)V', compound, checked)
    switch_view = as_view(b, toggle_view, 'Landroid/widget/Switch;')
    virtual(b, 'android/view/View', 'setTag(Ljava/lang/Object;)V', switch_view, j.object(b, key, 'Ljava/lang/String;'))
    virtual(b, 'android/view/View', 'setContentDescription(Ljava/lang/CharSequence;)V', switch_view, chars(b, title))
    virtual(b, 'android/view/View', 'setOnClickListener(Landroid/view/View$OnClickListener;)V', switch_view,
            callback(b, changed, 'android/view/View$OnClickListener', 'onClick(Landroid/view/View;)V'))
    params = new(b, 'android/widget/FrameLayout$LayoutParams', '(III)V', integer(b, -2), integer(b, -2), integer(b, 8388629))
    virtual(b, 'android/view/ViewGroup$MarginLayoutParams', 'setMarginEnd(I)V',
            cast(b, params, 'Landroid/widget/FrameLayout$LayoutParams;', 'Landroid/view/ViewGroup$MarginLayoutParams;'), px(b, context, 16))
    virtual(b, 'android/view/ViewGroup', 'addView(Landroid/view/View;Landroid/view/ViewGroup$LayoutParams;)V', row_group, switch_view,
            cast(b, params, 'Landroid/widget/FrameLayout$LayoutParams;', 'Landroid/view/ViewGroup$LayoutParams;'))
    # Tapping anywhere on the row flips the switch, as in YouTube's own rows.
    virtual(b, 'android/view/View', 'setTag(Ljava/lang/Object;)V', row_view, j.object(b, switch_view, VIEW))
    virtual(b, 'android/view/View', 'setOnClickListener(Landroid/view/View$OnClickListener;)V', row_view,
            callback(b, toggle, 'android/view/View$OnClickListener', 'onClick(Landroid/view/View;)V'))
    background(b, row_view, context, ITEM_BACKGROUND)
    b.ret(row_view)
    switch_row = j.finish((CONTEXT, 'Ljava/lang/String;', 'Ljava/lang/String;', 'Ljava/lang/String;', 'Z'), (VIEW,))

    def counter(block, counters, index):
        value = virtual(block, 'java/util/concurrent/atomic/AtomicLongArray', 'get(I)J', counters, integer(block, index))
        return static(block, 'java/lang/String', 'valueOf(J)Ljava/lang/String;', value)

    def join(block, *parts):
        result = parts[0]
        for part in parts[1:]:
            result = virtual(block, 'java/lang/String', 'concat(Ljava/lang/String;)Ljava/lang/String;', result, part)
        return result

    # --- open(View): the settings page, a full-screen Dialog owned by YouTube's Activity.
    b = j.block(VIEW)
    context = virtual(b, 'android/view/View', 'getContext()Landroid/content/Context;', b.params[0])
    j.direct(b, refresh, (context,))
    # Engine self-check: the real BF router runs inside YouTube on a known input.
    packet = array(b, 'B', tuple(b.const(type_('B'), value) for value in (1, 1, 1, 1, 0)))
    actual = static(b, 'org/youtubehideads/bf/dispatch_all', 'run([B)[B', packet)
    expected = array(b, 'B', (b.const(type_('B'), 1),))
    check = static(b, 'java/util/Arrays', 'equals([B[B)Z', actual, expected)
    valid, invalid, page = j.block(), j.block(), j.block('Ljava/lang/String;')
    b.cbr(check, valid, (), invalid, ())
    for block, status in ((valid, 'Self-check passed'), (invalid, 'Self-check FAILED')):
        j.log(block, 'Brainfuck policy ' + status.lower())
        block.br(page, text(block, status))
    b, engine = page, page.params[0]

    dialog = new(b, 'android/app/Dialog', '(Landroid/content/Context;)V', context)
    virtual(b, 'android/app/Dialog', 'requestWindowFeature(I)Z', dialog, integer(b, 1))
    dialog_tag = j.object(b, dialog, 'Landroid/app/Dialog;')
    root = new(b, 'android/widget/LinearLayout', '(Landroid/content/Context;)V', context)
    virtual(b, 'android/widget/LinearLayout', 'setOrientation(I)V', root, integer(b, 1))
    root_group = cast(b, root, 'Landroid/widget/LinearLayout;', GROUP)

    # Toolbar: back arrow and title, YouTube's 48dp bar.
    bar = new(b, 'android/widget/LinearLayout', '(Landroid/content/Context;)V', context)
    virtual(b, 'android/widget/LinearLayout', 'setGravity(I)V', bar, integer(b, 16))
    back = new(b, 'android/widget/ImageButton', '(Landroid/content/Context;)V', context)
    virtual(b, 'android/widget/ImageView', 'setImageDrawable(Landroid/graphics/drawable/Drawable;)V',
            cast(b, back, 'Landroid/widget/ImageButton;', 'Landroid/widget/ImageView;'), youtube_drawable(b, context, 'yt_outline_arrow_left_vd_theme_24'))
    back_view = as_view(b, back, 'Landroid/widget/ImageButton;')
    background(b, back_view, context, ITEM_BACKGROUND_ROUND)
    virtual(b, 'android/view/View', 'setContentDescription(Ljava/lang/CharSequence;)V', back_view, chars(b, text(b, 'Navigate up')))
    virtual(b, 'android/view/View', 'setTag(Ljava/lang/Object;)V', back_view, dialog_tag)
    virtual(b, 'android/view/View', 'setOnClickListener(Landroid/view/View$OnClickListener;)V', back_view,
            callback(b, close, 'android/view/View$OnClickListener', 'onClick(Landroid/view/View;)V'))
    bar_group = cast(b, bar, 'Landroid/widget/LinearLayout;', GROUP)
    size = px(b, context, 56)
    virtual(b, 'android/view/ViewGroup', 'addView(Landroid/view/View;II)V', bar_group, back_view, size, px(b, context, 48))
    title_text = label(b, context, text(b, 'YouTubeHideAds'), 'Title')
    virtual(b, 'android/widget/ImageView', 'setImageTintList(Landroid/content/res/ColorStateList;)V',
            cast(b, back, 'Landroid/widget/ImageButton;', 'Landroid/widget/ImageView;'),
            virtual(b, 'android/widget/TextView', 'getTextColors()Landroid/content/res/ColorStateList;', title_text))
    title = as_view(b, title_text, 'Landroid/widget/TextView;')
    pad(b, title, context, 16, 0, 16, 0)
    add(b, bar_group, title)
    add(b, root_group, bar, 'Landroid/widget/LinearLayout;')

    column = new(b, 'android/widget/LinearLayout', '(Landroid/content/Context;)V', context)
    virtual(b, 'android/widget/LinearLayout', 'setOrientation(I)V', column, integer(b, 1))
    column_group = cast(b, column, 'Landroid/widget/LinearLayout;', GROUP)

    def section(name):
        add(b, column_group, j.direct(b, header, (context, text(b, name)), (VIEW,)))

    def info(title, summary, click=None, tag=None):
        row = j.direct(b, text_block, (context, text(b, title) if isinstance(title, str) else title,
                                       text(b, summary) if isinstance(summary, str) else summary), (VIEW,))
        if click:
            virtual(b, 'android/view/View', 'setTag(Ljava/lang/Object;)V', row, tag)
            virtual(b, 'android/view/View', 'setOnClickListener(Landroid/view/View$OnClickListener;)V', row,
                    callback(b, click, 'android/view/View$OnClickListener', 'onClick(Landroid/view/View;)V'))
            background(b, row, context, ITEM_BACKGROUND)
        add(b, column_group, row)

    section('Ads')
    raw = slot(j, b, SNAPSHOT, '[B')
    for index, (key, title_text, summary_text) in enumerate(SWITCHES):
        value = j.element(b, raw, '[B', index)
        checked = j.equal(b, value, b.const(type_('B'), 1))
        add(b, column_group, j.direct(b, switch_row, (context, text(b, key), text(b, title_text), text(b, summary_text), checked), (VIEW,)))

    section('SponsorBlock')
    info('Skip sponsored segments', 'Not available yet. The skip policies are written; the player hook is not connected')

    section('About')
    counters = slot(j, b, 3, 'Ljava/util/concurrent/atomic/AtomicLongArray;')
    # ldc constants are ASCII-only in the pinned XAX JVM lowering; the middle dot is built from its code point.
    middle = static(b, 'java/lang/String', 'valueOf(C)Ljava/lang/String;', b.const(type_('C'), 0xB7))
    dot = join(b, text(b, ' '), middle, text(b, ' '))
    info('Removed this session', join(b, text(b, 'Video ads '), counter(b, counters, 0), dot, text(b, 'Components '), counter(b, counters, 1),
                                      dot, text(b, 'Premium '), counter(b, counters, 2), dot, text(b, 'Pop-ups '), counter(b, counters, 3)))
    info('Hooks installed', join(b, text(b, 'Video '), counter(b, counters, 4), dot, text(b, 'Components '), counter(b, counters, 5),
                                 dot, text(b, 'Premium '), counter(b, counters, 6), dot, text(b, 'Pop-ups '), counter(b, counters, 7)))
    info('Brainfuck engine', engine)
    info('Version', join(b, text(b, VERSION), dot, text(b, 'libxposed API 102')))
    info('Reset to defaults', 'Turn every switch back on', reset, dialog_tag)

    scroll = new(b, 'android/widget/ScrollView', '(Landroid/content/Context;)V', context)
    add(b, cast(b, scroll, 'Landroid/widget/ScrollView;', GROUP), column, 'Landroid/widget/LinearLayout;')
    virtual(b, 'android/view/ViewGroup', 'addView(Landroid/view/View;II)V', root_group,
            as_view(b, scroll, 'Landroid/widget/ScrollView;'), integer(b, -1), integer(b, -1))
    virtual(b, 'android/app/Dialog', 'setContentView(Landroid/view/View;)V', dialog, as_view(b, root, 'Landroid/widget/LinearLayout;'))
    virtual(b, 'android/app/Dialog', 'show()V', dialog)
    window = virtual(b, 'android/app/Dialog', 'getWindow()Landroid/view/Window;', dialog)
    virtual(b, 'android/view/Window', 'setLayout(II)V', window, integer(b, -1), integer(b, -1))
    # The page wears the theme's window background, so light and dark both match YouTube.
    # The row's context is a theme wrapper, not the Activity, so nothing here casts to Activity.
    virtual(b, 'android/view/Window', 'setBackgroundDrawable(Landroid/graphics/drawable/Drawable;)V', window,
            j.direct(b, themed_drawable, (context, integer(b, 16842836)), ('Landroid/graphics/drawable/Drawable;',)))
    b.ret()
    open_page = j.finish((VIEW,), ())

    # --- attach(holder, layout bounds...): add the entry row above YouTube's top-level list.
    # Runs as the list's OnLayoutChangeListener, because at focus time the rows are not bound yet.
    layout = (VIEW,) + ('I',) * 8
    top_block = j.block(*layout)
    holder = top_block.params[0]
    done = j.block()
    context = virtual(top_block, 'android/view/View', 'getContext()Landroid/content/Context;', holder)
    parent = virtual(top_block, 'android/view/View', 'getParent()Landroid/view/ViewParent;', holder)
    group_class = static(top_block, 'java/lang/Class', 'forName(Ljava/lang/String;)Ljava/lang/Class;', text(top_block, 'android.view.ViewGroup'))
    is_group = virtual(top_block, 'java/lang/Class', 'isInstance(Ljava/lang/Object;)Z', group_class,
                       cast(top_block, parent, 'Landroid/view/ViewParent;', 'Ljava/lang/Object;'))
    grouped, top, place = j.block(), j.block(), j.block()
    top_block.cbr(is_group, grouped, (), done, ())
    parent_view = cast(grouped, parent, 'Landroid/view/ViewParent;', VIEW)
    existing = virtual(grouped, 'android/view/View', 'findViewWithTag(Ljava/lang/Object;)Landroid/view/View;', parent_view,
                       j.object(grouped, text(grouped, ENTRY_TAG), 'Ljava/lang/String;'))
    missing = static(grouped, 'java/util/Objects', 'isNull(Ljava/lang/Object;)Z', j.object(grouped, existing, VIEW))
    grouped.cbr(missing, top, (), done, ())
    resources = virtual(top, 'android/content/Context', 'getResources()Landroid/content/res/Resources;', context)
    # shortcut: only the top-level Settings list has icon rows; subpages (General, ...) do not.
    icon_id = virtual(top, 'android/content/res/Resources', 'getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I',
                      resources, text(top, 'icon'), text(top, 'id'), text(top, 'android'))
    icon_view = virtual(top, 'android/view/View', 'findViewById(I)Landroid/view/View;', holder, icon_id)
    has_icons = static(top, 'java/util/Objects', 'nonNull(Ljava/lang/Object;)Z', j.object(top, icon_view, VIEW))
    top.cbr(has_icons, place, (), done, ())
    # The row copies YouTube's preference layout: 18dp icon inset, 24dp icon, title at 60dp.
    row = new(place, 'android/widget/LinearLayout', '(Landroid/content/Context;)V', context)
    virtual(place, 'android/widget/LinearLayout', 'setGravity(I)V', row, integer(place, 16))
    row_view = as_view(place, row, 'Landroid/widget/LinearLayout;')
    virtual(place, 'android/view/View', 'setMinimumHeight(I)V', row_view, px(place, context, 54))
    pad(place, row_view, context, 18, 0, 16, 0)
    icon = new(place, 'android/widget/ImageView', '(Landroid/content/Context;)V', context)
    virtual(place, 'android/widget/ImageView', 'setImageDrawable(Landroid/graphics/drawable/Drawable;)V', icon,
            youtube_drawable(place, context, 'yt_outline_shield_empty_vd_theme_24'))
    row_group = cast(place, row, 'Landroid/widget/LinearLayout;', GROUP)
    title_view = label(place, context, text(place, 'YouTubeHideAds'), 'Subhead')
    # Tint the icon with the title colour, as YouTube's own row icons are.
    virtual(place, 'android/widget/ImageView', 'setImageTintList(Landroid/content/res/ColorStateList;)V', icon,
            virtual(place, 'android/widget/TextView', 'getTextColors()Landroid/content/res/ColorStateList;', title_view))
    icon_size = px(place, context, 24)
    virtual(place, 'android/view/ViewGroup', 'addView(Landroid/view/View;II)V', row_group,
            as_view(place, icon, 'Landroid/widget/ImageView;'), icon_size, icon_size)
    title = as_view(place, title_view, 'Landroid/widget/TextView;')
    pad(place, title, context, 18, 0, 0, 0)
    add(place, row_group, title)
    entry_name = chars(place, text(place, 'YouTubeHideAds'))
    virtual(place, 'android/view/View', 'setContentDescription(Ljava/lang/CharSequence;)V', row_view, entry_name)
    virtual(place, 'android/view/View', 'setTag(Ljava/lang/Object;)V', row_view, j.object(place, text(place, ENTRY_TAG), 'Ljava/lang/String;'))
    virtual(place, 'android/view/View', 'setOnClickListener(Landroid/view/View$OnClickListener;)V', row_view,
            callback(place, open_page, 'android/view/View$OnClickListener', 'onClick(Landroid/view/View;)V'))
    background(place, row_view, context, ITEM_BACKGROUND)
    virtual(place, 'android/view/ViewGroup', 'addView(Landroid/view/View;I)V',
            cast(place, parent, 'Landroid/view/ViewParent;', GROUP), row_view, integer(place, 0))
    j.log(place, 'Settings entry attached')
    place.br(done)
    done.ret()
    attach = j.finish(layout, ())

    # --- Focus hook: refresh the snapshot on any YouTube Activity; watch the Settings list.
    hook = j.block(f'L{API}XposedInterface$Chain;')
    chain = hook.params[0]
    result = interface(hook, API + 'XposedInterface$Chain', 'proceed()Ljava/lang/Object;', chain)
    argument = interface(hook, API + 'XposedInterface$Chain', 'getArg(I)Ljava/lang/Object;', chain, integer(hook, 0))
    focused = virtual(hook, 'java/lang/Boolean', 'booleanValue()Z', cast(hook, argument, 'Ljava/lang/Object;', 'Ljava/lang/Boolean;'))
    focus, done = j.block(), j.block()
    hook.cbr(focused, focus, (), done, ())
    receiver = interface(focus, API + 'XposedInterface$Chain', 'getThisObject()Ljava/lang/Object;', chain)
    activity = cast(focus, receiver, 'Ljava/lang/Object;', 'Landroid/app/Activity;')
    context = cast(focus, activity, 'Landroid/app/Activity;', CONTEXT)
    j.direct(focus, refresh, (context,))
    name = virtual(focus, 'java/lang/Class', 'getName()Ljava/lang/String;',
                   virtual(focus, 'java/lang/Object', 'getClass()Ljava/lang/Class;', receiver))
    match = virtual(focus, 'java/lang/String', 'equals(Ljava/lang/Object;)Z', name,
                    j.object(focus, text(focus, SETTINGS_ACTIVITY), 'Ljava/lang/String;'))
    locate, found = j.block(), j.block()
    focus.cbr(match, locate, (), done, ())
    resources = virtual(locate, 'android/app/Activity', 'getResources()Landroid/content/res/Resources;', activity)
    list_id = virtual(locate, 'android/content/res/Resources', 'getIdentifier(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I',
                      resources, text(locate, 'list_container'), text(locate, 'id'), text(locate, 'android'))
    holder = virtual(locate, 'android/app/Activity', 'findViewById(I)Landroid/view/View;', activity, list_id)
    have_list = static(locate, 'java/util/Objects', 'nonNull(Ljava/lang/Object;)Z', j.object(locate, holder, VIEW))
    locate.cbr(have_list, found, (), done, ())
    virtual(found, 'android/view/View', 'addOnLayoutChangeListener(Landroid/view/View$OnLayoutChangeListener;)V', holder,
            callback(found, attach, 'android/view/View$OnLayoutChangeListener', 'onLayoutChange(Landroid/view/View;IIIIIIII)V'))
    j.direct(found, attach, (holder,) + tuple(integer(found, 0) for _ in range(8)))
    found.br(done)
    done.ret(result)
    hook_fn = j.finish((f'L{API}XposedInterface$Chain;',), ('Ljava/lang/Object;',))

    params = (f'L{API}XposedInterface;', f'L{API}XposedModuleInterface$PackageReadyParam;')
    entry = j.block(*params)
    module, param = entry.params
    loaded = cast(entry, param, params[1], f'L{API}XposedModuleInterface$PackageLoadedParam;')
    first = interface(entry, API + 'XposedModuleInterface$PackageLoadedParam', 'isFirstPackage()Z', loaded)
    install, stop = j.block(), j.block()
    entry.cbr(first, install, (), stop, ())
    package = interface(install, API + 'XposedModuleInterface$PackageLoadedParam', 'getPackageName()Ljava/lang/String;', loaded)
    match = virtual(install, 'java/lang/String', 'equals(Ljava/lang/Object;)Z', package, j.object(install, text(install, YOUTUBE), 'Ljava/lang/String;'))
    ready = j.block()
    install.cbr(match, ready, (), stop, ())
    # Bindings, counters and default snapshot are published before any hook can fire.
    j.direct(ready, ad_install, (module, param))
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
    j.log(ready, 'YouTube lifecycle hook installed')
    ready.br(stop)
    stop.ret()
    function = j.graph.function(tuple(type_(d) for d in params), ())
    return {'function': function, 'objects': tuple(j.graph.objects.values())}
