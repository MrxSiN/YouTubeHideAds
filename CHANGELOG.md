# Changelog

## 1.2.1 — 2026-10-22 (device-tested build 127)

The color picker's four sliders share a rounded 16 dp track, a vertical 4 × 44 dp handle,
handle spacing and an endpoint marker, using the geometry in YouTube 21.42.243's bundled
modern slider style. Colors follow YouTube's active theme; native dragging, keyboard input,
accessibility and the existing 48 dp touch targets remain in place.

Fixed module resource visibility, binary XML initialization and range-reset keyboard increments
found by phone testing. The inactive-track tint is applied once for proper contrast.
[Build and phone verification](evidence/sponsorblock_slider_device_20261022/README.md): 636 startup + 64 UI cases,
dark/light rendering, endpoints, keyboard and saved-color persistence pass.

## 1.2.0 — 2026-10-22

SponsorBlock uses YouTube-native preference rows, text styles, themed pages and a compact player bottom sheet. Category colors use a live visual picker with presets and red, green, blue and opacity sliders. Back navigation, keyboard handling and accessible touch targets are shared across the forms. Existing settings, playback policies and API behavior are preserved.

[Device checks and limits](evidence/sponsorblock_ui_20261022/README.md). The package remains an XAX host plus unchanged BF/native policies.

## 1.1.0 — 2026-10-21

SponsorBlock now has bounded retry, a cross-video cache, native player/settings controls, ten
category modes and colors, manual skip/undo, preview/review/submission, voting/category correction,
channel exclusions, local/community statistics, private identity, and desktop settings transfer.
Community POSTs are explicit and never automatically retried; view reporting defaults off.

Targets YouTube 21.41.525. XAX-only host; existing BF/native inputs preserved. The shell release
mirror was removed; mirroring is now manual. See [current evidence](evidence/sponsorblock_20261021/README.md)
for checks and remaining validation limits.

## 1.0.0 — 2026-10-18

First public release.

- Package is now `io.github.mrxsin.youtubehideads` (was `org.youtubehideads.module`), in line with the
  author's other modules on Xposed-Modules-Repo. versionCode 100. Preferences live in YouTube's own
  data and carry over, but the module must be enabled once in the manager under its new name.
- The seven three-input gates (Premium upsell, Shorts ad slot, Playables, fullscreen swipe, feed
  section, AI channel, original audio) share one native library, `liband3.so`, compiled from one
  source, `source/brainfuck/and3.bf`. Before, they shipped seven identical copies. The APK drops from
  17 to 11 native libraries and is about 97 KB smaller. The policy bytes and decision call sites are
  unchanged.
- Removed authored Brainfuck that never shipped (feed/search/shopping, resolver, cleanup and the
  older two-stage SponsorBlock programs), the legacy BFH1/BFR1 offline protocol and its vectors,
  fixtures with no runner, and pre-release device evidence.
- Every Brainfuck header now names the shipped ABI (`bfc_call_v1`).
- Releases are mirrored automatically to Xposed-Modules-Repo, which feeds modules.lsposed.org.

Verified on a Pixel 8 Pro, Android 17, YouTube 21.41.525 and Vector 2.2. All 531 startup self-checks
pass and every hook installs. The installed APK matches the published digest. Per-feature off/on UI
checks were last run on build 77; see `evidence/release_20261018`.

## Pre-release builds

Development builds were not published. Milestones, by versionCode:

- 77: AI-channel filters (AiSList high/medium confidence), forced original audio, static branding.
- 74: Feed switches for preview videos, Explore more topics, posts and feed Shorts.
- 67: Playables removal and fullscreen brightness/volume swipes.
- 60: Sponsored Shorts removed before the pager is built.
- 44: Premium, fullscreen and engagement-panel promotions.
- 39: SponsorBlock retrieval through a hash prefix, with guarded player seeks.
- 29: Native ad component and panel policies, live player/component suppression.
- 27: Brainfuck and XAX only. Conventional-language sources were removed.
- 26: YouTube-style settings page with defaults owned by Brainfuck.
