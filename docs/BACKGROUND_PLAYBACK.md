# Background playback

Released in **1.1.0** (first implemented in development build 131; fixed for YouTube 21.43 in 1.2.0), this feature runs in the stock YouTube process.
It needs the existing API 102 module, not a patched YouTube APK or a Morphe installation.
[Build and test evidence](../evidence/background_playback_20261027/README.md).

The independent **Background playback** switch is under **You → Settings → YouTube Hide Ads →
Player controls**, defaults on, and uses the existing `youtubehideads` preferences and switch
callbacks. Its summary is: “Allow videos to continue playing when YouTube is in the background
or the screen is off, including Made for Kids videos.” The existing reset clears its key and
restores the on default. Restart YouTube after changing it: callbacks read the saved switch on
each evaluation, but YouTube can cache capability and experiment values.

## Reference and scope

Research used Morphe commit `f3acc10e2691ffc4db29c6a6a651ee61fb54c047`:

- [Patch](https://github.com/MorpheApp/morphe-patches/blob/f3acc10e2691ffc4db29c6a6a651ee61fb54c047/patches/src/main/kotlin/app/morphe/patches/youtube/misc/backgroundplayback/BackgroundPlaybackPatch.kt)
- [Fingerprints](https://github.com/MorpheApp/morphe-patches/blob/f3acc10e2691ffc4db29c6a6a651ee61fb54c047/patches/src/main/kotlin/app/morphe/patches/youtube/misc/backgroundplayback/Fingerprints.kt)
- [Extension](https://github.com/MorpheApp/morphe-patches/blob/f3acc10e2691ffc4db29c6a6a651ee61fb54c047/extensions/youtube/src/main/java/app/morphe/extension/youtube/patches/BackgroundPlaybackPatch.java)
- [21.41 support change](https://github.com/MorpheApp/morphe-patches/commit/95eb1fbabe8bdb6251c20b962142cd4daefc1e47),
  which changes the settings fingerprint for 21.23+.

Morphe replaces regular-video eligibility returns, allows a background settings capability,
skips the kids background-policy controller, and disables automatic foreground resume. These
operations have method boundaries suitable for runtime hooks. This adaptation uses those boundaries.
It does not transplant the patcher, extension, player-controller interfaces or bytecode insertion.

Morphe also contains optional Shorts, auto-pause-on-lock, flyout-pause, older PiP and player-controls
flag changes. Those are outside this feature. In particular, the broad older player-type flag is
not overridden: upstream warns that it removes the seekbar on 21.36+.
Age verification, DRM, Premium entitlement, account security and media-session/audio-focus APIs
are not intercepted. The scoped flag hook passes every experiment except `45770945` unchanged.

The fingerprints derive from Morphe/ReVanced. The [Morphe notice](../LICENSES/Morphe-NOTICE.txt)
is preserved in source and in the APK's `res/raw/morphe_notice.txt`. This is a separate native
adaptation; neither upstream project publishes this module.

## Brainfuck authorization

The feature reuses the authored and pinned [AND3 policy](../source/brainfuck/and3.bf), unchanged
at the executable-command level. No new native dependency or ABI migration is needed.
The inputs are own enabled switch, validated restriction-gate fact, and validated context.
The existing JNI transport must return status zero and **exactly** one byte `01` before an override.
Unknown facts, failed readiness, empty/wrong replies and disabled settings preserve native behavior.

[Contract](../contracts/background_playback_inputs.json) ·
[Vectors](../testdata/background_playback_vectors.json).

There are 28 new packaged startup checks: all eight Boolean inputs, fourteen player-name cases
and six experiment ID/namespace cases. They supplement the unchanged 636 existing checks.
The native Boolean gate, string classifier and flag classifier used in the checks are the same
ones used by the hooks. No fallback policy or interpreter ships.

## XAX discovery and actions

The canonical store adds 19 typed functions and `BackgroundBindings`. Only startup initialization,
the existing preference refresh and the main settings page change among existing function bodies.
Other ad, SponsorBlock, original-audio and swipe callback graphs remain unchanged.

Since build 153 the player-context observer alone is installed during startup discovery, before any
Activity exists, so a player created before the worker finishes (a video opened from a link) is still
observed. It records state only; the worker still validates every role and gates every override.
[Diagnosis](../evidence/device_perf_20261028/README.md#background-playback-from-a-link-build-153).

One worker starts on the first normal Context refresh. It retains the application Context,
APK path and class loader, opens its own DexKit bridge and closes it on completion or failure.
The existing startup bridge has already closed before that Context is available; sharing it
would race its lifetime. Discovery adds no main-thread DEX scan, polling, service or wake lock.

| Role | Structural requirements | Authorized action |
| --- | --- | --- |
| Regular manager | Boolean return, one reference parameter, public static, full upstream 25-opcode sequence and integer `64657230` | Preserve native true; allow native false only for a non-null argument and valid regular-player context |
| Kids controller | Void return, int/reference/reference parameters, public final instance method, upstream eight-opcode sequence and integer `5`; second parameter is the discovered player enum, third is a reference | Skip this restriction controller only with both object arguments present and valid regular-player context |
| Background settings | Object(Object) caller using both background-category string resource IDs, resolved by resource name; unique instance Boolean no-argument callee excluding `java.lang.Boolean` | Allow that background capability |
| Foreground resume | Unique Boolean no-argument method using long `45770945`; unique invoked instance Boolean accessor with `(int,long,boolean)` or verified legacy `(long,boolean)` parameters | Return false only for that key, with namespace `288` for the current signature |
| Player context | Enum initializer containing the fullscreen, inline and PiP names; unique typed updater on YouTube's public player View class | Observe the returned native state and retain a weak View reference |

DexKit numeric matchers preserve literal types: protobuf/resource constants are Integers and
the experiment is a Long. Repeated invokes of the same accessor are deduplicated by DexKit's
encoded method identity; distinct candidates still reject. Reflection confirms the static/instance
modifiers and the kids/player enum relationship. Names such as `aqug.y` are diagnostics, never selectors.

All required roles resolve and validate before installation. Relevant direct callers and methods
containing the resume experiment are deoptimized, with a 128-caller bound; failures leave readiness
false. Hooks use libxposed's protective exception mode. Readiness becomes true only after the
complete hook installation; callbacks from a partial installation remain inactive.

Playback overrides require the main thread, an observed recognized regular-player state and a
live weak player View. None, hidden, inline, dismissing and unknown states reject. A visible
`reel_watch_player` under that View's root rejects the regular-player override. Settings and
experiment checks use their own validated method/argument contexts, so they do not need a playing
video. No decision depends on the ad master or SponsorBlock.

The host grants capabilities and removes the kids gate. YouTube still starts, pauses and terminates
playback, owns its media notification and lock-screen controls, and handles audio focus. There is no
module play command, delayed resume, retry timer or restart loop. Native pauses remain native pauses.

## Diagnostics and limits

Logs include `Background playback self-check (28 cases)=true`, candidate methods, complete hook
installation, and the first authorization for each of eligibility, kids policy, settings capability
and foreground resume. Missing/ambiguous roles and worker exceptions log native preservation.

Runtime acceptance currently covers Pixel 8 Pro, Android 17, Vector 2.2/API 102 and YouTube 21.43.523
(build 154: the settings callee must be declared in a YouTube default-package class) and YouTube
21.42.243. The 21.41.525 APK and legacy accessor were inspected; this change was not installed
against that version. Pre-21.23 settings fingerprints are unsupported and fail closed.
Off-main-thread or unknown player calls preserve native restrictions. Discovery begins after a
Context exists; already cached native capabilities may require a process restart.

Physical Bluetooth controls, incoming calls, real audio-focus interruptions, other YouTube
versions/frameworks/devices and mixed regular/Shorts stacks need separate device verification.
See the dated evidence for what was actually exercised and what remains untested.
