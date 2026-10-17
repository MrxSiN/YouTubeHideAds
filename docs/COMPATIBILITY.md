# Tested compatibility

Canonical module: **1.0.0, versionCode 100**. Tested through 2026-10-18.
The declared minSdk 28 and libxposed API 102 requirement do not certify untested Android/framework combinations.

| Device | Android | YouTube | Framework | Observed |
| --- | --- | --- | --- | --- |
| Pixel 8 Pro, arm64 | 17 / API 37 | 21.41.525 | Vector 2.2 / API 102 | 531 startup checks; final 77 AI/audio off/on, advancing video and artifact identity; earlier live ad/Shorts/Playables/feed removal, SponsorBlock seeks and fullscreen swipes; controlled Premium/fullscreen/panel/topics cases |

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
