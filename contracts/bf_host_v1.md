# bf-host-v1: executable-host boundary (iteration 2)

This is a **normative, tested binary contract** for the *off-device conformance layer*. It is not an XAX graph/program, not an Android ABI implementation, and does not claim to be linked into DEX. Source-specific Brainfuck programs use unchanged `run(byte[]) -> byte[]` calls, compiled as direct JVM bytecode. The eventual verified XAX host must implement this framing and independently pass the provided golden vectors.

## Request framing (14-byte header)

`struct <4sBBHIH` (little-endian; packed):

| Offset | Field | Type | Requirement |
| --- | --- | --- | --- |
| 0–3 | magic | `byte[4]` | ASCII `BFH1` |
| 4 | major | u8 | 1 |
| 5 | minor | u8 | 0 |
| 6–7 | feature_id | u16 | fixed ID listed below |
| 8–11 | generation | u32 | host-scoped monotonic context generation |
| 12–13 | size | u16 | 0..256; exactly remaining byte count |
| 14.. | payload | raw bytes | a feature-specific binary record: all commands consume one input byte each; `authorize_seek` uses six Booleans followed by an 8-byte unsigned little-endian timestamp; `select_sponsor_category` uses 16 interleaved Boolean bytes (enabled flag, category-selector flag) for eight categories; `sponsor_skip_pipeline` uses those 16 bytes, five context-gate Booleans, and an unsigned little-endian 64-bit segment end; `sponsor_time_window` uses 24 bytes of start/current/end signed-long-compatible millisecond timestamps |

The host validates each feature's expected input count **from executable Brainfuck**, *not* from annotation text. Annotation edits cannot change input counts. Current programs execute their `,` instructions exactly once each. For suppression/resolver/cleanup features all bytes must be `00` or `01`. For `select_sponsor_category`, all 16 bytes must be Boolean and the eight odd-indexed category-selector bytes must contain **exactly one** `01`; reject absent/multiple selections without running Brainfuck. Category order is fixed: `sponsor`, `selfpromo`, `interaction`, `intro`, `outro`, `preview`, `filler`, `music_offtopic`. These wire positions do not license host-side skip decisions. For `sponsor_skip_pipeline`, the first 21 bytes are Boolean, category selection must be one-hot among offsets 1,3,...,15, and the endpoint is at bytes 21–28. For `sponsor_time_window`, none of the 24 bytes are Booleans: the three little-endian 64-bit integers must each be in the range 0..2^63−1. For `authorize_seek`, only the first six bytes are Boolean; bytes 6–13 encode `segment_end_milliseconds` as an unsigned little-endian integer in the range 1..2^63−1. Reject short, long, invalid-Boolean, zero, and out-of-range frames without executing a program. Object references are never encoded as raw pointers.

## Response framing (15-byte header)

`struct <4sBBHIBH` (little-endian; packed):

| Offset | Field | Type | Requirement |
| --- | --- | --- | --- |
| 0–3 | magic | `byte[4]` | ASCII `BFR1` |
| 4–5 | major, minor | u8, u8 | 1, 0 |
| 6–7 | feature_id | u16 | must equal request feature ID |
| 8–11 | generation | u32 | must equal current active generation |
| 12 | action | u8 | 0 PASS, 1 SUPPRESS_COMPONENT, 2 COLLAPSE_CONTAINER, 3 REJECT_RESOLUTION, 4 SEEK_PLAYER, 5 CATEGORY_AUTO_SKIP, 6 TIME_WINDOW_VALID |
| 13–14 | size | u16 | 0..256; exact trailing byte count |
| 15.. | action data | raw bytes | empty for codes 0..3, 5 and 6; code 4 has exactly eight destination bytes computed/emitted by Brainfuck |

Action 4 (`SEEK_PLAYER`) is still **not executable on Android**. `authorize_seek.bf` now evaluates six Boolean gates, reads the 8-byte segment end and emits either one byte `00` (PASS) or nine bytes `04` followed by the unchanged 64-bit endpoint. The off-device codec requires the output destination to equal the input endpoint and the active generation to match, but rejects all positive seeks pending a canonical XAX runtime host. This is a partial policy: the actual time-window predicate, segment merging, async cancellation and player identity verification are not implemented. Host generation and feature IDs must match; malformed, stale, mismatched, unauthorized and extra-payload responses leave the target unchanged.

## Numeric feature IDs (stable, never renumber)

