# Tested compatibility

Canonical source and installed build: **1.2.1, versionCode 127**. Targeted slider/UI checks passed
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
