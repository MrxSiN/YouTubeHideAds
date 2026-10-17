# Morphe behavior-reference inventory

This is the inspected subset used by this project, not a complete recursive inventory or a claim
of Morphe parity. Most references were inspected at commit
`e5464395441e916b643af4e2175c4e253e6df487` of
[Morphe Patches](https://github.com/MorpheApp/morphe-patches/tree/e5464395441e916b643af4e2175c4e253e6df487).
The earlier swipe/Playables pass read moving-main files; see [provenance](UPSTREAM_PROVENANCE.md).
Morphe modifies APK bytecode/resources. Its implementation cannot be assumed reusable as runtime
libxposed hooks. No Morphe Java/Kotlin implementation was copied.

| Reference | Inspected mechanisms | Independent runtime equivalent / status |
| --- | --- | --- |
| Hide ads / AdsFilter | Video-ad fingerprints, component groups and exceptions, Premium measurement, panel identifiers, client/endpoint hooks | Typed XAX hooks and BF policies; live video/search/product removal, controlled Premium/fullscreen/panel tests; no client/OS spoofing |
| HideFullscreenAdsPatch | Serialized _interstitial fact plus existing component classification | Shared XAX extractor and BF ad_fullscreen; controlled real-hook positive passes |
| Shorts ad selection | ReelPageAdsInterface and minTsla diagnostics, native video/image ad helpers | Native facts authorize BF suppression and pre-pager entry removal; live removal and advancing video verified |
| SponsorBlock | Video/progress/type hooks, typed seeks, categories, resource/UI dependencies | Bounded privacy-prefix client and BF window/category/pipeline policies; live sponsor/outro seeks; no overlay/submission UI |
| Channel whitelist | Channel preferences, flyout item and ad-patch dependencies | Standalone policy has a whitelist input; no shipped whitelist persistence/UI |
| LayoutComponentsFilter / ShortsFilter / HorizontalShelvesFilter | Games components, selected feed sections and context exclusions | Playables, previews, topics, posts and feed Shorts controls; own payload and typed context guard |
| SwipeControlsConfigurationProvider / ClassicSwipeController / PlayerType | Separate brightness/volume switches, fullscreen state and native gesture coexistence | Window-local brightness and media volume with independent toggles; actual Pixel calibration; advanced options omitted |
| AiSListFilter / AiSListRequester / AiSListPatch | Whole-handle lists, block/warn choices and four-hour refresh | Exact Unicode-handle own-card filter and bounded persistent caches; live high-confidence search off/on; no in-app reports/statistics or full per-scope configuration |
| ForceOriginalAudioPatch and shared audio-track fingerprints | Original .4 track convention and typed selection for newer playback | Typed SABR update/controller setter, unique non-dubbed original and BF gate; Hindi off / English original on verified |

The pinned ad sources include HideAdsPatch.kt, its Fingerprints.kt, AdsFilter.java and the shared
engagement-panel/fullscreen helpers. AdsFilter's ordinary-content exceptions informed fact
extraction; hiding attribution alone is not implemented. PAproduct/jumpahead roles use the typed
request-to-ID helper, not protobuf toString. No label-only disguise or endpoint OS-name rewrite ships.

Actual YouTube 21.41.525 DEX supplied the unique runtime member roles. Earlier notes that player
anchors or Premium measurement were future work are superseded by the recorded hook/device tests.
Not all upstream dependencies, settings or version differences have been inspected.

[Current feature coverage](FEATURE_COVERAGE.md) · [Resolver contracts](DEXKIT_RESOLUTION.md) ·
[Evidence](../evidence/README.md)
