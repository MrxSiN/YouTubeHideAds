# Tested compatibility

Development build **157 (1.3.0)** was exercised on the same Pixel 8 Pro, Android 17 and Vector 2.2/API 102 with
YouTube **21.45.88**: 22 startup `installed` lines with no unresolved, ambiguous or exception line, the settings page,
default speed, the speed button, blacklist Save, video quality on Wi-Fi and Shorts, captions, DeArrow thumbnails and the
swipes, with 0 `FATAL EXCEPTION`. Return YouTube Dislike could not fetch behind the phone's HTTPS filtering. Mobile-data
quality, live streams and automatic-caption blocking were NOT RUN. The same-day rebuild (store `41c36cb4...fabee7`)
was re-checked for startup (22 `installed` lines), the More videos sheet (no swipe while it is shown) and the speed
button.
[Checks and limits](../evidence/release_1_3_0_20261114/README.md).

Development build **156 (1.2.1)** was exercised on the same Pixel 8 Pro, Android 17 and Vector 2.2/API 102 with
YouTube **21.45.88**: 1.2.0 itself installs every hook there; build 156 passes all startup checks, the live chat
swipe fix, live-position save/restore and the skip mechanism (inverted probe). A real live Short was not available.
[Checks and limits](../evidence/release_1_2_1_20261114/README.md).

Release **1.2.0, versionCode 155** (and development build 154 before it) was exercised on the same Pixel 8 Pro, Android 17 and
Vector 2.2/API 102 with YouTube **21.43.523**: all startup suites, every hook and background role
resolving, and background playback from a link (Home, screen off). SponsorBlock segment fetching was
not observed on this phone because an HTTPS-filtering proxy failed Certificate Transparency; the player
hook, video ID, seek and duration bridges resolve. [Checks and limits](../evidence/release_1_2_0_20261030/README.md).

The following records describe release 1.1.0:

Release **1.1.0, versionCode 153** was exercised on Pixel 8 Pro, Android 17, Vector 2.2/API 102 and
YouTube 21.42.243: all 11 startup suites, ads and sponsored-Shorts removal, SponsorBlock, original audio,
and background playback from the feed and from a link (Home, screen off, switch off), with and without
the DexKit cache. It retains arm64/API 102 requirements and the same native/third-party dependencies.
No other device, framework or YouTube version is certified. [Checks and limits](../evidence/device_perf_20261028/README.md).
Background playback was first exercised on development build 131:
[dated checks and remaining limits](../evidence/background_playback_20261027/README.md).

The following records describe earlier development builds:

Development build **127**. Targeted slider/UI checks passed
2026-10-22 on YouTube **21.42.243**: 636 startup and 64 UI cases, dark/light rendering, touch,
keyboard and saved-color persistence. [Exact phone evidence and limits](../evidence/sponsorblock_slider_device_20261022/README.md).
The rows below retain earlier feature proof and do not certify 21.20.405.
The declared minSdk 28 and libxposed API 102 requirement do not certify untested Android/framework combinations.

| Device | Android | YouTube | Framework | Observed |
| --- | --- | --- | --- | --- |
| Pixel 8 Pro, arm64 | 17 / API 37 | 21.42.243 | Vector 2.2 / API 102 | Build 127: modern sliders, 636 startup + 64 UI checks; dark/light, endpoints, one-step keyboard and save/reopen pass. |
| Pixel 8 Pro, arm64 | 17 / API 37 | 21.42.243 | Vector 2.2 / API 102 | Build 123: YouTube-native SponsorBlock UI and color picker; 636 startup + 28 UI checks. See current evidence for device coverage. |
| Pixel 8 Pro, arm64 | 17 / API 37 | 21.41.525 | Vector 2.2 / API 102 | Build 111: 636 startup checks, installed digest and native menu/transfer navigation; preview/review and track markers on 110. Earlier feature proofs remain attached to their historical builds. |
| Pixel 8 Pro, arm64 | 17 / API 37 | 21.42.243 | Vector 2.2 / API 102 | Same build 111: 636 post-restore startup checks, native player/menu controls, valid settings round trip and malformed-import preservation. Community writes and natural manual skip/undo remain untested. |

