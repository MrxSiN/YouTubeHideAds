# YouTube Music background playback

Development build **159** adds **Remove background playback restrictions** to the stock Music
process. It follows YouTube's existing boundary: authored Brainfuck authorizes each override;
canonical XAX owns structural discovery, preferences, callbacks and native UI. It uses the same
module and shared settings scaffold as Music ad hiding. No Music APK is patched.

Open **Account → Settings → YouTube Hide Ads → Settings → Player controls → Background playback**.
The independent switch defaults on, matching YouTube. It uses `background_playback` in Music's own
`youtubehideads` preference file. Changing it does not change YouTube's preference or depend on
Hide ads. Restart Music after changing the switch because Music can cache capabilities. Clearing
the preference through the existing preference lifecycle restores the on default; this increment
does not add a Music reset control.

## Discovery and lifecycle

Music's existing package dispatch initializes the native libraries and package-local DexKit session.
Background discovery reuses that session during startup and closes no shared resource itself.
It uses YouTube's completed-future/continuation startup pattern on the calling thread, preserving
the shared DexKit lifetime. An unexpected discovery or installation exception resets background
readiness and logs preservation while Music's ad and settings startup continues.
The existing Instrumentation Application callback publishes the attached Music Context before
application `onCreate`. No extra worker, observer, service, timer, polling or wake lock is added.
YouTube's player-context observer and its background installers remain specific to YouTube.

| Role | Structural contract | Authorized action |
| --- | --- | --- |
| Eligibility | Unique `ZL` shorty, the upstream nine-opcode sequence and integer protobuf discriminator `64657230`; reflection requires public static and a reference parameter | Keep native true; replace native false with true only for a non-null argument and validated Music Context |
| Kids policy | Unique `VILZ` shorty and long experiment anchor `45638079`; reflection requires public final instance and an enum second parameter | Skip this controller only for a non-null receiver and enum argument with validated Music Context |

Both roles must resolve uniquely and pass reflection checks before installation. Their direct callers
are deoptimized through the existing bounded helper (at most 128 per role), and deoptimization of
both target methods must succeed. Both callbacks use libxposed API 102 protective exception mode.
The separate `MusicBackgroundBindings` holder publishes readiness only after all checks and both
installations succeed. A callback installed before an installation failure remains inactive.
Obfuscated names in device evidence are observations, never selectors. Numeric literals are named
structural contracts, not instruction offsets or resource IDs.

## Policy and native behavior

The unchanged [AND3 policy](../source/brainfuck/and3.bf) receives three Boolean bytes: the saved
independent setting, validated restriction fact and validated call context. XAX accepts only status
zero and an exact one-byte `01` reply. The same typed native gate used by YouTube is shared without
changing its graph or its library. Missing Context, another package, null arguments, disabled settings,
failed policy checks and incomplete readiness preserve native behavior.

The eligibility callback calls the original first and preserves a native true result. The kids callback
proceeds normally when authorization fails. A two-slot atomic counter reports the first authorization
of each role; it logs no playback identifiers. Music continues to own playback, pause, stop, audio focus,
the notification and lock-screen controls. The module issues no play, resume or seek command and adds
no global experiment, entitlement, subscription, DRM or account hook.

Twelve packaged startup checks exercise all eight Boolean combinations through the actual BF/JNI
boundary and four host-name cases through the runtime classifier. They are separate from Music's
existing 96 ad checks. [Contract](../contracts/music_background_playback_inputs.json) and
[fixtures](../testdata/music_background_playback_vectors.json) distinguish startup tests from
integration acceptance requirements.

## Upstream reference and limits

Inspected Morphe revision
[`44031c5`](https://github.com/MorpheApp/morphe-patches/tree/44031c561ea048c8f196877f30a49c13bfd6afb6):
[Music patch](https://github.com/MorpheApp/morphe-patches/blob/44031c561ea048c8f196877f30a49c13bfd6afb6/patches/src/main/kotlin/app/morphe/patches/music/misc/backgroundplayback/BackgroundPlaybackPatch.kt)
and [fingerprints](https://github.com/MorpheApp/morphe-patches/blob/44031c561ea048c8f196877f30a49c13bfd6afb6/patches/src/main/kotlin/app/morphe/patches/music/misc/backgroundplayback/Fingerprints.kt).
Its two method-boundary actions are adapted to protective runtime hooks. Its patcher, extension,
settings implementation and Java/Kotlin code are not bundled. The existing GPL/Morphe notice is
retained in source and APK resources.

Morphe also depends on a shared recycled-bitmap metadata fix. That separate behavior is not adapted
here; any bitmap crash during broader media-notification use requires separate diagnosis. This
increment does not claim complete Morphe dependency parity, other Music versions or device-wide
interruption handling. [Dated build and device evidence](../evidence/music_background_20261116/README.md)
records what actually ran, rejected attempts and untested cases. Release 1.3.0/build 157 predates
Music support; no new release is implied by this development feature.
