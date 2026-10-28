# YouTube-style UI, Shorts controls and languages — 2026-10-27/28

Exact development artifact: **1.4.0-dev/code 132**, installed on Pixel 8 Pro / Android 17,
Vector 2.2/API 102, stock YouTube 21.42.243. No YouTube APK was modified.
[Build identity](build.json) · [Toolchain](toolchain.json) · [Runtime log](runtime.log).

The canonical store and installed APK correspond to root
`b34d4b6502b5bfe713bc05a46840782b04098d9abef948df990d419e0fd125db`.
APK SHA-256: `38f15f0a0f61b7f5fea45154c8ae42fe46f80c67c5b7172e4047c9a009b859de`.

## What changed

| Area | Result |
| --- | --- |
| Name | **YouTubeHideAds** everywhere: launcher label, settings heading, page titles, logs. |
| Settings entry | Its own **YouTubeHideAds** section above **Account**, built from YouTube's own `preference_group_title` and `preference_with_icon` layouts; it scrolls with the list. [Screenshot](settings-section.png) |
| Module page | Same scaffold, headings and rows as the SponsorBlock pages, now with a **Shorts** section. [Top](module-page.png) · [Shorts section](module-page-shorts.png) |
| Compatibility & diagnostics | Module, system, framework, per-feature compatibility, self-check totals, session counters and **Copy compatibility report**. [Top](diagnostics-top.png) · [Features](diagnostics-features.png) |
| Hide Shorts components | Ten switches (default off): like, comments, share, remix, save, sound, subscribe, title, suggestions/info panels, paused-overlay buttons. [Page](shorts-components.png) · [Like, comments, share and remix hidden](shorts-hidden-buttons.png) |
| Skip live Shorts | Switch (default off). When the Shorts pager settles on a live preview page it moves to the next Short. |
| Swipe controls | A pill on the side being swiped: YouTube brightness or volume icon, a vertical level and the value, held briefly after release. [Rendering](swipe-hud-probe.png) |
| SponsorBlock | Player icon between autoplay and cast; floating menu card like the player settings menu. [Controls](player-controls.png) · [Menu](sponsorblock-menu.png) |
| Languages | 259 user-visible strings in 简体中文, 繁體中文, Español, Português, Русский, 日本語, 한국어, Bahasa Indonesia and Bahasa Melayu, following YouTube's language. [Module page](module-page-zh-CN-probe.png) · [Diagnostics](diagnostics-zh-CN-probe.png) |
| Pages | Full-screen module pages paint behind the system bars; segment rows show category and time range; switch rows without a summary centre their title. |

Shorts components reuse the existing component hook: path names identify most buttons, and the
existing element serializer identifies the anonymous comment, share and remix buttons by their
accessibility ids, only when one of those switches is on. Matches, like live-Short skips, are
authorized by the unchanged AND3 Brainfuck policy. Settings are read from a snapshot published on
refresh, so the hook never touches SharedPreferences. Diagnostics read one bounded startup event
list (54 sites, at most 160 entries).

## Device observations (final APK)

- Cold start: 11 startup self-checks pass and every hook installs, with no unresolved roles or
  crashes. Opening at 855 s on a sponsored test video produced three accepted skips.
- All 16 feature rows show **Compatible**; the diagnostics page reported 12 checks passed after
  the native UI suite ran.
- With like, comments, share and remix enabled, those four buttons were absent from Shorts while
  save and sound remained. All test switches were turned back off afterwards.
- The settings section appears above Account on first open and moves with the list.

## Development probes (not the shipped APK)

Probe variants of the same source were used where the device could not produce the condition on
demand; their screenshots are labelled `-probe`.

- **Swipe HUD:** injected `adb` drags were taken by YouTube's own fullscreen gestures, so a probe
  rendered the HUD at fullscreen entry. Its look is shown; a real finger swipe was not captured.
- **Languages:** YouTube on this phone ignored a per-app locale and the system language was not
  changed, so a probe forced the module lookup to `zh-CN`. Real locale switching is not shown.
- **Skip live Shorts:** no live preview page appeared in about 130 scrolled Shorts during testing.
  An inverted probe confirmed that settle detection, current-page selection and the page advance
  work and that the next Short plays. That live preview pages lack the Shorts overlay container
  is an unconfirmed assumption.

## Limits

Dark theme only. Light theme, tablets, right-to-left layouts, other YouTube versions and a real
live Short were not exercised. The menu drag handle is visual; tap outside or Back closes it.
Vector logged one "null receiver" exception after `proceed()` in an existing hook, so YouTube's
own behavior ran; it was not traced to a specific function in this session.
