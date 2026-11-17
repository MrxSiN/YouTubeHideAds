# Downloads in YouTube and Music

Development build 162 adds **In-app downloads**, **External downloads**, and **Export downloads**
to each host's YouTube Hide Ads settings page. Both modes default off and use that host's own
preferences. They are independent of Hide ads. If both are enabled, external downloads take priority.
The released 1.3.0 APK predates these changes.

New download labels and guidance currently use English fallbacks. Physical checks and untested
cases are recorded in [the dated evidence](../evidence/downloads_20261117/README.md).

Enable In-app downloads to save the current player item using the host's offline library and
quality selection. YouTube has a download button beside its player controls. Both settings pages
also have a current-item action. Music's matched native player download action uses the same path.
Matched top-level download and upsell commands with an unambiguous video or playlist ID are
converted to native ADD commands. Removal, refresh, unrelated purchases and command containers
retain their original behavior. This is not full Morphe album/menu/playlist-page parity.

External downloads send a canonical watch or playlist link as plain text to the first available
supported app: Seal, YTDLnis, then NewPipe. Install and configure a downloader separately. A missing
downloader produces guidance and consumes the download action. No account tokens, signed stream
URLs or cookies are passed to the downloader.

Choose **Choose export folder** once in each app, grant access to a folder, then choose
**Export downloads**. Keep the app open until it finishes. **Cancel export** requests cooperative
cancellation. Completed files remain; owned temporary files and incomplete output documents are
removed on handled failure or cancellation. This increment has no foreground service or recovery
after process termination.

## Architecture and bounds

All implementation is native XAX. The existing Brainfuck AND3 gate authorizes effects after XAX
validates settings, structural roles, identity, thread and freshness. Startup installers are guarded
independently. Twelve protocol checks run before download hooks are installed. Discovery uses
semantic anchors, signatures and relationships rather than host class names or version offsets.
Current player models, command routers, loggers and view roots are weakly referenced where retained.
The current-item action checks its displayed item again at click time.
Navigation invalidation runs on the main thread: a different valid video ID clears the binding,
while reopening the same validated video preserves it when the host reuses its player.

The host owns download scheduling, database state, playback and native quality selection. A
bounded off-main response hook marks suitable public streams offline eligible and supplies the
host's offline policy. Existing usable current-item streams are preferred. Otherwise, a public
VISIONOS visitor registration and player request obtain direct streams without forwarding account
headers or cookies. HTTPS requests reject redirects, use four-second connection/read timeouts,
an eight-second read deadline and a four-MiB body limit. Expired, ciphered, DRM and unsupported
formats are rejected. The Cronet GET override applies only to eligible registered plain streams;
it does not change arbitrary host traffic. See the [exact contract](../contracts/downloads_inputs.json).

Export reads the host's completed offline rows and existing cache key through host APIs. It does
not persist keys or log stream URLs. Only the supported cache encryption type is accepted; DRM
samples are rejected. The EXI2 index must pass its checksum and EOF validation. Cache spans must
be unique, contiguous and canonically inside the selected stream root. AES-CTR output uses the
cache's nonce and position rules, including unaligned spans. MediaExtractor validates tracks;
compatible audio/video pairs use MediaMuxer. Incompatible pairs export separately.

Each export is limited to 16 databases, 100 items, two streams per item, four GiB per stream and
one hour. Index limits are 64 MiB, 65,536 entries, 64 metadata fields per entry and one MiB per
metadata value. Copying uses a 64-KiB buffer. One job runs per host. SAF output is created with a
unique partial name and renamed only after closing successfully. Export never removes host downloads.

Private or restricted videos, paid content, unavailable streams, DRM, unsupported cache revisions,
other downloaders, background process survival and every future host version are outside the
verified scope. Public endpoint behavior can change independently of the app version.

## Reference

Behavior and protocol references were inspected at Morphe commit
[`31234a8465683a389bcfba25ad636fd1cd38fd02`](https://github.com/MorpheApp/morphe-patches/tree/31234a8465683a389bcfba25ad636fd1cd38fd02),
including the YouTube/Music Downloads patches, shared BaseInAppDownloadsPatch,
OfflineVideoExporter, offline/player-response schemas, visitor requests and activity command router.
The adaptation follows this repository's shared XAX/BF host architecture. No Morphe Java/Kotlin
implementation or patcher is packaged. Existing [Morphe terms](../LICENSES/Morphe-NOTICE.txt)
remain in source and APK resources.

The cache index checksum follows the primary
[ExoPlayer CachedContentIndex implementation](https://github.com/google/ExoPlayer/blob/r2.19.1/library/datasource/src/main/java/com/google/android/exoplayer2/upstream/cache/CachedContentIndex.java).
