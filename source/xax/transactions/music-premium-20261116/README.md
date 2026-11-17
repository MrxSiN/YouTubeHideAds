# Music Premium promotion transactions

These exact-root native transactions extend build 159 at commit
`fe783656e72e2b5330fbe8202d2c0265031ef1aa` to development build 160.
The canonical source remains [youtubehideads.xax](../../youtubehideads.xax).
The [manifest](manifest.json) records every input/output root and carrier hash;
[toolchains.json](../../../../toolchains.json) pins the native compiler.

Extract the baseline store from that commit. Set `XAX_REQUIRE_NATIVE=1` for native compiler
invocations. Apply stages in manifest order with `edit INPUT TRANSACTION CANDIDATE`, then
`verify CANDIDATE DIAGNOSTIC`. Empty verification diagnostics and successful status are required
before using a candidate as the next input. Publish only the final verified store. Stale roots
reject with status 1 and a structured diagnostic record, never a replacement store.

1. `00-premium.batch`: native BF/classifier checks, structural discovery, bounded field
   deduplication, protective account/membership/navigation/mealbar callbacks, separate readiness,
   weak view state and guarded Music startup. Shared policy, hook and DexKit helpers retain their
   existing content identities. Material types resolve through the host ClassLoader.
2. `01-metadata.edit`: declare twelve Music Premium state fields, code 160 and static branding digest.
3. `02-labels.edit`: update diagnostic version and the existing English Premium summary fallback.
4. `03-resource-identity.batch`: resolve named Music resource IDs and compare them to candidate
   view IDs. Unnamed/generated views are skipped without resource-name exceptions or disabling
   unrelated promotion hooks.

`.batch` is native workspace-edit transport from XAX's `docs/09_AI_PROTOCOL.md` section 16.
`.edit` is XAXEDIT1. Read-only SDK inspection and declaration/metadata serialization do not author
application graphs. Native edit/verify/resolve/build own mutation and compilation. Brainfuck
commands, packaged native libraries and third-party DEX are unchanged.
[Design](../../../../docs/MUSIC_PREMIUM_PROMOTIONS.md) ·
[Replay and device evidence](../../../../evidence/music_premium_20261116/README.md).
