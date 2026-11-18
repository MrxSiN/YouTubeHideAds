# YouTube Music audio playback

Development build 163 adds **Exclusive audio playback** (on by default) and **Enable Audio/Video
switch** (off by default) to Music's existing module settings under Player controls. Both switches
are independent of ad hiding and background playback. Restart Music after changing them.

Exclusive audio enables the structurally discovered audio-only capability and removes the external
controller's playback restriction. The shared predicate is overridden only when the discovered
external controller is on the current bounded stack. Its ordinary phone-player callers retain
native behavior. This does not grant a server subscription or change offline entitlements.

Enable Audio/Video switch lets a tap in the **left half** of Music's native Song/Video pill select
the matching version in either direction. The right half keeps its native action: selecting a video
version can retain Music's audio-only presentation until you use that native control. Searches use
public metadata, take place off the main thread and can fail when no verified counterpart is
available. The setting does not automatically replace songs or videos while a playlist advances.

## Native queue and lifecycle

The implementation follows the repository's existing XAX discovery, weak host bindings, settings
rows and Brainfuck authorization. It does not package Morphe Java/Kotlin or a patching runtime.
Unique structural roles identify enqueue, storage, current index, local mode, displayed queues,
removal, video IDs and the queue executor. Ambiguous or missing roles decline the custom switch.
The constructor hook captures the manager weakly; operations require a live LOCAL queue.

A job captures the current ID, index and exact item identity. Public oEmbed and Android Music
search identify the opposite ATV/OMV type using Morphe's normalized title score. This adaptation
also verifies the candidate's normalized publisher through its own oEmbed result before accepting
it. Verified pairs are cached in both directions for the life of the process, with 600 entries.

The worker rechecks the source, enqueues PLAY_NEXT on the queue executor, waits for the requested
next item, dispatches media NEXT on main, and waits for actual advancement. Only then may it remove
the exact previous source entry. Source changes, Activity pause, a disabled preference, changed
manager/index and expired waits prevent further switching. Rollback may remove only an observed
newly inserted next item absent from the original identity snapshot; an existing playlist item is
never a rollback target. Uncertain queue state is left alone.

The Activity dispatcher follows YouTube's existing gesture architecture. Named runtime resources
beneath the native player identify the pill. A new touch-down may refresh a stale Activity binding
only from Music's focused, shown and attached window. Unclaimed gestures continue through the
original dispatcher; claimed gestures retain ownership through cancellation or release. Pause and
player replacement clear gesture state. Activity, root and queue references are weak.
Single-pointer gestures obey Android touch slop. One job may run
at a time; mutation callbacks check the published job identity, and old callbacks cannot act on a
later job or release its lock. Successful cleanup is observed separately from queue advancement.

Requests have bounded connection/read timeouts, response bytes, body deadlines and JSON traversal.
They use no cookies, account credentials or API key. Logs contain static feature outcomes, never
titles, account data, requested IDs or URLs. Exact bounds and byte contracts are in
[the input contract](../contracts/music_audio_inputs.json); synthetic expected vectors are in
[the fixture data](../testdata/music_audio_vectors.json).

## Reference and limits

Reference: Morphe main
[`31234a8465683a389bcfba25ad636fd1cd38fd02`](https://github.com/MorpheApp/morphe-patches/tree/31234a8465683a389bcfba25ad636fd1cd38fd02):

- [Exclusive audio](https://github.com/MorpheApp/morphe-patches/tree/31234a8465683a389bcfba25ad636fd1cd38fd02/patches/src/main/kotlin/app/morphe/patches/music/misc/audio).
- [Audio/Video switch and queue ABI](https://github.com/MorpheApp/morphe-patches/tree/31234a8465683a389bcfba25ad636fd1cd38fd02/patches/src/main/kotlin/app/morphe/patches/music/misc/audiovideoswitch).
- [Switch extension](https://github.com/MorpheApp/morphe-patches/blob/31234a8465683a389bcfba25ad636fd1cd38fd02/extensions/music/src/main/java/app/morphe/extension/music/patches/EnableAudioVideoSwitchPatch.java).

Morphe's optional Always play song behavior is outside this increment. This implementation also
declines when native queue operations are unavailable, including remote/Cast queues; it does not
fall back to opening a new mix through a deep link. Exact publisher checking can reject legitimate
versions uploaded by different publishers. Public search results can change. Attribution remains
in [Morphe-NOTICE](../LICENSES/Morphe-NOTICE.txt) and the packaged branding resources.
