# Feature coverage, as verified

| Requirement | BF source | Policy JVM | Actual Xposed/YT behavior |
| --- | --- | --- | --- |
| Launcherless module and in-YouTube settings page | Platform work in canonical XAX | Real XAX callbacks compiled; BF engine self-check inside page | PASS on YouTube 21.41.525 / Vector 2.2, three navigation cycles; no standalone Activity |
| Video preroll/midroll/postroll ad | `ads/player/suppress_video_slot.bf` | Pass | NOT IMPLEMENTED |
| Feed paid renderer | `ads/feed/suppress_feed_item.bf` | Pass | NOT IMPLEMENTED |
| Search sponsored renderer | `ads/feed/suppress_search_result.bf` | Pass | NOT IMPLEMENTED |
| Shorts ad slot | `ads/shorts/suppress_shorts_slot.bf` | Pass | NOT IMPLEMENTED |
| Premium upsell | `ads/promotions/suppress_premium_upsell.bf` | Pass | NOT IMPLEMENTED |
| Paid shopping shelf | `ads/shopping/suppress_paid_shelf.bf` | Pass | NOT IMPLEMENTED |
| Empty ad container | `ui/collapse_filtered_container.bf` | Pass | NOT IMPLEMENTED |
| Resolver ambiguity rejection | `resolver/reject_ambiguous.bf` | Pass | NOT IMPLEMENTED |
| SponsorBlock eight-category auto-skip selection | `sponsorblock/select_sponsor_category.bf` | Complete 2,048-case reference and JVM checks; same-generation causal oracle | No XAX runtime, no SponsorBlock HTTP or Android seeking |
| SponsorBlock skip gate + 64-bit segment endpoint | `sponsorblock/authorize_seek.bf` | 54-suite-pass; binary and JVM differential tests | No runtime host or seeks; temporal predicate incomplete |
| One-call BF-owned SponsorBlock category and seek decision | `sponsorblock/sponsor_skip_pipeline.bf` | Exhaustive 2,048-category reference tests, JVM differential and desktop JNI router; no intermediate category permission | No player host, API calls, or actual seeks |
| SponsorBlock signed-long timestamp window | `sponsorblock/sponsor_time_window.bf` | Brainfuck computes `start ≤ current < end`, validated by reference and AOT JVM plus 63-bit boundary and cross-policy tests | No verified live timestamps, player-hook binding or Android seeks |
| SponsorBlock API, player identity, live timeline provenance, live seeks | none | Not run | NOT IMPLEMENTED |
| Persistent feature controls / RemotePreferences | none | Not run | NOT IMPLEMENTED; in-app status page exists |
| Hot reload / ad-feature compatibility | none | Not run | NOT IMPLEMENTED |

A JVM truth-table success indicates **only that the indicated decision program responds to synthetic bytes**; it is not proof that Android yields those inputs, that a hook can obtain them safely, or that its action can be applied safely.
