# Music exclusive audio and counterpart switching, build 163

Apply these exact-root transactions to the build 162 store at commit
`428adba0af389e005cc215a2624708dcabdcdcd0`. The machine-readable
[manifest](manifest.json) records every input/output root, carrier digest and store digest.

1. `00-startup.batch`: native XAX discovery, scoped exclusive hooks, public metadata,
   bounded matching, weak window/queue bindings, gesture and queue-job lifecycle, and packaged checks.
2. `01-settings.batch`: two independent rows in Music's shared Player controls group.
3. `02-metadata.edit`: build 163 metadata and the disjoint fifteen-field Music audio holder.
4. `03-labels.edit`: update the existing displayed development build label.

Use native `xaxc edit INPUT TRANSACTION OUTPUT`, then native `xaxc verify OUTPUT REPORT`
after **each** stage. The `.batch` files are literal native semantic records; `.edit` files
are native exact-root record carriers. They are transport for the canonical XAX graph.
No conventional application generator, private compiler patch or SDK lowering is required.
Build dependencies remain pinned in [toolchains.json](../../../../toolchains.json).

EXECUTED: independent replay through all four edits and mandatory verifications produced the
byte-identical final store. Reapplying the first edit to the final store failed with status 1
and the structured `WORKSPACE-EXPECTED-ROOT` diagnostic. Source SHA-256:
`ff4e75aeb9462917fdfb93d7bc57f8a2cd8d249a9e86fde26bb557aa67a54284`.

[Design and bounds](../../../../docs/MUSIC_AUDIO_PLAYBACK.md) ·
[Artifact and physical-device evidence](../../../../evidence/music_audio_20261118/README.md).
