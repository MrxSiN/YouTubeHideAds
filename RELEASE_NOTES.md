# YouTube Hide Ads v1.1.0

## What's new since 1.0.0

- **Background playback**, including Made for Kids videos and videos opened from a link. It has its
  own switch under Player and does not depend on Hide ads or SponsorBlock. Restart YouTube after
  changing it.
- **A YouTubeHideAds section** above Account in YouTube Settings, YouTube-style module pages and a
  **Compatibility & diagnostics** page with a copyable report.
- **SponsorBlock**: a player icon beside autoplay with a floating menu like YouTube's own, ten category
  modes and colors with a visual picker, manual skip/undo, segment preview, submission and voting,
  channel exclusions, statistics, settings transfer, bounded retry and a cross-video cache.
- **Shorts**: hide ten individual buttons and panels, and skip live Shorts. Both are off by default.
- **Swipe controls** shown as a pill with YouTube's brightness or volume icon, a level and the value.
- **Nine more languages**, following YouTube's language: 简体中文, 繁體中文, Español, Português,
  Русский, 日本語, 한국어, Bahasa Indonesia and Bahasa Melayu.
- **Lighter and faster.** The Brainfuck bridge used to reopen the module APK on every policy call,
  which was about 23 % of YouTube's CPU while scrolling and playing; it is now under 0.1 %. DexKit
  results are cached per YouTube build, so after the first launch YouTube shows its first screen about
  0.35 s sooner.

### Verified

Pixel 8 Pro, Android 17, Vector 2.2 (libxposed API 102), YouTube 21.42.243: all 11 startup self-check
suites pass and every hook installs, with or without the DexKit cache. Ads and sponsored Shorts were
removed, SponsorBlock lookups and original audio worked, and background playback continued from the
feed and from a link (Home and screen off) and stopped when its switch was off.
[Device checks and limits](evidence/device_perf_20261028/README.md).

Other YouTube versions, devices and 32-bit/x86 ABIs are not certified. The APK is arm64-v8a only.

### Version metadata

- Version name: `1.1.0`
- Android version code: `153`
- Package: `io.github.mrxsin.youtubehideads`
- Git tag: `v1.1.0`
- APK filename: `YouTubeHideAds-v1.1.0.apk`
- APK SHA-256: `80029979ada6a92fe1805994f9abe45cc4a4a898027a971adc2e8d297ac66060`

### Installing

Install the APK over 1.0.0; settings are kept in YouTube's data. Keep `com.google.android.youtube` as
the only scope in Vector or LSPosed, then force-stop and reopen YouTube.

# YouTube Hide Ads v1.0.0

## First public release

Removes YouTube ads and unwanted feed content, skips SponsorBlock segments, and adds fullscreen brightness/volume swipes and original-audio selection. Policy decisions are compiled Brainfuck; the host is a single XAX semantic store.

### Features

- Video, feed/search and shopping ads; sponsored Shorts removed before the pager is built.
- Premium, fullscreen and engagement-panel promotions.
- SponsorBlock: privacy-preserving hash-prefix lookup, guarded seeks; sponsor and self-promotion on by default.
- Playables, preview videos, Explore more topics and posts hidden by default; feed Shorts optional.
- Optional AI-channel filters (high and medium confidence AiSList lists).
- Fullscreen swipes: left edge brightness, right edge media volume.
- Prefers the original audio track on multi-language videos.
- Settings under **YouTube → You → Settings → YouTubeHideAds**.

### Changed since the last development build

- New package `io.github.mrxsin.youtubehideads` (was `org.youtubehideads.module`).
- Seven identical gate libraries merged into one `liband3.so`. The APK has 11 native libraries instead of 17 and is about 97 KB smaller. Behavior is unchanged.

### Verified

- Pixel 8 Pro, Android 17, YouTube 21.41.525, Vector 2.2 (libxposed API 102): all 531 startup self-checks pass and every hook installs. The installed APK matches the published SHA-256.
- Per-feature off/on UI checks were last run on development build 77 with the same policy bytes.

Other YouTube versions, devices and 32-bit/x86 ABIs are not certified. The APK is arm64-v8a only.

### Version metadata

- Version name: `1.0.0`
- Android version code: `100`
- Package: `io.github.mrxsin.youtubehideads`
- Git tag: `v1.0.0`
- APK filename: `YouTubeHideAds-v1.0.0.apk`
- APK SHA-256: `0c57a68a23baafc5a8b619bee3057ef7785c7d866853ebd45c4c81baa69ceb2b`

### Installing

Install the APK, enable **YouTubeHideAds** in Vector or LSPosed with `com.google.android.youtube` as the only scope, then force-stop and reopen YouTube. If a development build (`org.youtubehideads.module`) is installed, uninstall it first. Your settings are kept in YouTube's data.
