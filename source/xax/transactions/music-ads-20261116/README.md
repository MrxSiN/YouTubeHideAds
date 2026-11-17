# Music ad transactions

These native exact-root transactions extend the build 157 store at commit
`1de3af9804717499ac5f809b54f5978fa9fee677` to build 158. The canonical source remains
[`../../youtubehideads.xax`](../../youtubehideads.xax); these files are reviewable edit transport,
not another application source or a replacement compiler. [Manifest](manifest.json) records every
input/output root and SHA-256. [Toolchain pins](../../../../toolchains.json) identify the compiler.

Apply the files in manifest order using the pinned native compiler. Set `XAX_REQUIRE_NATIVE=1`.
For each stage run `edit INPUT TRANSACTION OUTPUT`, followed by `verify OUTPUT DIAGNOSTIC`;
use the verified output as the next input. The first input must be the baseline store extracted
from the named commit, not the current final store. Publish only the verified final store.
A stale expected root must be rejected. The native `.batch` grammar is documented in XAX's
`docs/09_AI_PROTOCOL.md` section 16; `.edit` uses the native XAXEDIT1 binary record format.

1. `00-music.batch`: package dispatch, shared discovery/initialization, Music classifiers, hooks,
   lifecycle preference loading, ads-only settings and native policy self-checks.
2. `01-module-metadata.edit`: both host scopes, development code 158, static branding digest and
   the shared initializer's explicit module-member reference.
3. `02-ui-scope.batch`: keep the existing SponsorBlock settings checks in the YouTube host.
4. `03-version-label.edit`: synchronize the shared diagnostics version label with module metadata.

Native authoring used queried baseline views and bounded semantic operations. The read-only SDK
was used for inspection and metadata/record serialization; application lowering and APK production
used the pinned native Windows compiler. No exported whole-program carrier was reconstructed.
The checked-in LF-normalized carriers were replayed and verified independently; final store bytes
match the tested candidate. [Evidence](../../../../evidence/music_ads_20261116/README.md).
