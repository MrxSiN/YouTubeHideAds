# Hot-path fixes, build 164

Apply these exact-root transactions to the build 163 store at commit
`501cc23fe178849f23552580faa80a3b2c3aa277`. The [manifest](manifest.json) records every
input/output root and store digest.

| Stage | Change |
| --- | --- |
| `00-hot-paths.batch` | Player progress hook returns before invoking on a null player response (`PLAYBACK_PENDING`). Feed shelf and AI root-card classifiers check their fixed `startsWith` prefixes before their anchored regexes. |
| `01-player-type.batch` | The player-type check compares the seven names its full-match regex accepts with `String.equals`. |
| `02-music-pill.batch` | Music Audio/Video pill search resolves `player_page` and the pill container ID once per search, not with a `getIdentifier` per visited view; no pill resource ends the search at once. |
| `03-music-ad-gate.batch` | Music's two ad classifiers call the AND3 gate only when their matched-fact input is true. |
| `04-metadata.edit` | Version code 164 and the static field `PolishBindings.container`. |
| `05-downloads-container.batch` | `@player_container_id`: `player_additional_view_container` resolved once per process (the existing `PolishBindings` cached-ID pattern); the downloads button attacher uses it. |
| `06-speed-container.batch` | The speed button attacher uses the same cached ID. |
| `07-sponsorblock-container.batch` | The SponsorBlock controls attacher uses the same cached ID. |
| `08-labels.edit` | Displayed development build label `1.3.0 (164)`. |

Every change returns the same result for every input:

- a regex now runs only on a string that already has its required prefix;
- a resource ID cannot change within a process;
- the startup self-check proves AND3 is false whenever an input is false, and disables the
  feature otherwise.

Several stages hold one `replace` each because one `xaxc edit` batch replacing two functions with
shared owners can write a store that `xaxc verify` rejects (`XAX.IDENTITY.OBJECT_MISSING`), while
each replacement alone verifies.

Use native `xaxc edit INPUT TRANSACTION OUTPUT`, then native `xaxc verify OUTPUT REPORT` after
**each** stage. Toolchains are pinned in [toolchains.json](../../../../toolchains.json).

EXECUTED: replay of all nine stages from the build 163 source, each verified, produced the
byte-identical final store. Reapplying the first stage to the final store failed with status 1
and `WORKSPACE-EXPECTED-ROOT`. Source SHA-256:
`3fa31b5a8d719fdc0b8f3b05e1211f314365df9fbbb52145b484f242dc422316`.

[Evidence](../../../../evidence/perf_20261118/README.md).
