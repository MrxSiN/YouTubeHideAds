# Premium and download transactions

These ten exact-root native transactions extend build 161 at commit
`2a7cefdf657da2c0e0423121159f2bc0c048165c` to development build 162.
The [manifest](manifest.json) records every carrier digest, input root and verified output.
The final store is [youtubehideads.xax](../../youtubehideads.xax).

Extract the baseline store from that commit. For each manifest stage run the pinned native
compiler with `XAX_REQUIRE_NATIVE=1`: `edit INPUT TRANSACTION CANDIDATE`, then
`verify CANDIDATE DIAGNOSTIC`. Require status zero and an empty verification diagnostic before
advancing. Native replay reproduced the final store byte for byte. Applying the first transaction
to the final root returned a structured stale-root rejection.

1. Premium own-thumbnail classification extends the existing BF-gated component callback.
2. Music startup installs shared download protocol, offline response/policy, public stream,
   command and cache-export roles. Effects reuse BF authorization.
3. YouTube startup installs those shared roles and bounded Premium header rewriting.
4. Music settings adds independent modes and current-item/export/folder/cancel actions.
5. YouTube settings adds the same actions using its existing row factories.
6. The player control refresh adds the YouTube download button and weak layout observation.
7. Metadata declares DownloadBindings, code 162 and the branding digest.
8. The diagnostic version label changes to code 162.
9. Activity-router installation removes an early Application-context dependency. Structural
   discovery works before application attachment and supports both host routers.
10. Navigation invalidation preserves a validated same-video binding, clears different IDs, and
    avoids invalidation from worker-thread command resolution.

Each startup/settings function is replaced in a separate stage, using a fresh native workspace
view. SDK use is read-only inspection and declaration/metadata serialization. Native edit/verify
perform all graph mutation; native resolve/build produce APKs. BF, native/JNI and third-party
DEX inputs are unchanged. [Design](../../../../docs/DOWNLOADS.md) ·
[Build and device evidence](../../../../evidence/downloads_20261117/README.md).

The separate [cache fixture transaction](fixtures/README.md) is excluded from normal APKs.
