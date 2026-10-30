# Changelog

## Unreleased

## 1.2.0 — 2026-10-30 (versionCode 155)

Collects development builds 154 and 155, listed below, and supports YouTube 21.43.523.

### Development build 155 (1.2.0) — 2026-10-30

- **Check for updates** (About, on by default): once per YouTube start, off the main thread, the module
  sends one bodiless `HEAD` to `github.com/…/releases/latest` and reads the tag from the redirect (no
  JSON, no GitHub API rate limit). A newer `vX.Y.Z` shows a dialog in YouTube's own modern style
  (24 dp rounded raised surface, YouTube text styles, stacked pill buttons); **Update** opens the
  release page, **Later** closes it. Failures are logged as `Update check failed: …` and never shown.
- **Report a problem** (Compatibility & diagnostics): opens a new GitHub issue with the compatibility
  report filled in. Nothing is sent until you submit it on GitHub. The copy button and the issue link
  share one report builder; constant URL parts are encoded at build time.
- The per-process "already checked" marker no longer holds the first Activity; only a weak reference is kept.
- Force original audio was already part of the module (on by default, under Player controls); it was
  checked again on 21.43.523 (`Original audio selected: en.4`).
- README: troubleshooting entry for HTTPS-filtering apps (exclude `sponsor.ajay.app` and `github.com`).

Tested on the same Pixel and YouTube 21.43.523: no startup regressions, switch saved and restored, one
`HEAD` per start, the dialog with both buttons (against a local redirect, since this phone's HTTPS filter
breaks github.com inside YouTube), the copied report header (`1.2.0 (155)`) and the prefilled issue link.
New strings are English only.

### Development build 154 (1.1.1) — 2026-10-30

