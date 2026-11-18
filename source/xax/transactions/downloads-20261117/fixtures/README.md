# Controlled cache-export fixture

Apply `fixture.batch` to the production root named in [manifest.json](manifest.json), then run
native verification. This replaces only the export worker and its content-addressed callers.
It constructs an isolated SQLite/cache fixture in the host cache, runs the unchanged shared
exporter, and removes owned temporary state. It does not modify the host offline library.

The physical seven-case run used development fixture APK code 39. This transaction replays against
the final source. Its fixture entry and all 71 transitively referenced functions are identical to
the tested fixture, including the export algorithms. Unrelated host startup/router code differs.
The [evidence](../../../../../evidence/downloads_20261117/README.md) distinguishes those identities.

The test requires a granted SAF output tree and an unencrypted local audio input named
`yha-export-fixture-input.m4a` in the host cache. The measured input was 309,288 bytes, SHA-256
`a01b38c896d27707ef852301f1ccc6c39cebe792852c868109e85753ef159e47`.
Media bytes are not redistributed. Set the test-only global key
`youtubehideads_downloads_fixture` to `success`, `gap`, `duplicate`, `bad_checksum`, `incomplete`,
`drm` or `cancel`, then invoke Export downloads. Only success creates a completed output.
The valid fixture splits its encrypted stream at byte 17 to exercise unaligned CTR decryption.

Delete the global key and owned input after testing, then reinstall the ordinary development APK.
The normal APK must not contain the fixture mode marker. The fixture is not a production option.
