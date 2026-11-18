# YouTube Hide Ads v1.4.0

## What's new since 1.3.0

- **YouTube Music support** ([#5](https://github.com/MrxSiN/YouTubeHideAds/issues/5)). Add YouTube Music to the module's
  scope to get its own settings page (Account → Settings → YouTube Hide Ads) with:
  - ad hiding: audio/video ads, sponsored and Premium components, fullscreen promotions;
  - Premium promotions: Upgrade tab, Get Music Premium entries, membership upsell, promotion mealbar, welcome offer;
  - background playback (on by default);
  - exclusive audio playback (on by default) and an optional Audio/Video switch on the left half of the player pill.
- **Downloads in YouTube and YouTube Music**, off by default: in-app downloads with native quality selection, or
  hand-off to Seal, YTDLnis or NewPipe, plus export of completed downloads to a folder you choose.
- **YouTube Premium promotions:** the Premium button in the You-page header is removed too.
- **Fixed:** a crash inside the player progress hook at the start of every video, which skipped that moment's
  SponsorBlock and player work.
- **Faster:** no regex compiling or resource-name lookups on hot paths. While scrolling, the module's share of YouTube's
  CPU from its layout listener fell from about 1.3 % to 0.3 %, and in YouTube Music from about 1.9 % to 0.4 %.

### Known issues

- SponsorBlock, Return YouTube Dislike and DeArrow are YouTube only.
- In Music, restart the app after changing a switch.
- Downloads: private, paid, DRM or restricted videos are not supported; an export stops if the app is closed.
- AdGuard and similar apps with a system HTTPS certificate stop SponsorBlock, dislikes, Audio/Video search and the
  update check from connecting. [Details](README.md#sponsorblock-or-update-check-never-connects).
- New strings are English only.

### Verified

Pixel 8 Pro, Android 17, Vector 2.2, YouTube 21.45.88 and YouTube Music 9.46.51: this APK installed over 1.3.0, all
startup checks passed and every hook installed in both apps with 0 hook crashes, and a video ad was suppressed. The
same code (build 164) passed ad and component removal, SponsorBlock, the download button, the Music Audio/Video switch
and Music background playback after Home and screen off. Music Premium/welcome surfaces were not served during testing;
download save/export was verified by the development builds, not re-run on this APK.
[Release checks](evidence/release_1_4_0_20261118/README.md) · [Performance and feature checks](evidence/perf_20261118/README.md).

Other app versions, devices and 32-bit/x86 ABIs are not certified. The APK is arm64-v8a only.

### Version metadata

- Version name: `1.4.0`
- Android version code: `165`
- Package: `io.github.mrxsin.youtubehideads`
- Git tag: `v1.4.0`
- APK filename: `YouTubeHideAds-v1.4.0.apk`
- APK SHA-256: `a9a3ffc23217a35e7c0f0e1071cc9ce89fe60787d4fc10e9ec481ced3e8853a0`

### Installing

Install the APK over 1.3.0; settings are kept in each app's data. In Vector or LSPosed keep
`com.google.android.youtube` in scope and add `com.google.android.apps.youtube.music` for Music, then force-stop
and reopen the app. If you used a YouTube Hide Ads development package for Music, disable it first.

# YouTube Hide Ads v1.3.0

## What's new since 1.2.0

- **Works with YouTube 21.45.88.**
- **One settings page.** YouTube Hide Ads opens as a single page with sections (Ads & promotions, SponsorBlock,
  Player, Shorts, Feed & content, About) and inline settings.
- **New, all off or neutral by default:**
  - Default playback speed, separately for videos and Shorts.
  - Default video quality, separately for Wi-Fi, mobile data, Shorts and live streams.
  - Preferred caption languages, and an option to stop automatic captions.
  - Return YouTube Dislike (read only, no votes are sent).
  - Tap to seek, Loop video and a Speed button in the player's top bar.
  - Channel and keyword blacklist for feed, search, related items and optionally comments.
  - DeArrow thumbnails.
  - Remember live stream position.
- **Fullscreen live chat no longer changes the volume.** A drag on an open live chat, comments or description
  panel, or on the end-of-video More videos sheet, starts no brightness or volume swipe.
  ([#6](https://github.com/MrxSiN/YouTubeHideAds/issues/6))
- **Skip live Shorts works again** on YouTube 21.45.
- **Swipe pill moved:** brightness docks right and volume left, beside an open fullscreen panel.
- Startup installers are guarded one by one, so one failure no longer skips the rest.

### Known issues

- YouTube's speed menu still shows 1x after a default speed is applied.
- AdGuard and similar apps with a system HTTPS certificate stop SponsorBlock, Return YouTube Dislike and the update
  check from connecting (`NOT_ENOUGH_SCTS`). Exclude those hosts from HTTPS filtering.
  [Details](README.md#sponsorblock-or-update-check-never-connects).
- New strings are English only.

### Verified

Pixel 8 Pro, Android 17, Vector 2.2, YouTube 21.45.88: all 22 hooks installed at startup, the settings page,
default speed, speed button, blacklist, video quality on Wi-Fi and Shorts, captions, DeArrow thumbnails, SponsorBlock,
both swipes and the live chat drag, with 0 crashes. Return YouTube Dislike fetching was BLOCKED on the test phone by
HTTPS filtering; mobile-data quality, live streams and automatic-caption blocking were NOT RUN.
[Device checks and limits](evidence/release_1_3_0_20261114/README.md).

Other YouTube versions, devices and 32-bit/x86 ABIs are not certified. The APK is arm64-v8a only.

### Version metadata

- Version name: `1.3.0`
- Android version code: `157`
- Package: `io.github.mrxsin.youtubehideads`
- Git tag: `v1.3.0`
- APK filename: `YouTubeHideAds-v1.3.0.apk`
- APK SHA-256: `3d11356e56eba2e8e329b248b4eaa17903eb9f0db4e64281ea154df9cce70665`

### Installing

Install the APK over 1.2.0; settings are kept in YouTube's data. Keep `com.google.android.youtube` as
the only scope in Vector or LSPosed, then force-stop and reopen YouTube.

# YouTube Hide Ads v1.2.0

## What's new since 1.1.0

- **Works with YouTube 21.43.523.** Background playback and SponsorBlock skipping had stopped working
  after the YouTube update; both are back. ([#3](https://github.com/MrxSiN/YouTubeHideAds/issues/3))
- **Update check.** Once each time YouTube starts, the module asks GitHub whether a newer release
  exists and, if so, shows a YouTube-style dialog with **Update** (opens the release page) and
  **Later**. It is on by default; turn it off under **About → Check for updates**.
- **Report a problem.** **About → Compatibility & diagnostics → Report a problem** opens a new GitHub
  issue with the compatibility report already filled in. Nothing is sent until you submit it.
- **New name: YouTube Hide Ads**, matching the other modules. Settings, package and saved preferences
  are unchanged.
- The About page and compatibility report show the real version again (1.1.0 showed `1.1.0 (132)`).
- SponsorBlock request failures are now logged with their cause.

### Known issue: HTTPS filtering apps

AdGuard and similar apps, when their certificate is installed as a system certificate, stop
SponsorBlock and the update check from connecting (`NOT_ENOUGH_SCTS` in the log). Exclude
`sponsor.ajay.app` and `github.com` from HTTPS filtering. [Details](README.md#sponsorblock-or-update-check-never-connects).

### Verified

Pixel 8 Pro, Android 17, Vector 2.2 (libxposed API 102), YouTube 21.43.523: every startup self-check
passes and every hook installs; background playback continued after Home and with the screen off for a
video opened from a link; original audio was selected on a multi-language video; the update dialog and
both buttons, the switch and the prefilled issue were checked. [Device checks and limits](evidence/release_1_2_0_20261030/README.md).

Other YouTube versions, devices and 32-bit/x86 ABIs are not certified. The APK is arm64-v8a only.

### Version metadata

- Version name: `1.2.0`
- Android version code: `155`
- Package: `io.github.mrxsin.youtubehideads`
- Git tag: `v1.2.0`
- APK filename: `YouTubeHideAds-v1.2.0.apk`
- APK SHA-256: `d984de2fda0ca0e29d1b98823142915f6a54403f9d12a86f687c7950661e6d0d`

### Installing

Install the APK over 1.1.0; settings are kept in YouTube's data. Keep `com.google.android.youtube` as
the only scope in Vector or LSPosed, then force-stop and reopen YouTube.

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
