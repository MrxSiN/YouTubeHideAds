# YouTube Hide Ads v1.2.1 — device-tested build 127

SponsorBlock's four color sliders now share modern track and handle geometry, endpoint markers
and YouTube theme colors. Existing settings, presets and opacity behavior are preserved.

Installed as versionCode 127 on the Pixel 8 Pro with YouTube 21.42.243. All 636 startup and 64 UI
cases pass. Touch endpoints, keyboard, presets, save/reopen and dark/light rendering were checked;
original settings were restored. [Phone evidence and limits](evidence/sponsorblock_slider_device_20261022/README.md).

# YouTube Hide Ads v1.2.0

## 1.2.0 — 2026-10-22

SponsorBlock uses YouTube-native preference rows, text styles, themed pages and a compact player bottom sheet. Category colors use a live visual picker with presets and red, green, blue and opacity sliders. Back navigation, keyboard handling and accessible touch targets are shared across the forms. Existing settings, playback policies and API behavior are preserved.

[Device checks and limits](evidence/sponsorblock_ui_20261022/README.md). The package remains an XAX host plus unchanged BF/native policies.

# YouTube Hide Ads v1.1.0

## 1.1.0 — 2026-10-21

SponsorBlock now has bounded retry, a cross-video cache, native player/settings controls, ten
category modes and colors, manual skip/undo, preview/review/submission, voting/category correction,
channel exclusions, local/community statistics, private identity, and desktop settings transfer.
Community POSTs are explicit and never automatically retried; view reporting defaults off.

Targets YouTube 21.41.525. XAX-only host; existing BF/native inputs preserved. The shell release
mirror was removed; mirroring is now manual. See [current evidence](evidence/sponsorblock_20261021/README.md)
for checks and remaining validation limits.

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
- Settings under **YouTube → You → Settings → YoutubeHideAds**.

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

Install the APK, enable **YoutubeHideAds** in Vector or LSPosed with `com.google.android.youtube` as the only scope, then force-stop and reopen YouTube. If a development build (`org.youtubehideads.module`) is installed, uninstall it first. Your settings are kept in YouTube's data.
