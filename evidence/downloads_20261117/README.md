# Premium controls and downloads: development build 162

This November 17 record covers YouTube Premium header removal and shared YouTube/Music download
modes and export. This is unreleased source with separately signed development test APKs.
[Build identities](build.json) · [device scope and limits](device.json) ·
[design](../../docs/DOWNLOADS.md) · [Premium scope](../../docs/YOUTUBE_PREMIUM_PROMOTIONS.md).

## Native source and build

- **EXECUTED:** ten [exact-root native transactions](../../source/xax/transactions/downloads-20261117/manifest.json),
  mandatory verification, independent byte-identical replay from build 161, and
  [structured stale-root rejection](stale-root.txt). Final source SHA-256:
  `0856d74cda08076a32a5949ba205ea54b2e08fe3bd228cf8c1191e3538617037`.
- **EXECUTED:** native resolve/build for the production unsigned APK and signed Music/YouTube
  development variants. All four DEX files, eleven native libraries and static resource payloads
  match. Existing native/JNI and third-party DEX pins are unchanged. No release signing or release
  publication was performed. Exact toolchains and retention reason are in [build.json](build.json).
- **EXECUTED:** read-only inspection of 3,367 foreign declarations, zero descriptor errors.
  The final store has 761 functions and retains 544 of build 161's 563 function CIDs.
  New production implementation is native XAX with the existing BF authorization gate.

## Physical host checks

Pixel 8 Pro, Android 17/API 37, Vector 2.2/API 102; YouTube 21.45.88 and Music 9.45.51.
These are physical-device runs. Twelve new packaged protocol checks pass in both hosts.

- **EXECUTED:** naturally served You-page Premium action removal, with the header hook resolving
  structurally. [Scoped log](youtube-premium-startup.log). This does not establish every Premium
  surface or new switch-off/master-off coverage for the header rewrite.
- **EXECUTED:** YouTube's added player button preserves neighboring controls, opens the native
  quality dialog, and dispatches a completed native save. The two cache streams contain
  252,182/252,182 and 223,779/223,779 bytes, encryption type zero.
  [Native-save log](youtube-native-save.log) · [export result](youtube-export.json).
- **EXECUTED:** Music's real native download exported as one 3,449,447-byte M4A with one audio
  track, duration 213.0895 seconds. SHA-256 matches the original plain stream.
  [Measured result](music-export.json). The final ordinary Music APK reruns startup and export;
  [final device record](final-device-cleanup.json) owns that later identity/hash check.
- **EXECUTED:** separate SAF grant and real YouTube export. Its Opus/WebM and AV1/MP4 streams
  use the documented mixed-container fallback: two files. Both exported byte sequences match
  independent downloads of their original plain streams. No partial documents remain.
  [Measurements](youtube-export.json) · [runtime](youtube-export-runtime.log).
- **EXECUTED:** missing-downloader guidance with both modes enabled, in both apps; external takes
  priority. [Music settings/guidance](music-external-guidance.png). The final YouTube case includes
  reopening the same video without restarting its player. A prior candidate cleared that binding;
  the final transaction preserves validated same-ID navigation and confines invalidation to main.
- **EXECUTED:** final ordinary YouTube startup suites, unified settings and Back, unchanged
  preferences, installed APK hash, and restoration of the owner's original module/scope.
  [Regression](youtube-regression-result.json) · [installed identity](youtube-installed-identity.json).

The unchanged player progress callback occasionally logs a caught null-receiver during watch
startup; Vector restores native state. The download, save and export paths complete. RYD also
encounters the previously documented certificate-transparency filtering failure. These are not
reported as clean watch logs or as newly certified playback behavior.

## Controlled cache cases

**EXECUTED:** seven cases in a separate Music fixture APK: valid export, missing span, duplicate
span, bad index checksum, incomplete stream, rejected encryption type, and cancellation. Only
the valid case produces a completed file. Every case leaves zero partial documents and zero
fixture directories. The valid fixture splits at byte 17, exercising unaligned CTR decryption.
[Results](controlled-export.json) · [scoped runtime](controlled-export-runtime.log).

The tested fixture APK is code 39, with a different complete graph from the final ordinary APKs.
The [final fixture transaction](../../source/xax/transactions/downloads-20261117/fixtures/manifest.json)
replays and verifies against current production. Its entry and all 71 transitively referenced
functions are identical to the tested fixture. Normal APK DEX excludes the fixture mode marker;
the fixture APK contains it. Media bytes and private host database/key snapshots are not committed.

## Explicit limits and cleanup

**NOT RUN:** actual handoff into an installed downloader (none of the supported apps is installed),
compatible audio/video pair muxing (the real saved pair uses mixed container families), exported
file playback UI, other host versions, DRM/restricted/private media, process-kill recovery and full
Morphe menu/album/playlist-page parity. New modes default off and remain independent of ad settings.

Cleanup removes the fixture mode key, owned fixture input/output files and temporary state;
restores the original screen timeout, stay-awake and rotation settings; pauses media; and removes
the temporary YouTube regression module. The ordinary Music development module remains installed.
Real test downloads/exports and the selected folder grants remain available for inspection.
[Final observed cleanup](final-device-cleanup.json).