| ID | Program | Allowed nonzero action |
| --- | --- | --- |
| `0x0101` | `suppress_video_slot` | 1 |
| `0x0102` | `suppress_feed_item` | 1 |
| `0x0103` | `suppress_search_result` | 1 |
| `0x0104` | `suppress_shorts_slot` | 1 |
| `0x0105` | `suppress_premium_upsell` | 1 |
| `0x0106` | `suppress_paid_shelf` | 1 |
| `0x0201` | `collapse_filtered_container` | 2 |
| `0x0301` | `reject_ambiguous` | 3 |
| `0x0401` | `authorize_seek` | 4, but deployment blocked |
| `0x0402` | `select_sponsor_category` | 5, category-policy authorization only |
| `0x0403` | `sponsor_skip_pipeline` | 4, but deployment blocked; one-call BF-owned category-and-seek gate |
| `0x0404` | `sponsor_time_window` | 6, timeline-member evidence only; no device seek |

These identifiers and action domains are protocol metadata, not feature classifiers. `toolchain/brainfuck/host_abi.py` is an **off-device test oracle**, not project-authored Python application runtime logic. The XAX host must perform the same validation via verified canonical semantic graphs. No policy decision is computed by the encoder/decoder. The legacy two-call SponsorBlock path requires the XAX host to execute `select_sponsor_category` before `authorize_seek`, use the Brainfuck category action as the second Boolean seek gate, and reject different generations, incorrect input encodings or forged inter-stage actions. `checked_sponsor_chain` is the **off-device conformance oracle** for this causal contract. Its tests execute real AOT JVM Brainfuck policies. The existing `authorize_seek` accepts an already-validated category gate but has not yet gained raw time-window computation; positive seeks remain blocked. This is not a deployable Android runtime implementation.

## Conformance and source integrity

- `testdata/bf_abi_v1_vectors.json` contains byte-exact source-derived fixtures for eligible and disabled inputs, including blocked SponsorBlock seeking.
- `tests/test_host_abi.py` tests round trips, corrupted framing, input bounds, stale generations, action authorization, and annotation invariance.
- `tests/test_host_link.py` compiles, loads and invokes the **actual generated JVM classes**, wraps their output, and rejects altered JAR bytes or stale source SHA-256.
- `python3 -m scripts.verify_linkage` validates the compiled JAR and optimized JAR against every original `.bf` command digest and byte-exact class emission.

Remaining platform work: Canonical XAX encoder/decoder, DEX/class composition, libxposed hook adapters, thread/typed action checks, generation lifecycle, device tests. The test oracle must never be shipped as an Android fallback implementation.

### Iteration 13 — one-call SponsorBlock alternative

`0x0403 sponsor_skip_pipeline` (29 bytes) replaces the legacy interstage category gate with one genuine Brainfuck computation. Its 16 category bytes select an auto-skip setting, its next five Boolean bytes bind host-provided enablement/generation/window/live/already-skipped predicates, and its last eight bytes are a signed-long-compatible positive little-endian endpoint. The generic host validates only shape, one-hot selection, timestamp range, and action/destination integrity; all category and seek Boolean conjunctions are performed in Brainfuck. The host cannot insert a forged category permission between separate calls. **The valid-segment-window flag is still supplied by an external player host; it is not derived from raw timestamps.** Device seeking remains categorically blocked until a separately verified XAX runtime can prove live playback context and handle exceptions.

### Iteration 14 — signed-long timestamp window and causal gate

The new stable feature `0x0404 sponsor_time_window` consumes exactly three eight-byte unsigned little-endian values constrained to the signed-long domain (0..2^63−1). The genuine Brainfuck commands calculate `start <= current < end` by bitwise unsigned comparison and return one-byte `06` (`TIME_WINDOW_VALID`) or `00`. The comparator has an explicitly annotated **2,000,000-command fuel limit**; the rest of the standalone policies retain the 100,000-command default, while the eleven/twelve-way inline router uses the maximum budget of its included branches. The XAX host remains responsible for proving that the three integers originate from the **same player, playback generation and authenticated SponsorBlock segment**; a syntactically valid binary request is not evidence of authenticity.

`checked_sponsor_time_chain` is an *off-device test oracle*, not Android host code. Its preconditions are (a) source/JAR-verified Brainfuck replies, (b) same active generation on both requests, (c) byte-identical `segment_end` between the 24-byte window request (offset 16) and the 29-byte SponsorBlock request (offset 21), and (d) the latter's `valid_segment_window` input byte (offset 18) equal to `1` iff the Brainfuck window result was `06`. Every spoofed, mismatched or stale transfer fails closed. Positive `SEEK_PLAYER` results continue to be categorically rejected by `checked_reply` until a real XAX player runtime has independently verified live state and is permitted to act.
