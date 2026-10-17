# Architecture

Release 1.0.0 (versionCode 100): 123 functions, 11 native paths (9 policy libraries plus JNI bridge and DexKit), one pinned
branding input. [Exact build](../evidence/ai_audio_branding_20261018/build.json) · [Settings/defaults](README.md#settings-and-defaults)

Annotated Brainfuck is compiled by external brainfuckC into AArch64 bfc_call_v1 libraries.
The canonical XAX store becomes DEX, manifest, libxposed metadata and a signed APK.
YouTube hooks supply facts through XAX/Bfp1Bridge; exact Brainfuck replies authorize typed actions.

The canonical store owns Android/libxposed, DexKit, reflection, settings, HTTPS/JSON and byte
transport. One component extractor serves parser and fullscreen callbacks. The engagement hook uses
YouTube's typed identifier helper instead of protobuf text. Brainfuck owns final ad/category authorization,
ad/SponsorBlock defaults and master gating, and timestamp-window comparisons. Independent content/
player preference defaults and structural string/context classification are XAX operations.

Fifteen policy library paths ship, plus the external JNI bridge and DexKit; identical AND3
policies share pinned input bytes under separate semantic names. There is no on-device BF
interpreter. Startup runs 531 checks: 70 ad, 277 SponsorBlock, 24 Playables, 28 swipe, 72 feed and 60 AI/audio
cases through the actual packaged libraries/JNI and host classifiers. Failed checks disable the
corresponding feature.

SponsorBlock uses a single worker and CompletableFuture exception handling. A fixed HTTPS endpoint
receives a four-hex-digit SHA-256 prefix. The complete response is bounded to 256 KiB and 1,024 video
records, with at most 100 segments for the exact local video ID. Read/connect timeouts are four
seconds; an elapsed deadline and read-count limit bound successful reads. Redirects are disabled.
Connections disconnect on completion, including errors. Failed or absent data produces no seek.

SponsorBlock requests stay disabled until the first saved-preference refresh.

One request is attempted per playback generation; there is no cross-video cache or automatic retry.
An in-flight request finishes into its original job. The current player never consumes a previous
job's response. Main-thread checks bind the player instance, video ID and CPn generation token,
and revalidate the current asset immediately before a BF-authorized seek. Completed UUIDs prevent
repeated seeks within the same generation. Unknown playback types fail closed.

There is no Activity. The page attaches inside YouTube Settings; preferences live in YouTube storage.
Clearing YouTube data resets them. Category defaults are enabled/sponsor/selfpromo on; others off.

Feed filters share the existing typed component replacement hook. FeedBindings owns only context
roles and readiness; classification, per-section preferences and native authorization remain
separate functions. The resolver reuses the existing DexKit lifetime and typed serializer. Feed
changes add no worker, scrolling observer or player callback. [Feed contract](../contracts/feed_section_inputs.json).

AI filtering reuses the component hook, own-element serializer, context guard and typed empty
component factory. Previously authorized ad/feed removal returns first; AI failure cannot undo it.
Separate functions parse handles, match sets, fetch/cache public lists and authorize via BF. The
high-confidence and warnlist preferences are independent and default off. Requests run as two bounded
CompletableFutures with separate connections; successful sets persist for four hours. No video data
is sent. ExtraBindings holds immutable published sets, request state and audio bindings/readiness.

Original audio resolves the typed format-record array, update callback, current controller and its
String setter through a single DexKit lifetime. After the update, the main-thread callback requires
2..128 tracks and exactly one non-dubbed `.4` ID. BF authorization precedes the setter. A weak
controller plus array equality avoids repeated changes and respects a manual choice on the same list.
Unknown bindings preserve native behavior. Settings/reset and persistence reuse the existing builders.

## Static resources and lifecycle

The settings page attaches to YouTube; there is no module Activity or permission request. Static
branding XML supplies the exact YoutubeHideAds title, short description and adaptive/monochrome
shield icon. AAPT2 compiles these resources; the external branding-v2 profile packages their pinned
archive alongside XAX-generated DEX. See [BUILD.md](BUILD.md).

Discovery requires unique typed roles; missing/ambiguous bindings leave that feature unchanged.
Process-local caches/state are rebuilt on restart; only preferences and AI list caches persist.
There is no persistent DexKit resolver cache or general dynamic hot-unhook lifecycle.
