# Changelog

## Unreleased

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
