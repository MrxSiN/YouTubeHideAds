# Music native welcome transactions

These exact-root native transactions extend build 160 at commit
`6997de2e438ee27b9438c37c867adce3cd87518d` to build 161. The
[manifest](manifest.json) records every carrier hash and input/output root. The canonical source
is [youtubehideads.xax](../../youtubehideads.xax), compiled with the exact
[toolchain pins](../../../../toolchains.json).

Extract the baseline store from that commit. Set `XAX_REQUIRE_NATIVE=1` for native compiler
invocations. Apply each stage with `edit INPUT TRANSACTION CANDIDATE`, then
`verify CANDIDATE DIAGNOSTIC`. Require successful status and empty verification diagnostics
before advancing. Publish only the final verified store. Stale roots return status 1 with a
structured rejection record.

1. `00-welcome.batch`: bounded structural controller/binding discovery, typed layout checks,
   shared Premium/BF authorization, weak candidate, one posted Runnable, native cancel action,
   guarded startup/queued callbacks and twelve startup checks. The existing five-node platform
   main-thread helper is reused; it reads no YouTube player state.
2. `01-metadata.edit`: five welcome state fields, code 161 and branding digest.
3. `02-labels.edit`: diagnostic version and the existing Premium summary fallback.

SDK use is read-only inspection and declaration/metadata serialization. Native edit, verify,
resolve and APK build perform application mutation and compilation. BF commands, JNI/native
libraries and third-party DEX remain unchanged.

The separate [fixture transactions](fixtures/README.md) exercise the same production scheduling
and cancel functions using host layouts with controlled listeners. They are excluded from final
APKs. [Design](../../../../docs/MUSIC_PREMIUM_PROMOTIONS.md) ·
[Build and execution evidence](../../../../evidence/music_welcome_20261117/README.md).
