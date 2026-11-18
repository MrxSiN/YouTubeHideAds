# Release 1.4.0 (versionCode 165), 2026-11-18

Release of development builds 158-164 (merged pull requests #11-#16). [Build identities](build.json) ·
[Version transactions](../../source/xax/transactions/release-1.4.0/manifest.json).

## Construction

**EXECUTED:** seven single-mutation native transactions on build 164 update every version string
(`YouTubeHideAds/1.4.0` user agent x2, `YouTube Hide Ads 1.4.0 (165)`, `1.4.0 (165)`, `1.4.0`), the
update-check version constant (1004000) and the module record (1.4.0, 165, rebuilt branding archive with
versionName 1.4.0). Each stage verified; independent replay is byte-identical and a stale replay is rejected.
`xaxc build-signed` (XAX `fa6d2ed`) produced the APK, signed with the release certificate `3c4644a0...926b`.
Compared with the device-tested build 164, only `AndroidManifest.xml` and the two application DEX files
(version literals and constant) differ.

## Device checks

Pixel 8 Pro, Android 17/API 37, Vector 2.2/API 102, YouTube 21.45.88, YouTube Music 9.46.51.

| Status | Observation |
| --- | --- |
| EXECUTED | Installed over the released 1.3.0 (157) as an update; package reports 1.4.0 / 165. |
| EXECUTED | YouTube cold start: every startup self-check passed and every hook installed, 0 hook crashes. [Log](youtube-startup.log) |
| EXECUTED | YouTube video opened from a link: video ad suppressed, 0 hook crashes. [Log](youtube-video-open.log) |
| EXECUTED | YouTube Music cold start with Music added to the release module's scope: every Music self-check passed and every hook installed, 0 hook crashes. [Log](music-startup.log) |

Feature-level checks of the identical build 164 code are in [the build 164 evidence](../perf_20261118/README.md).

After the checks the release module's scope was set back to YouTube only and the separately installed Music
development module was re-enabled for Music, as before the run.

**NOT RUN:** Music Premium/welcome surfaces on this APK (not served), download save/export on this APK, other
devices, versions and themes.
