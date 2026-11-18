# Music Premium controls: build 160

Native authoring and builds ran on **2026-11-16**. Final physical-device acceptance ran on
**2026-11-17** after the owner reconnected and unlocked the phone. This record covers development
build 160, not the released 1.3.0 APK. [Build identities](build.json),
[device identity](device.json) and [acceptance summary](acceptance-summary.json) identify the exact
source and separately signed device APKs.

## Executed build and integrity checks

- **EXECUTED:** pinned native Windows compiler `edit` and mandatory `verify` for four
  [exact-root stages](../../source/xax/transactions/music-premium-20261116/manifest.json).
  Independent replay reproduces final canonical bytes. A stale input returns status 1 and the
  [structured stale-root diagnostic](stale-root.txt), rather than publishing a store.
- **EXECUTED:** native resolve/build of the production-package unsigned APK, plus native signed
  builds of Music-only and temporary YouTube-only development packages. The installed Music APK
  SHA-256 matches the accepted build. All four DEX files, eleven native libraries and eleven static
  `res/` files match across production/development variants; manifests, namespace resources and
  signatures intentionally differ. Native libraries and third-party DEX match build 159.
- **EXECUTED:** [graph preservation](native-checks.json): 508 baseline functions, 545 final;
  498 baseline function CIDs retained. The ten changed existing functions are exactly the three
  direct edits (Music startup, version text, Music summary) and their content-addressed ancestors.
  Shared BF, hook, reflection and DexKit helper identities are unchanged.
- **NOT RUN:** release signing; the private capability matching the release certificate is
  unavailable. The device package is `io.github.mrxsin.youtubehideads.musicdev`, versionCode 17,
  using the existing separate development signer. No release was published.

The source root is `92e1250946969d4ff7533b4f8cbc0750ea0fc0f15f3c3c1fb263af407ca6e144`;
source SHA-256 is `4768fd4586c197dcc6a6bf839c21bea37cfcc17ae650ad1929252add60d8e37c`.
Current exact pins and the reason for retaining the compiler pin are in
[toolchains.json](../../toolchains.json). Latest XAX main was checked again on November 17; its
changes since the pin are handoff/state documentation only. Compiler, SDK and seed are unchanged.

## Physical phone acceptance

Pixel 8 Pro, Android 17/API 37, Music **9.45.51**, YouTube **21.45.88**, the existing Vector 2.2/API 102
setup. These are physical-device runs, including the wireless ADB connection on November 17.

| Check | Evidence and result |
| --- | --- |
| Music policy/startup | **EXECUTED:** fifteen Premium checks, twenty-six Music ad checks and twelve background checks logged; all four Premium roles resolve and install. [Runtime log](music-runtime.log) |
| Premium enabled | **EXECUTED:** Upgrade tab and Get Music Premium account/settings entries absent; native Home/Search/Library labels and shared settings remain. [UI record](music-ui.json) |
| Premium disabled | **EXECUTED:** saved off value survives restart; Upgrade and account/settings Premium entries return. |
| Hide ads master disabled | **EXECUTED:** Premium preference remains on, while native promotional entries return. Restoring master and restarting hides them again. |
| Shared settings | **EXECUTED:** all six switches remain available and finish on. [Final screenshot](module-settings.png) |
| Ordinary playback | **MEASURED:** foreground, Home and verified Dozing screen-off states remain PLAYING; native pause reports position 23,649 ms. [Playback samples](music-playback.json) |
| Kids playback | **MEASURED:** Baby Shark request remains PLAYING on Home; native pause advances to 10,031 ms. Kids-controller authorization is logged. Screen-off was not repeated on this final APK. |
| YouTube regression | **EXECUTED:** all 664 startup and 64 native settings UI cases pass; unified settings and Back work. [Result](youtube-regression.json), [log](youtube-regression.log) |
| Isolation and cleanup | **EXECUTED:** YouTube preference checksum unchanged; original YouTube module re-enabled; temporary regression module uninstalled. Final Music playback is paused. Original free rotation and 600,000 ms screen timeout restored. |

Final scoped runtime logs contain no hook/discovery errors, failed self-checks or fatal exceptions.
Earlier candidates and interrupted UI automation are not used as acceptance for the final artifact.
One earlier candidate encountered an unnamed floating view; the final resource-identity stage
compares runtime named IDs and the final playback runs no longer trigger that failure.

## Limits and test setup

- **NOT RUN:** naturally served reference promotion mealbar; that exact presentation was not
  delivered. Its structural hook is implemented and resolves, but this record does not certify a
  live positive. Other Music versions, account states and arbitrary server UI are not certified.
- **NOT RUN:** injected ambiguity/deoptimization/exception failures. The guarded normal path and
  native semantic graph were checked; this is not execution evidence for every failure branch.
- The separate audio/video-switch `upsell.eml` trial BottomSheet remains unsupported. A native
  full-page welcome offer was also served on November 17 and manually dismissed with **No thanks**
  before UI acceptance. Neither is reported as removed. No purchase flow was entered.
- Screen-off caused a secure lock; the owner unlocked the phone before final UI acceptance.
  Kids Home/pause and all UI checks ran before the final ordinary screen-off test. Earlier build
  159 kids screen-off measurements remain scoped to [that dated record](../music_background_20261116/README.md).

[Design and reference scope](../../docs/MUSIC_PREMIUM_PROMOTIONS.md) ·
[Contract](../../contracts/music_premium_inputs.json) ·
[Fixtures versus requirements](../../testdata/music_premium_vectors.json)