YouTube 21.43.523 support ([issue #3](https://github.com/MrxSiN/YouTubeHideAds/issues/3)).

- Fix: background playback was off on 21.43. The background-settings caller now also calls
  `Iterator.hasNext()` and `Optional.isPresent()`, so the settings role was ambiguous and the whole
  feature failed closed. The callee must now be declared in one of YouTube's own classes.
- Fix: SponsorBlock skipping was off on 21.43. The progress method calls the same accessor twice;
  discovery counted call sites instead of distinct methods. The player hook installs again.
- The module is now named **YouTube Hide Ads** (label, settings section, report), like the other modules.
- The About page and compatibility report showed `1.1.0 (132)`; they now show the real version.
- A failed SponsorBlock request logs its cause (`SponsorBlock request error: …`).

Tested on Pixel 8 Pro, Android 17, Vector 2.2, YouTube 21.43.523: all startup suites pass, every
background role resolves, audio continues after Home and with the screen off for a video opened from a link.

- GitHub Actions: `Release CI` checks contracts, the source boundary and tag/version agreement on
  every push, and verifies each published release APK (package, version, release signing certificate,
  SHA-256 in the release notes). `xposed-sync` then mirrors the verified release to
  Xposed-Modules-Repo automatically again.

## 1.1.0 — 2026-10-28 (versionCode 153)

The first release since 1.0.0. It collects development builds 111 to 153, listed below.

- **Background playback**, including Made for Kids videos and videos opened from a link; its own
  switch, independent of Hide ads and SponsorBlock.
- **Settings and pages**: a YouTubeHideAds section above Account in YouTube Settings, YouTube-style
  module pages, and a Compatibility & diagnostics page with a copyable report.
- **SponsorBlock**: bounded retry and cross-video cache, ten category modes and colors with a visual
  picker, manual skip/undo, segment preview, submission and voting, channel exclusions, statistics,
  settings transfer, a player icon beside autoplay and a floating menu like YouTube's own.
- **Shorts**: hide ten individual buttons and panels, and skip live Shorts.
- **Swipe controls** shown as a YouTube-style pill with icon, level and value.
- **Languages**: 简体中文, 繁體中文, Español, Português, Русский, 日本語, 한국어, Bahasa Indonesia and
  Bahasa Melayu, following YouTube's language.
- **Faster**: the Brainfuck bridge no longer reopens the APK on each policy call (it was about 23 %
  of YouTube's CPU while scrolling and playing), and DexKit results are cached per YouTube build,
  so YouTube shows its first screen about 0.35 s sooner after the first launch.

Tested on a Pixel 8 Pro, Android 17, Vector 2.2 (API 102), YouTube 21.42.243.
[Device checks](evidence/device_perf_20261028/README.md).

## Development build 153 — 2026-10-28

Fix: background playback now continues when a video was opened from a link. The player was created
before the background hooks were ready, so the module never saw it and left YouTube's restriction in
place. The player observer is now installed at startup; overrides still need every existing check.

## Development build 152 — 2026-10-28

Cold start: DexKit answers are cached per YouTube build in YouTube's `code_cache`, so after the first
start the hook search takes about 80 ms instead of 460 ms and YouTube's first screen appears about
0.35 s sooner. The same hooks, checks and diagnostics run; a YouTube or module update, or a damaged
file, simply rebuilds the cache.

## Development build 143 — 2026-10-28

Cold start: the main-thread hook search runs DexKit on 8 threads instead of 2, so YouTube shows
its first screen about 0.27 s sooner on a Pixel 8 Pro. The same hooks resolve.

## Development build 135 — 2026-10-28

Faster on the phone, same behaviour. The Brainfuck bridge reopened the module APK on every policy
call; that path was about 23 % of YouTube's CPU while scrolling and playing, and is now under 0.1 %.
Policy calls no longer allocate a tape or path string, and the background playback flag hook skips
the policy call for flags it can never change. All startup self-checks pass and features behave as
in build 132. [Profile and checks](evidence/device_perf_20261028/README.md).

## Development build 132 — 2026-10-27

The module is named **YouTubeHideAds** throughout. In YouTube Settings it now has its own
**YouTubeHideAds** section above Account, made from YouTube's own heading and icon-row layouts. It
scrolls with the list instead of staying pinned. The module page uses the same scaffold, headings
and rows as the SponsorBlock pages.

New **Compatibility & diagnostics** page under About: module, Android, build, YouTube and framework
versions; whether each feature's hooks resolved on this YouTube version; self-check totals;
session counters; and a copyable report for bug reports.

SponsorBlock's "SB" overlay button is replaced by an icon beside autoplay in the player's top bar.
Its menu matches the player settings menu: floating rounded card, drag handle, icons and chevrons.
Full-screen pages extend behind the system bars, and segment rows show category and time range.
New Shorts section: **Hide Shorts components** (ten switches: like, comments, share, remix, save,
sound, subscribe, title, suggestions and info panels, paused-overlay buttons) and **Skip live
Shorts**, both off by default. Swipe controls now show a pill on the side being swiped with a
YouTube icon, a vertical level and the value, held briefly after release.

The module speaks the viewer's YouTube language: 简体中文, 繁體中文, Español, Português, Русский, 日本語,
한국어, Bahasa Indonesia and Bahasa Melayu join English ([issue #2](https://github.com/MrxSiN/YouTubeHideAds/issues/2)).
The README is available in the same languages.

Existing policies, hooks, native inputs and preferences are unchanged; new removals use the existing
AND3 policy. [Build and device checks](evidence/ui_redesign_20261027/README.md).

## Development build 131 — 2026-10-27

Adds **Background playback** under Player controls, enabled by default and independent of Hide ads
and SponsorBlock. Brainfuck's existing AND3 policy authorizes structurally resolved XAX hooks for
regular playback eligibility, the Made for Kids controller, background settings and the single
automatic foreground-resume experiment. No play commands, Premium spoof, services or wake locks.

Discovery runs on a worker, requires unique typed roles, deoptimizes relevant callers and enables
the complete set only after validation and installation. Settings use existing save/reset behavior;
restart YouTube after a change to discard native caches. Native dependencies and all existing
startup suites are unchanged. Morphe attribution is preserved in source and packaged resources.

[Build, verification and device limitations](evidence/background_playback_20261027/README.md) ·
[Implementation and reference research](docs/BACKGROUND_PLAYBACK.md).

## Development build 127 — 2026-10-22

The color picker's four sliders share a rounded 16 dp track, a vertical 4 × 44 dp handle,
handle spacing and an endpoint marker, using the geometry in YouTube 21.42.243's bundled
modern slider style. Colors follow YouTube's active theme; native dragging, keyboard input,
accessibility and the existing 48 dp touch targets remain in place.

Fixed module resource visibility, binary XML initialization and range-reset keyboard increments
found by phone testing. The inactive-track tint is applied once for proper contrast.
[Build and phone verification](evidence/sponsorblock_slider_device_20261022/README.md): 636 startup + 64 UI cases,
dark/light rendering, endpoints, keyboard and saved-color persistence pass.

## Development build 123 — 2026-10-22

SponsorBlock uses YouTube-native preference rows, text styles, themed pages and a compact player bottom sheet. Category colors use a live visual picker with presets and red, green, blue and opacity sliders. Back navigation, keyboard handling and accessible touch targets are shared across the forms. Existing settings, playback policies and API behavior are preserved.

[Device checks and limits](evidence/sponsorblock_ui_20261022/README.md). The package remains an XAX host plus unchanged BF/native policies.

## Development build 111 — 2026-10-21

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
