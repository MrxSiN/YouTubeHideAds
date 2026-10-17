# Testing

Current acceptance is release 1.0.0 (versionCode 100) ([cold start](../evidence/release_20261018/README.md)) on the environment in [COMPATIBILITY.md](COMPATIBILITY.md).
The table combines current startup checks with explicitly dated earlier device experiments; it is
not a claim that every historical test was repeated on 1.0.0. [Evidence index](../evidence/README.md).

| Check | Evidence |
| --- | --- |
| Ad policies | 368 component + 16 panel fixtures, reference and compiled AArch64 emulation (fixture files removed before 1.0.0) |
| Requested ad surfaces | 24 new native/reference cases; controlled real Premium view and actual fullscreen/panel/Shorts hook calls pass |
| SponsorBlock policies | 14 window + 768 pipeline + 1,026 settings cases, reference and AArch64 emulation (fixture files removed before 1.0.0) |
| Settings exhaustive reference check | 39,366 valid present/value/default/master states |
| Current packaged startup | 70 ad + 277 SponsorBlock + 24 Playables + 28 swipe + 72 feed + 60 AI/audio = 531 pass on Pixel |
| Actual retrieval | Four-hex-digit prefix response with 123 video records; exact local ID yields one segment |
| Actual seek | Sponsor end 68,509 ms; outro end 76,737 ms; successful typed player result logged |
| Category defaults | Outro off initially; enabling it permits the same video's skip |
| No data | Public jNQXAC9IVRw response has zero matching segments; no seek |
| Live | Playing news stream type 9/duration 0; no SponsorBlock fetch or seek |
| Compatibility | Factory APK analyzed; downgrade rejected by Android, current app preserved |

JSON checks reject wrong video identity, unsupported category/action, string timestamps, reversed
ranges, negative and sub-millisecond-negative starts, wrong arity and invalid UUIDs. Decimal endpoint
conversion is checked exactly. Packaged BF replies must match both action and endpoint bytes.

External BrainfuckCC tests.reference.execute and Unicorn are test tooling, not repository source.
Fixtures contain data only. The XAX graph contains the actual startup self-checks; no fallback
implementation ships. Build via BUILD.md, install, force-stop YouTube and capture ADB logcat.
Hook installation alone does not prove positive removal of every surface.

Evidence and remaining limits: remaining_20261016 (`remaining_20261016`, removed before 1.0.0).
Controlled ad-surface milestone: ad_surfaces_20261017 (`ad_surfaces_20261017`, removed before 1.0.0).
Sponsored Shorts evidence: shorts_sponsored_20261017 (`shorts_sponsored_20261017`, removed before 1.0.0).

Live Shorts feed entries are removed before pager insertion. Device fixtures check paired tracking
data, off/empty/all-ad/last-ad/mismatched inputs, response-copy preservation and initial seeds.
Playback acceptance compares video pixels several seconds apart, including after manual transitions;
progress or position changes alone are insufficient. The old auto-navigation evidence is rejected.
Temporary diagnostic builds explicitly omit unchanged SponsorBlock vectors; final builds preserve
all 347 original checks.

## Historical Playables and fullscreen swipes (2026-10-17)

Build 67 adds 24 Playables and 28 swipe cases. All 399 startup checks pass on the Pixel. Swipe
cases cover eight native gate inputs, twelve bounded level calculations and eight intent cases.

On YouTube 21.41.525, the real Explore drawer loses only Playables; adjacent rows remain contiguous.
The direct games page loses its cards. Turning Hide Playables off restores cards after a cold
start. Its toggle was restored on through the same UI.

Actual fullscreen tests bind to MainActivity, show Brightness/Volume percentage overlays, change
brightness 5 to 31 to 5% and media volume 0 to 6 to 0, and restore the system-managed window brightness
on fullscreen exit. Taps reveal native controls and long holds show the native 2x indicator.
Horizontal movement leaves brightness/volume unchanged. Both switches off leave the fullscreen
window override NaN and media volume 0. Both switches and Hide Playables were restored on.
Temporary stay-awake was restored to 0; the feature never writes system brightness.

Shorts video content advances in two clips separated by a manual swipe. The captured log records
three sponsored entries removed before pager creation. Pixel comparisons exclude progress and
side controls; visual review confirms changes inside video content. No swipe action is logged
in Shorts. Real multi-pointer gestures, fixed-volume routes and another app version remain untested.

Evidence: playables_swipes_20261017 (`playables_swipes_20261017`, removed before 1.0.0).

## Historical feed switches (2026-10-17, build 74)

All 471 startup checks pass: the previous 399 plus 72 feed cases. The latter cover eight native BF
gates, component paths/payloads (including History and ordinary-shelf negatives), defaults, four
context combinations and authorization edge cases. Authored BF reference execution and packaged
binary alias equality also pass. Final semantic construction verifies; the installed APK hash
matches the promoted artifact. Only the existing f5/f9/f20 functions change from build 67.

Actual UI checks verify all four switches and on/on/on/off persistence across cold start. Live
preview/post/Shorts off/on evidence includes root-header cleanup and advancing Shorts video pixels.
The final build has no component probes. A live Home Explore more topics positive was not served;
its English-heading positive and History negative remain fixture coverage. Other locales are
unverified. Temporary stay-awake was restored to 0. Exact artifacts, milestone attribution and
remaining limits: feed evidence (`feed_filters_20261017`, removed before 1.0.0).

## AI/audio, branding and controlled topics (build 77)

[testdata/ai_audio_vectors.json](../testdata/ai_audio_vectors.json) records the actual 60 startup
cases: 16 native Boolean gates, 10 original-ID cases, 13 handle validation cases, 13 membership
cases and eight root-card cases. Unicode/case folding, partial-handle negatives, UC-ID/comment
rejection, auto-dubbed and malformed originals are covered. Authored BF reference checks and
packaged alias equality pass. Semantic reconstruction, all input digests and installed APK match.

Final-build high-confidence AI off/on search, original audio off/on native menus, controller
selection log and two video-content frames pass. Cache fetch counts came from intermediate 76;
controlled topics and App info branding came from 75. Milestones are explicitly labeled and not
represented as final-build network or natural topics proof. Final settings persisted and USB
stay-awake returned to 0. No data clear/uninstall or report submission occurred. Separate warnlist
live-positive, unknown versions and a natural Home topics shelf remain unchecked.
[Current evidence](../evidence/ai_audio_branding_20261018/README.md).

## Documentation and artifact checks

For documentation-only edits, validate local Markdown/image links and heading anchors, check JSON
contracts/fixtures still parse, compare stated identities with dated build records and run git diff
--check. Keep runtime source, native inputs, logs, measurements and the APK unchanged. Do not claim
a device rerun from a documentation check. The earlier Python/JVM conformance harness is absent;
its paths in the legacy contract identify historical tooling, not runnable repository commands.
