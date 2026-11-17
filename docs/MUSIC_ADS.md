# YouTube Music ads

Build 160 extends the existing Premium switch to native Upgrade/account/membership/reference-mealbar
surfaces. [Premium controls, architecture and limits](MUSIC_PREMIUM_PROMOTIONS.md).

Build 159 adds [Music background playback](MUSIC_BACKGROUND_PLAYBACK.md) to the same shared settings
page under Player controls. The ad master controls only ads. The build 158 description and its
dated evidence below describe the earlier ads-only increment.

Development build 158 extends the existing module to `com.google.android.apps.youtube.music`.
This is the Hide Ads part of [issue #5](https://github.com/MrxSiN/YouTubeHideAds/issues/5).
Music SponsorBlock and the YouTube player/feed extras are not enabled in Music.
The released 1.3.0/build 157 predates this support.

## Host and policy boundary

The first-package entry selects exactly one host startup path. YouTube keeps its existing
feature installers. Music installs ad activation, component filtering, fullscreen filtering,
preference initialization and its settings entry. Both hosts share native-library initialization,
structural component/empty-component discovery, fullscreen discovery and the settings scaffold.
There is no APK patcher, conventional-language application implementation or on-device BF interpreter.

Music reuses the unchanged authored [AND3 policy](../source/brainfuck/and3.bf) and pinned native library.
Its three inputs are the effective setting, a matched ad fact and a validated context.
Only a successful native call returning exactly `01` authorizes suppression. The existing
BF `settings_snapshot` computes all five defaults and four master-gated switches.
The byte and host contracts are [music_ads_inputs.json](../contracts/music_ads_inputs.json).

Ad effects start disabled. A protective hook on the platform's
`Instrumentation.callApplicationOnCreate(Application)` reads preferences after the Application has
an attached Context and before its `onCreate`. Music's own Context stores preferences, so its switches
do not change YouTube's switches. Settings refreshes publish another complete BF snapshot.

## Discovery and effects

- Video/audio activation: uniquely anchor the media diagnostic, then require exactly one invoked
  `void(boolean)` method. An authorized call changes that argument to false and calls the original
  method. A native false argument, disabled setting or unsuccessful policy preserves the original call.
- General components: recognize explicit ad-carousel and sponsored-video component markers.
- Premium components: recognize Music's alert, paid-content overlay and statement-banner markers.
  A compact banner additionally needs a match at path index zero and the circle-button marker in
  that candidate's own serialized element. Payloads are bounded to 1 MiB; ancestor buffers are excluded.
- Fullscreen: reuse the existing bounded `_interstitial` extraction and BF fullscreen policy.
- Missing or ambiguous discovery preserves the affected surface. All hooks use protective exception mode.

No obfuscated class/member names, instruction offsets, numeric host resource IDs or version-only
selectors are embedded. The settings Activity and theme are public named host contracts; other roles
come from diagnostics, prototypes and typed relationships. The DexKit cache remains package-local.

## Settings

Open **Account → Settings → YouTube Hide Ads → Settings** in Music. Its ads-only page uses the same
entry, dialog, sections, rows, switch persistence and BF snapshot design as YouTube. Music's main theme
is resolved by name for those shared views because its settings theme does not provide every text-style
attribute. New Music labels have English resource defaults.

The existing dialog holder supplies only its page stack and dialog bookkeeping in Music. The shared
scaffold runs the SponsorBlock color-picker checks in YouTube only; Music does not initialize
SponsorBlock playback or networking to display its ad settings.

## Reference and scope

Behavior was checked against Morphe commit
[`44031c5`](https://github.com/MorpheApp/morphe-patches/tree/44031c561ea048c8f196877f30a49c13bfd6afb6):
[Music HideAdsPatch](https://github.com/MorpheApp/morphe-patches/blob/44031c561ea048c8f196877f30a49c13bfd6afb6/patches/src/main/kotlin/app/morphe/patches/music/ad/HideAdsPatch.kt),
[fingerprints](https://github.com/MorpheApp/morphe-patches/blob/44031c561ea048c8f196877f30a49c13bfd6afb6/patches/src/main/kotlin/app/morphe/patches/music/ad/Fingerprints.kt),
and [AdsFilter](https://github.com/MorpheApp/morphe-patches/blob/44031c561ea048c8f196877f30a49c13bfd6afb6/extensions/music/src/main/java/app/morphe/extension/music/patches/components/AdsFilter.java).
This is an independent runtime adaptation; no Morphe Java/Kotlin code or patcher is bundled.
The existing [notice](../LICENSES/Morphe-NOTICE.txt) is retained in the APK.

The native **Upgrade** tab, **Get Music Premium** account/settings entries and native Premium
bottom sheets without a recognized serialized ad payload remain unchanged. This increment does not
claim full Morphe parity or support for every Music version.

[Build and device evidence](../evidence/music_ads_20261116/README.md) distinguishes startup checks,
actual UI/playback observations, development packaging and remaining untested surfaces.
