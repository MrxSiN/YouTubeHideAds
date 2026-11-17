# Music background playback transactions

These exact-root native transactions extend Music ad build 158 at commit
`86d83b78079c2229f3afddf43839a0aea997eb62` to development build 159.
The canonical source remains [youtubehideads.xax](../../youtubehideads.xax).
The [manifest](manifest.json) records input/output roots and carrier hashes; the native Windows
compiler identity is pinned in [toolchains.json](../../../../toolchains.json).

Extract the baseline store from the named commit. Set `XAX_REQUIRE_NATIVE=1`, then apply the files
in manifest order. For each stage run `edit INPUT TRANSACTION CANDIDATE`, then
`verify CANDIDATE DIAGNOSTIC`; use only a verified output as the next input. Publish only the final
verified candidate. A stale expected root must reject. Native batches are workspace edit transport
documented in XAX's `docs/09_AI_PROTOCOL.md` section 16; `.edit` files are XAXEDIT1 records.

1. `00-background.batch`: native policy/host checks, structural discovery, protective eligibility and
   kids-policy callbacks, separate readiness, bounded deoptimization, shared settings rows and Music
   startup. It reuses the existing BF gate, preference getter, hook installer and DexKit session.
2. `01-context.batch`: the existing Application callback publishes its attached Context. This stage
   uses handles rebound to its own exact input root; caller and lifecycle edits are verified separately.
3. `02-metadata.edit`: declare the three volatile Music state fields, code 159 and the new branding digest.
4. `03-version.edit`: update the existing diagnostic version literal to match module metadata.
5. `04-startup-guard.batch`: share YouTube's synchronous completed-future guard pattern so an
   unexpected background discovery exception preserves Music's ad and settings startup.

The read-only SDK inspects semantic objects and serializes declarations/metadata; application graph
editing, verification, resolve and APK build run through the pinned native compiler. No whole-program
carrier or application implementation in another language is generated. BF commands and packaged
native/third-party DEX inputs are unchanged. [Build and device evidence](../../../../evidence/music_background_20261116/README.md).
