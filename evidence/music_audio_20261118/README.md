# Music exclusive audio and counterpart switching, 2026-11-18

Development source **1.3.0, build 163** was exercised on a physical Pixel 8 Pro with Android
17/API 37, Vector 2.2/API 102 and Music 9.45.51. The accepted Music development APK uses code 67.
[Build identities](build.json) · [Structured device results](device.json) ·
[Native transactions](../../source/xax/transactions/music-audio-20261118/README.md).

| Status | Observation |
| --- | --- |
| EXECUTED | Native edit and verify for each of four exact-root stages, byte-identical independent replay, stale-root rejection and final canonical verification. The read-only audit inspected 3,579 foreign declarations with zero errors. |
| EXECUTED | Native unsigned production and signed development builds. The four DEX files, all eleven native libraries and packaged static resources match across variants. The resolved resource strings also match. Package differences are listed in the build record. |
| EXECUTED | On-device startup passed all 51 new packaged checks. The exclusive-audio capability and scoped external-controller hooks each authorized a live call. Both settings were exercised across a restart. |
| EXECUTED | A public track switched from video to song and back through Music's LOCAL queue. Both operations verified the target at the next index, actual advancement and removal of the exact previous entry. The return used the in-process pair cache. |
| MEASURED | The first switch completed in 2.26 s with one source metadata request. The cached return completed in 0.56 s with zero source metadata requests. Music retained song presentation after the return. Its native right-side control displayed video without starting another custom job. |
| EXECUTED | With both settings disabled, the left tap started zero custom jobs and exclusive audio recorded zero authorizations. With ad hiding off, exclusive audio authorized and the custom switch completed. A drag beyond touch slop started zero jobs. The second tap during an active switch was declined. Going Home during lookup cancelled the job before advancement. |
| EXECUTED | YouTube 21.45.88 startup, existing packaged checks, unified settings and Back passed with the same DEX. No Music audio feature started. The original YouTube module was re-enabled, the regression package removed and YouTube's saved module preferences matched their prior checksum. |
| NOT RUN | Real head-unit playback, remote/Cast queues, other host versions and forced late queue-executor failures. Production release signing was outside this development run. |

[Music switch log](music-accepted.log) · [Controls log](music-controls.log) ·
[YouTube regression log](youtube-regression.log) · [Feature behavior](../../docs/MUSIC_AUDIO_PLAYBACK.md).
