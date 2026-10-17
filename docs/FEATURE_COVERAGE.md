# Feature coverage

Current module: **1.0.0, versionCode 100**. The [current build record](../evidence/ai_audio_branding_20261018/build.json)
pins identity and counts. Evidence below retains the build on which each behavior was exercised;
531 final-build startup checks do not turn controlled cases into server-delivered positives.

| Surface | Implemented behavior and proof |
| --- | --- |
| Video ads | Two player hooks; live suppression logged |
| Feed/search ads | Shared component parser; live search replacement paths logged |
| Shopping/products | Live product_carousel and products_in_video_with_preview replacement logged |
| Premium components/banners | Independent BF gate and organic exceptions; natural positive pending |
| Native Premium offer | Controlled real-view off/on/off measurement 129/0/129 px; visibility preserved |
| Fullscreen promotions | _interstitial fact and shared BF decision; controlled real-hook suppression; natural positive pending |
| Shopping/Premium panel | Typed PAproduct/jumpahead real-hook tests; natural positive pending |
| Sponsored Shorts | Native video/image facts and BF pre-pager entry removal; paired metadata retained; live removal and advancing frames |
| Empty containers | Typed EmptyComponent replacement; complete independent empty-space/layout proof pending |
| Playables | Live game shelves/cards and Explore-row removal; off/on and cold-start restoration |
| Feed previews/posts/Shorts | Independent switches, live removals and root-header cleanup; Shorts tab/player preserved |
| Explore more topics | Own-heading/context fixtures and controlled actual-hook on/off with History negative; natural Home shelf pending |
| AI channels | Two independent AiSList switches, whole Unicode handles and persistent cache; high-confidence live search off/on |
| Force original audio | Typed multi-language original selection; native Hindi when off / English original when on; video advances |
| Fullscreen controls | Brightness/media volume, HUDs, restoration, disabled toggles and native tap/hold tested |
| SponsorBlock | Privacy-prefix retrieval and typed sponsor/outro seeks; BF defaults/window/category/type/duplicate gates |
| Settings and branding | In-YouTube page, persistent/reset preferences, exact YoutubeHideAds title and static shield/strike adaptive/monochrome icon |

[Settings/defaults and master dependencies](README.md#settings-and-defaults) are listed centrally.
Playables, feed filters, AI filters, swipes and original audio are independent of the ad master.
The master gates ad switches and SponsorBlock's effective enabled state.

## Behavior boundaries

Feed changes apply when components load; reload existing feeds. Preview/topics use their own English
headings and preserve ordinary shelves/History. Hiding feed Shorts leaves navigation/player usable.
Sponsored entries are removed before pager insertion; no automatic pager navigation is installed.

AI filtering applies only to supported own Home/related/search video and Shorts cards with validated
context. Channel rows, playlists and protected library/subscription contexts remain. Both community
list filters default off; optional lists can contain mistakes. Downloads are public fixed-URL GETs
with four-hour persistent caching. A warnlist-positive live card remains untested. There is no
in-app reporting/statistics or full Morphe per-scope configuration.

Original audio defaults on. It requires exactly one non-auto-dubbed ID ending .4 in a validated
multi-track list on the main thread. Unknown/ambiguous roles preserve native selection. A weak
controller/array check prevents repeated switching and respects a manual choice on the same list.
Switch changes apply to a fresh list/controller, normally the next video.

Fullscreen swipes are limited to the actual regular fullscreen player Activity. Brightness is
window-local and restores its prior value; volume uses the media stream. Controls/center/edges and
horizontal movement pass through, with native tap/hold replay. Advanced gesture options, persisted
brightness, real multi-pointer cases and fixed-volume routes are not certified.

SponsorBlock attempts once per playback generation with no cross-video cache/retry. Unknown player
types fail closed; live type 9 and a no-data public video continued without seek. There is no colored
seekbar, submission UI or channel whitelist. Client/OS spoofing, attribution-only hiding, end-screen
interception and complete Morphe parity are not implemented. Standalone feed/search/shopping,
cleanup and resolver BF programs are building blocks, not additional installed runtime hooks.

## Evidence

- [AI/audio, branding and controlled topics](../evidence/ai_audio_branding_20261018/README.md): final 77; controlled topics/App info milestone 75; initial list fetch milestone 76.
- Feed filters (`feed_filters_20261017`, removed before 1.0.0): final 74; live identification 72.
- Playables and swipes (`playables_swipes_20261017`, removed before 1.0.0): final 67, earlier Playables milestone 65.
- Sponsored Shorts (`shorts_sponsored_20261017`, removed before 1.0.0): final 60 and rejected navigation experiment.
- Controlled ad surfaces (`ad_surfaces_20261017`, removed before 1.0.0): final 44.
- SponsorBlock and panel roles (`remaining_20261016`, removed before 1.0.0): final 39.
- Earlier ad policy checks (`ad_hooks_20261016`, removed before 1.0.0): final 29.

Only the environment in [COMPATIBILITY.md](COMPATIBILITY.md) is certified.