The Pixel's factory YouTube 21.18.164 APK was copied and inspected. Its current player-progress and
seek-anchor strings differ; it is not certified compatible. Android rejected an in-place downgrade
with INSTALL_FAILED_VERSION_DOWNGRADE. No uninstall or data clear was performed. The current base
APK and all three splits are backed up under ignored build/research/youtube-installed.

No second device or emulator image was available. Sponsored Shorts entries are now removed before
pager insertion. The prior auto-navigation experiment was rejected after a playback regression.
Naturally delivered Premium/fullscreen/panel positives remain pending. See
Shorts evidence (`shorts_sponsored_20261017`, removed before 1.0.0) and
earlier controlled evidence (`ad_surfaces_20261017`, removed before 1.0.0).

## Historical Playables and swipe build 67

Playables drawer/card removal, settings persistence, disabled cold-start restoration and re-enabling
pass on the same Pixel and YouTube version. All 399 startup checks pass. Actual fullscreen left/
right swipes, percentage HUDs, brightness restoration, media volume restoration, disabled toggles,
native taps/2x holds and two advancing Shorts clips pass. Three live sponsored entries were removed
before pager creation during the Shorts check. Both switches were restored on. No additional
YouTube version is certified. See evidence (`playables_swipes_20261017`, removed before 1.0.0).

## Historical feed build 74

All 471 startup checks pass on the same Pixel/YouTube version. Four feed switches toggle and
persist across cold starts with the requested defaults. Preview, posts and feed Shorts have live
removal evidence; the Home Explore more topics shelf was not served. Its own-heading classifier
and History negative pass fixtures. Preview/topics matching is English-only. No additional
YouTube version is certified. Exact builds and checks (`feed_filters_20261017`, removed before 1.0.0).

## Build 77

The same Pixel/YouTube version passes all 531 checks, live high-confidence AI filtering off/on,
native Hindi versus forced English original audio, advancing video, restored preferences and
installed APK identity. Topics passes a controlled actual-hook test on milestone 75; no natural
Home shelf arrived. Original-track `.4` IDs and typed SABR selection are calibrated only here.
Other YouTube versions/devices and a warnlist-positive live card are not certified.
[Evidence and exact artifacts](../evidence/ai_audio_branding_20261018/README.md).

## Additional limits

Natural Home topics and Premium/fullscreen/panel positives, English-heading alternatives, a separate
warnlist-positive live card, real multi-pointer swipes and fixed-volume routes remain unverified.
Original audio uses the upstream .4 convention calibrated on 21.41.525. The external branding-v2
compiler snapshot is a build requirement, not broader runtime compatibility.

[Current evidence](../evidence/ai_audio_branding_20261018/README.md) · [All coverage](FEATURE_COVERAGE.md)

## HTTPS-filtering apps

Segments never appear, no update is offered or dislike counts never show, and the log has `SponsorBlock request
error`, `Update check failed` or `RYD request failed` with `NOT_ENOUGH_SCTS`. An HTTPS-filtering app such as
AdGuard re-signs secure traffic with its own certificate, and when that certificate is installed as a system
certificate, Android sends YouTube's traffic through it. YouTube enforces Certificate Transparency, which that
certificate cannot meet, so Android refuses the connection. The module does not weaken this check.

Fix: in AdGuard, open Settings > Filtering > Network > HTTPS filtering > Exclusions (the path can differ by
version) and add `sponsor.ajay.app` (SponsorBlock), `github.com` (update check), `returnyoutubedislikeapi.com`
(Return YouTube Dislike) and `dearrow-thumb.ajay.app` (DeArrow thumbnails; its branding lookup uses
`sponsor.ajay.app`). Also exclude a custom SponsorBlock server's domain. Then force-stop and reopen YouTube.

## Known limits (summary)

- Premium, fullscreen and engagement-panel promotions were removed in controlled hook tests only; naturally
  delivered ones have not appeared yet. Preview-video and Explore-more-topics shelves match English headings only.
- AI channel lists are community-maintained and can misclassify channels, which is why they default off.
- SponsorBlock submission and voting have not been tried against the live server.
- Background playback needs a YouTube restart after its switch changes and leaves Shorts to YouTube.
- The first launch after a YouTube or module update rebuilds the hook cache and starts about 0.4 s slower.
- Module pages were checked in dark theme only. Light theme, tablets and right-to-left layouts are untested.
- arm64-v8a only. Only the setups listed here were tried; LSPatch was not.
