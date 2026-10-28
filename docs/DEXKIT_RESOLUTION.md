# DexKit resolution

Background playback adds five validated runtime roles, with typed opcode/numeric fingerprints,
dynamic background resource IDs and explicit caller deoptimization. Its full discovery contract,
runtime contexts, fail-closed publication and observed-version limits are in
[BACKGROUND_PLAYBACK.md](BACKGROUND_PLAYBACK.md). Obfuscated names in evidence are observations only.

Since build 152, DexKit answers are cached in YouTube's `code_cache` and keyed by DexKit's own
serialized query bytes; the cache is discarded when YouTube's base.apk or the module APK changes.
Every role below is still validated on each start. [Design and checks](../evidence/device_perf_20261028/README.md#dexkit-result-cache-build-152).

DexKit 2.3.0 is bundled as third-party DEX/native input. Discovery and reflection are XAX. This guide describes build 77; obfuscated names below are
observations on YouTube 21.41.525, never hardcoded selectors. [Compatibility](COMPATIBILITY.md).

| Role | Required discovery evidence |
| --- | --- |
| Video activation | Both TriggerBundle/ping-migration strings, one argument, void |
| Player ad layout | PlayerBytesLayout ad-count diagnostic, one argument, void |
| Component parser | Two element-type diagnostics, six arguments; unique context field; typed EmptyComponent factory/result |
| Premium measure | Named CompactYpcOfferModuleView onMeasure(II)V |
| Fullscreen dialog | Public/final void, byte-array/reference arguments, invokes show and Activity.isDestroyed |
| Engagement panel | Exact initialization diagnostic, private/final, two reference plus two Boolean arguments; reference return |
| Panel ID helper | Unique invoked static String method taking exactly the controller's request type |
| Shorts ad selection | Both minTsla-empty and missing ReelPageAdsInterface diagnostics; private/final void, zero arguments |
| Shorts feed removal | ReelPageAdapter getItemViewType diagnostic and unique List transformer; paired append method from emergency-buffer diagnostic; typed insert and response callers; ReelToReelList diagnostic and both constructors; native classifiers from ReelPageAdsInterface diagnostics |
| Player progress | Exact media-progress diagnostic, void, eight arguments |
| Video ID | Response String getter called by the player-byte diagnostic |
| Response/streaming data | Typed getter relationships with the uniquely anchored player initializer |
| Seek | Both seek diagnostics, Boolean result, long plus enum arguments; first enum constant is SEEK_SOURCE_UNKNOWN on tested APK |
| Current asset | Public/final zero-argument player getter returning the same asset interface |

Resolvers require unique roles. Shorts resolves all feed roles before installing its five removal
hooks. Missing or unexpected candidate counts leave that feature unchanged. No automatic pager
navigation, page visibility changes or layout/scroll observer is installed.
Hooks use protective libxposed exception mode. No obfuscated class name is a selector.
Numeric duration/type fields are read from validated VideoStreamingData formatting; missing fields
fail closed, and full streaming data/DRM fields are never logged. Progress argument 2 is position;
argument 3 is buffered extent, not video duration.

The panel uses the typed identifier helper, not protobuf toString. Null requests or identifiers at
least 1,024 characters long pass. The BF ad_panel library decides PAproduct/jumpahead gating.
Controlled PAproduct and jumpahead protobuf calls pass through the actual panel hook.
A naturally delivered panel-blocking case remains pending.

No persistent resolver cache or general hot-unhook lifecycle is implemented. Factory YouTube
21.18.164 differs in player anchors and is not certified.

## Playables and fullscreen swipe discovery

Playables drawer classification resolves one zero-argument byte-array serializer that invokes
UpbMessage.jniEncode(JJ)B. Only a more_drawer root CellType is serialized, with a 1 MiB bound;
FEmini_app_destination must belong to that individual row. Generic parent buffers are not used.
The shared component hook also recognizes horizontal_gaming_shelf.e and mini_game_card.e.
A fresh preference read for matching components honors a disabled toggle across a cold start.

Swipe discovery uniquely anchors the player-type enum initializer with WATCH_WHILE_FULLSCREEN,
then finds the unique void, one-enum-argument setter on YouTubePlayerViewNotForReflection.
The player View supplies its actual Activity through at most eight ContextWrapper steps.
That Activity's dispatchTouchEvent method is hooked once and guarded by Activity identity.
The manifest launcher is an alias and is not used as a class selector. Missing or ambiguous
bindings leave native touches unchanged. Build 67 passed startup and actual fullscreen gesture calibration on the Pixel;
the runtime binding is com.google.android.apps.youtube.app.watchwhile.MainActivity.

## Feed context and own-element classification

The existing component parser's path Field identifies ConversionContext. Its diagnostic formatter
must contain widthConstraint, heightConstraint and horizontalCollectionSwipeProtector labels.
The two unique nonstatic Integer fields used by that formatter identify width then height. A
unique interface field must expose boolean(RecyclerView, MotionEvent), supporting both support-v7
and AndroidX RecyclerView. Pixel bindings are height=d and touch=k; these names are observations,
not selectors. Missing/ambiguous fields preserve feed content.

The feed guard requires null horizontal swipe protector or null height constraint. Generic root
horizontal shelves, root shelf headers and chips_shelf candidates use the already-resolved typed
element serializer, bounded to 1 MiB. The specific preview/topics headings must occur in that own
payload. Root headers additionally recognize exact length-prefixed Shorts/Posts titles. This
preserves ordinary shelves and History chips. No view-tree, scrolling or pager-navigation hook is
added. [Live proof and locale limits (`feed_filters_20261017`, removed before 1.0.0).

## AI context reuse

AI filtering reuses the existing component serializer and discovered feed context fields. Root-card
path and whole-handle checks run against the candidate's own bounded bytes; no additional navigation
or ancestor-buffer resolver is installed. Search root cards and allowed Home/related contexts are
validated before BF authorization. Channel rows and playlists do not match the root-card gate.
[AI contract](../contracts/ai_channel_inputs.json).

## Original-audio resolution (build 77)

Resolve the unique formatter containing id/displayName/isAutoDubbed/isDefault; validate a four-field
record with two Strings and two booleans. Resolve the void one-argument audio update method by
menu_item_audio_track and a typed record-array field on its object argument. Primitive overloads
are rejected. From the audio-item callback referencing the record ID, require one invoked void
String setter and a unique controller field of that setter's owner type on the update owner.

Pixel 21.41.525 bindings: record akzk (ID a, auto-dubbed c), update armt.a(aovk), aovk.g:[Lakzk,
controller armt.a:asfu and setter asfu.N(String). These names are observations, not selectors.
Missing/ambiguous roles preserve native audio. The callback runs after the original format update,
on the main thread, and only after the 60-case readiness gate. No network/player-response spoofing
is involved. See the [original-audio contract](../contracts/original_audio_inputs.json) and
[build 77 device evidence](../evidence/ai_audio_branding_20261018/README.md).
