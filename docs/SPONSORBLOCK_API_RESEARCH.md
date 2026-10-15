# SponsorBlock read API — research only

Upstream: <https://wiki.sponsor.ajay.app/w/API_Docs> (consulted 2026-10-15). This describes a remote service's contract; this repository does not contain a client yet and no live request was made.

- Public base URL described by upstream: `https://sponsor.ajay.app`.
- Read-only endpoint: `GET /api/skipSegments?videoID=...&categories=...`, with URL parameters `videoID`, `category` (repeatable) or `categories` JSON list, optional action types and service.
- Response is an array of segment objects: `segment: [start_seconds,end_seconds]`, `category`, `UUID`, `actionType`, optional `videoDuration` and other fields.
- Documented alternative with lower disclosure of viewing history: `GET /api/skipSegments/{sha256HashPrefix}`, typically four initial hex characters of SHA-256(video ID). The response may include several candidate videos: match the requested video identity *locally* before any segment is accepted.
- Skip-relevant category identifiers seen in the upstream docs include `sponsor`, `selfpromo`, `interaction`, `intro`, `outro`, `preview`, `filler` and `music_offtopic`; additional identifiers may exist and should not automatically be treated as skippable.
- Expected error cases include 400, 404, rate limiting and network failures. Correct behavior must be no synthetic skip segments and no blocking player/UI thread.
- Upstream explicitly disallows automated segment submissions; this project's planned client is read-only.

Iteration 5 now includes a real `.bf` program that gates auto-skip and selects the original **64-bit little-endian segment-end timestamp** supplied as source data. Tests cover all 64 Boolean combinations, boundary timestamps, binary bytes, malformed inputs and direct optimized/unoptimized JVM execution. The off-device ABI still refuses to execute seeks. **Pending:** real API transport/schema validator and JSON parser, generation-safe asynchronous cancellation, cache, seconds-to-milliseconds conversion, Brainfuck-computed time-window and overlap predicates, XAX networking/typed player seek and device verification.

## Iteration 6: category selection implemented in Brainfuck

`select_sponsor_category.bf` owns the auto-skip category decision for the eight chosen skip categories. The v1 wire order is `sponsor`, `selfpromo`, `interaction`, `intro`, `outro`, `preview`, `filler`, `music_offtopic`; the wire order is fixed and independent of upstream display names. Raw JSON category identifiers would require validated indexing into this eight-slot domain by the future XAX host. Unknown or unsupported categories must fail closed and never be silently reclassified. The one-hot representation is a wire validation constraint, not a hidden policy lookup. `hook`, `poi_highlight`, `chapter` and other special categories are **not** added to automatic skipping by this first eight-category policy.

Each candidate arrives with eight independent configured auto-skip bits and exactly one category-selector bit. Genuine BF outputs action code 5 only for a selected and enabled category; later policy `authorize_seek` consumes this choice as a Boolean gate. A generic, off-device causality checker validates feature identity and generation but does not decide whether a category is allowed. Positive seek actions remain disabled pending Android validation.
