# SponsorBlock

The player **SB** button opens a compact bottom sheet. Its **Settings** row and the module’s **SponsorBlock settings** entry open the full settings pages. Native YouTube preference rows, named text appearances, navigation icons and theme colors provide the presentation. Back returns to the previous page. Long-press the manual skip prompt to open playback controls.

## Playback and controls

- Ten categories: sponsor, self-promotion, interaction, intro, outro, preview, filler, non-music,
  highlight and hook. Each has Ignore, Seekbar only, Manual, Automatic once and Automatic modes.
- Sponsor and self-promotion default to Automatic; other categories default to Ignore. The ad master
  and SponsorBlock enable switch still gate playback actions through the packaged BF policies.
- Each category has a visual color picker with a live preview, eight presets, and red, green, blue and opacity sliders. Presets retain the selected opacity. Existing ARGB values and desktop import/export remain compatible. Highlights are point markers. Native
  track geometry is resolved by DexKit structure; ambiguous roles preserve the native seekbar.
  Drawing clips the current thumb area. A previewed draft appears in white.
- Manual skip and undo recheck the player/video/generation. Undo suppresses another automatic skip
  for that segment during this playback and reverses its local skip/time-saved counters.
- Minimum segment duration, optional skip/error notices, channel exclusions, refresh, and local
  statistics are available. Configured exclusions pause skipping when the channel cannot be proven.

## Retrieval

The client sends four hexadecimal SHA-256 prefix digits to the selected HTTPS origin's
`/api/skipSegments/{prefix}`, requesting all supported categories and skip/poi action types.
Only the exact local video ID is accepted from the bucket. Limits remain 256 KiB, 1,024 video records,
100 segments and seven-day VOD duration. Numeric seconds convert with BigDecimal; malformed,
negative or inconsistent times, UUIDs, categories and player identities are rejected. A reported
duration must match within 1,000 ms. Live/unknown player types preserve playback.

One worker owns retrieval. IO failures, HTTP 408 and 5xx permit at most three attempts, with 2/4-second
delays driven by playback updates. HTTP 404 is authoritative empty data; other client errors are
terminal. Errors are never cached. An origin/video-scoped 32-entry LRU retains valid responses for
10 minutes and valid empty responses for one minute, across playback generations. Redirects are off;
connect/read timeouts are four seconds, with byte/read-count/elapsed limits and connection cleanup.

## Community actions and settings

The segment editor sets or adjusts boundaries, previews the exact range, then opens a review showing
video, category, range and server. Only the final **Submit this segment** action publishes. The reviewed
video/generation/server must still match. Automatic skipping is suspended during preview. Start/end
changes require another preview. Highlights require equal boundaries; range segments require start < end.

Segment controls provide upvote, downvote, undo vote and category correction. Public username changes
and community statistics use a private random identity, created only for an explicit community write
or supplied by the user. Optional skipped-segment view reporting defaults off. These operations use
documented API routes, bounded UTF-8 JSON, one operation at a time, no redirects and no automatic
POST retry. Successful submissions/votes invalidate retrieval data.

Import/export uses desktop categorySelections/barTypes JSON, modes, color/opacity, server, minimum
duration, notices and view tracking. Unknown categories are ignored. Duplicate known categories and
invalid known values reject the import. A worker validates the entire document before one preference
commit; invalid imports preserve existing settings. Input is limited to 64 KiB. Exports omit the
private identity unless explicitly requested; do not share exports containing it. Channel exclusions
and editor adjustment step remain local application settings.

## References and verification

Primary contract: [SponsorBlock API documentation](https://wiki.sponsor.ajay.app/w/API_Docs) and
[category/submission guidelines](https://wiki.sponsor.ajay.app/w/Guidelines), consulted 2026-10-21.
The user's [j-hc module reference](https://github.com/j-hc/revanced-magisk-module) points to
[Morphe patches](https://github.com/MorpheApp/morphe-patches/tree/e5464395441e916b643af4e2175c4e253e6df487).
The XAX implementation uses Android platform APIs and the existing BF/JNI boundary; no upstream
Java/Kotlin implementation was copied. Complete upstream patch parity is not claimed.

Runtime checks and device evidence are recorded in [testing](TESTING.md) and the
[2026-10-21 feature evidence](../evidence/sponsorblock_20261021/README.md) and [2026-10-22 UI evidence](../evidence/sponsorblock_ui_20261022/README.md). Test data is never published to the
community service: segment/vote/username POSTs are implemented but not exercised against production.
