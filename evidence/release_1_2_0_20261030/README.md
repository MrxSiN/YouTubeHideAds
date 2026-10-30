# Release 1.2.0 (builds 154 and 155), 2026-10-30

Pixel 8 Pro, Android 17, Vector 2.2 (libxposed API 102), YouTube **21.43.523**. [Build identity](build.json).

## YouTube 21.43 regressions (build 154)

The 1.1.0 log on 21.43.523 showed two features failing closed:

| Log line on 1.1.0 | Cause | Fix |
| --- | --- | --- |
| `Background playback roles unresolved/ambiguous; native behavior preserved` | The background-settings caller `pgc.a` now also invokes `Iterator.hasNext()` and `j$.util.Optional.isPresent()`; only `java.lang.Boolean` was excluded, so three Boolean callees matched | The callee must be declared in a default-package (YouTube) class; `nja.L()` resolves, matching `nli.H()` on 21.42 |
| `Player progress diagnostic unresolved/ambiguous` (no `SponsorBlock player hook installed`) | The progress method `astx.bW` invokes `asxj.av()` twice; discovery counted invoke sites | A repeat of the previous match is not counted |

After the fix every hook installs ([runtime log](runtime-155.log)). Audio continued for a video opened
from a link after Home and with the screen off (`AudioPlaybackConfiguration … state:started`,
launcher on top), with `Background playback authorized: eligibility` and `kids policy` logged.
`Original audio selected: en.4` was logged for `TQHEJj68Jew`.

## Update check and problem report (build 155)

- **Check for updates** switch under About ([screenshot](settings-about.png)); toggling it wrote
  `update_check` false/true to `youtubehideads.xml`.
- One `HEAD /releases/latest` per YouTube start, User-Agent `YouTubeHideAds/1.2.0`.
- The dialog ([screenshot](update-dialog.png)) and both buttons were exercised with a probe build whose
  request went to a local server answering `302 → …/releases/tag/v1.1.0` and whose local version key was
  lowered to 1.0.0: **Later** dismissed it; **Update** started `ACTION_VIEW https://github.com/…`.
- **Report a problem** ([screenshot](diagnostics-report.png)) opened
  `https://github.com/MrxSiN/YouTubeHideAds/issues/new?title=%5BBug%5D+&body=…`. No issue was submitted.
- **Copy compatibility report** still copies the report, whose header reads `YouTube Hide Ads 1.2.0 (155)`.

## Limits

- This phone runs AdGuard with its certificate in the system store. Inside YouTube, connections to
  `sponsor.ajay.app` and `github.com` fail Certificate Transparency
  (`SSLHandshakeException … NOT_ENOUGH_SCTS`), so live SponsorBlock segments and a live update prompt
  were not observed here. The real certificates carry SCTs.
- New strings (update dialog, switch, report row) are English only.
- Light theme, tablets, other devices and other YouTube versions were not tested.
