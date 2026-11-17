# Native Music welcome: build 161

This November 17 session adds native welcome-offer cancellation to build 160. Exact source,
APK identities and payload comparisons are in [build.json](build.json); physical environment and
cleanup are in [device.json](device.json). This is an unreleased development build, not a release APK.

## Native build and replay

- **EXECUTED:** three [exact-root transactions](../../source/xax/transactions/music-welcome-20261117/manifest.json),
  native verification, independent byte-identical replay and [stale-root rejection](stale-root.txt).
  The pinned native Windows compiler ran with `XAX_REQUIRE_NATIVE=1`. SDK use was inspection and
  declaration/metadata serialization, not application lowering or mutation.
- **EXECUTED:** native production unsigned build and separately signed Music/YouTube development
  builds. All four DEX files, eleven native libraries and eleven static `res/` files match between
  production and final development variants. Native libraries and third-party DEX match build 160.
- **EXECUTED:** [graph checks](native-checks.json): 545 baseline functions, 563 production functions,
  535 baseline CIDs retained. Existing changes are exactly Music startup, version/summary literals
  and their content-addressed ancestors. The five-node main-thread helper reads no player state.
- **EXECUTED:** independent [fixture replay](../../source/xax/transactions/music-welcome-20261117/fixtures/manifest.json).
  The fixture retains 561 of 563 production function CIDs; only the startup wrapper and its
  content-addressed ancestor change. Production scheduling, validation, BF authorization and cancel
  functions are identical. The fixture APK's generated DEX differs and is explicitly not the final APK.

Canonical source SHA-256: `8e23c7e9cf8d5b0a795af4cd982febe6a269be8d5c53df587fc914b4926a3175`.
Root: `6564126c8c89dca70612256cd0b4cf118a51261b527b22a77e58d68ef6c091b0`.
[Toolchain pins and retention reason](../../toolchains.json).

## Controlled host-layout execution

**EXECUTED** on physical Pixel 8 Pro, Android 17/API 37, Music 9.45.51, the existing Vector 2.2/API 102
setup. The separate fixture APK inflates Music's real layouts, installs controlled cancel/action
listeners and invokes the unchanged production scheduler before attaching the candidate beneath
Music's interstitial container. Cancellation removes that controlled view and restores visibility.
No purchase endpoint is connected to the fixture action.

| Case | Automatic cancel callbacks | Result |
| --- | --- | --- |
| Premium/master on, standard promo layout | 1 | Removed |
| Premium/master on, onboarding promo layout | 1 | Removed |
| Education layout | 0 | Preserved; manually closed for cleanup |
| Lookalike view with unmatched layout identity | 0 | Preserved; manually closed |
| Premium off | 0 | Preserved; manually closed |
| Master off, Premium saved on | 0 | Preserved; manually closed |
| Settings restored on | 1 | Removed |

All seven cases also verify the account menu remains interactive after cleanup. The action listener
was never invoked. [Case results](controlled-fixtures.json) · [Scoped runtime log](fixture-runtime.log).
An earlier candidate selected a YouTube-state validation helper; this fixture exposed that error.
The final candidate uses the existing platform-only main-thread check. Earlier failed candidates
and interrupted drivers are excluded from accepted logs and artifact identities.

## Final ordinary APK

The test APK was replaced by the ordinary Music-only development APK, versionCode 20. Its installed
hash matches the accepted build. Final DEX contains no fixture class, mode key or controlled labels.
The temporary mode key was deleted, and the original free rotation and 600,000 ms timeout restored.

- **EXECUTED:** twelve welcome startup cases, successful binding discovery/install, existing Music
  ad/background/Premium startup checks and [all six settings on](music-ui.json).
  The shared summary includes welcome offers. [Final screenshot](settings.png).
- **MEASURED:** kids Home/pause and ordinary Home/screen-off/pause playback remain functional.
  Screen-off is verified before and after the observation interval. [Samples](music-playback.json).
- **EXECUTED:** YouTube 21.45.88 regression: 664 startup and 64 settings UI cases, unified settings
  and Back, unchanged preference checksum, original module restored and temporary regression package
  removed. [Result](youtube-regression.json) · [Log](youtube-regression.log).
- **EXECUTED:** final Music is paused, fixture key absent and regression package removed. Scoped
  final logs contain no hook crashes, failed self-checks or welcome callback/discovery failures.
  [Music runtime](music-runtime.log).

## Limits

**NOT RUN:** naturally served welcome/controller cancellation. The offer was not delivered again
after its earlier manual dismissal. The controlled fixture proves the production queued effect
and gates on real host layouts with controlled listeners; it does not execute the live controller
binding or prove server dismissal state. Normal startup resolves that controller/binding uniquely.

**NOT RUN:** injected ambiguous/discovery/deoptimization failures, other Music versions/accounts,
and kids screen-off on this final APK. Earlier build-specific evidence remains scoped to its build.
The separate audio/video-switch trial BottomSheet is still unsupported.

**NOT RUN:** release signing; its matching private capability is unavailable. Existing separate
development signing was used; no release was published.

[Design](../../docs/MUSIC_PREMIUM_PROMOTIONS.md) · [Contract](../../contracts/music_welcome_inputs.json) ·
[Fixtures versus requirements](../../testdata/music_welcome_vectors.json)
