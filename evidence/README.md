# Evidence index

The canonical source and release is **1.1.0, versionCode 153**
(`io.github.mrxsin.youtubehideads`). Dated
directories are immutable measurements of their named builds; their prose may say canonical/installed
relative to that session. Those statements do not identify today's source store or APK. Preserve
original hashes, screenshots, logs and measurements when documentation changes.

| Session | Builds and scope |
| --- | --- |
| [Device performance, DexKit cache and link background playback, 2026-10-28](device_perf_20261028/README.md) | 135-153, released as 1.1.0: bridge rework (22.7 % to 0.05 % of YouTube CPU), DexKit threads and result cache (first screen 0.35 s sooner), background playback from links; A/B timings and cache invalidation checks |
| [YouTube-style UI, Shorts and languages, 2026-10-27/28](ui_redesign_20261027/README.md) | 132: settings section above Account, shared page design, Compatibility & diagnostics, inline SponsorBlock icon and menu, Shorts components, live-Short skipping, swipe pill, nine languages; 11 startup + 64 UI checks, live skips; probes labelled; dark theme only |
| [Background playback, 2026-10-27](background_playback_20261027/README.md) | 131: 664 startup checks, scoped regular/Pinkfong screen-off and notification tests, disabled behavior, unchanged native inputs and original preferences restored; hardware/UI limits documented |
| [Slider phone acceptance, build 127, 2026-10-22](sponsorblock_slider_device_20261022/README.md) | 127: installed digest, 636 startup + 64 UI checks, dark/light, endpoints, keyboard, save/reopen and settings restoration |
| [SponsorBlock sliders, build 124, 2026-10-22](sponsorblock_slider_20261022/README.md) | 124: historical local-build snapshot; subsequently rejected during phone testing (see code 127 session) |
| [SponsorBlock UI, build 123, 2026-10-22](sponsorblock_ui_20261022/README.md) | 123: native YouTube presentation, visual color picker, 636 startup + 28 UI checks |
| [SponsorBlock, build 111, 2026-10-21](sponsorblock_20261021/README.md) | 111: 636 checks, player/menu controls, cache/retry, preview/review, markers and settings transfer; production writes untested |
| [Release 1.0.0, 2026-10-18](release_20261018/README.md) | Historical 100: shared `liband3.so`, new package; 531 checks, every hook installed, installed digest |
| [AI/audio, branding and topics, 2026-10-18](ai_audio_branding_20261018/README.md) | 77: AI/audio live off/on, video pixels and restored preferences; controlled topics/App info on 75, initial cache fetch on 76 |

Pre-release sessions are summarized in the [changelog](../CHANGELOG.md): feed filters 74,
Playables/swipes 67, sponsored Shorts 60, ad surfaces 44, SponsorBlock/panels 39, ad hooks 29,
XAX-only 27 and settings 26. Their raw logs and screenshots were removed before the first public
release.

## Current authoritative records

- [Current development identity and native hashes](background_playback_20261027/build.json)
- [Tagged baseline identity](sponsorblock_slider_device_20261022/build.json)
- [Current external compiler and pinned inputs](background_playback_20261027/toolchain.json)
- [Build 77 device settings](ai_audio_branding_20261018/device-checks.json) and [verification](ai_audio_branding_20261018/verification.json)

A component-replacement log alone does not prove all layout/blank-space behavior. Progress movement
alone does not prove video playback. A fixture or controlled hook positive is not a naturally
served ad/shelf. [Current coverage](../docs/FEATURE_COVERAGE.md) and
[remaining limits](../docs/COMPATIBILITY.md) keep those distinctions explicit.
