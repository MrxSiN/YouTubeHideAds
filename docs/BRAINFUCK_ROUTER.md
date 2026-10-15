# Single-call Brainfuck policy router — Iteration 8

## Implementation and source authority

`toolchain/brainfuck/router.py` is an **off-device, deterministic compiler constructor**. It reads the ten annotated `.bf` programs, checks that every loop returns to the same tape cell, checks that no program moves the tape pointer below its starting cell, and emits a new **executable eight-command Brainfuck** source program at `generated/router.bf`.

There are ten selector branches. The selector test and loop execution are themselves `><+-.,[]`, not Python-dispatched policy logic. Each matching branch contains a **byte-for-byte identical 8-command stream** from its corresponding feature file. The compiler never interprets feature semantics, rewrites feature actions, or supplies host-side decisions. In each branch, the original BF program runs on a reserved tape window starting at cell 3; cells 0–2 are reserved for the selector, comparison, and one-shot branch flag. The pointer proof ensures all loops balance and body offsets return to the branch dispatcher. The builder refuses unknown, duplicate, or missing policies.

The builder emits one direct-AOT JVM class:

- Class: `org.youtubehideads.bf.dispatch_all`
- Method: `public static byte[] run(byte[] selectedPayload)` (JVM descriptor `([B)[B`)
- Input: **one selector byte** (1–10), then exactly the selected policy's already-defined raw payload. The selector byte is consumed by the BF router and not by the selected policy.
- Output: unchanged selected `.bf` program output bytes (`PASS`, suppress/collapse/reject, category, or `SEEK` plus eight little-endian endpoint bytes). It is *unframed*. The `BFH1`/`BFR1` host ABI still must be decoded and checked by the eventual XAX runtime, which must append the selector byte and validate the response.
- Invalid selector (0, 11–255): no bytes emitted, **not** an implicit `PASS`. A strict caller must reject an empty policy result and leave the target unchanged.

The router is **build generated**, not a replacement for the ten handwritten authoritative `.bf` programs. Its source and class-file hashes are attested against the current ten policy sources in `generated/router.json`; `verify_router()` re-compiles byte-identically before accepting an artifact. The router output must never bypass ABI request, generation, output-size or action validation.

## Frozen selectors

| Selector | BFH1 feature ID | Authoritative Brainfuck program |
| ---: | ---: | --- |
| 1 | `0x0101` | suppress_video_slot |
| 2 | `0x0102` | suppress_feed_item |
| 3 | `0x0103` | suppress_search_result |
| 4 | `0x0104` | suppress_shorts_slot |
| 5 | `0x0105` | suppress_premium_upsell |
| 6 | `0x0106` | suppress_paid_shelf |
| 7 | `0x0201` | collapse_filtered_container |
| 8 | `0x0301` | reject_ambiguous |
| 9 | `0x0401` | authorize_seek |
| 10 | `0x0402` | select_sponsor_category |

The numeric mapping is derived from ascending frozen v1 feature IDs. Changing or inserting an ID requires an explicit protocol version decision before release; the current builder's manifest binds all IDs and selectors.

## Execute and verify offline

```sh
PYTHONPATH=. python3 -m toolchain.brainfuck.router --out generated
PYTHONPATH=. python3 -m toolchain.brainfuck.router --out generated-optimized --optimize
PYTHONPATH=. python3 -m scripts.verify_linkage
PYTHONPATH=. python3 -m unittest -v tests.test_brainfuck_router
```

`tests.test_brainfuck_router` compares the router against every standalone BF program for more than 2,300 legal inputs, including all 2,048 category combinations and 192 six-gate/endpoint seek vectors. It also executes the actual generated JVM router in both compiler modes using a **test-only** reflection harness, tests the checked frame boundary, and confirms the positive BF seek remains denied for device execution. These are **JVM tests only**.

## Optional controlled D8 composition

When **real** pinned XAX and D8 toolchains exist, `scripts/link_xax_smoke.sh` now passes two separate source-attested JARs to D8 in a single invocation: the original ten policies and the router. The verifier requires all 11 DEX classes to have callable `run([B)[B` code items and scopes the unsigned result to `com.example.target` only. On this host no D8 has run. The D8 adapter's tests use a deliberately noninstallable synthetic DEX generator and fake D8 subprocess, which **cannot** establish DEX semantic equivalence, ART verification, or runtime execution.

## Next missing XAX integration

A single actual XAX JNI callable contract remains to be implemented: resolve and invoke `org.youtubehideads.bf.dispatch_all.run([B)[B` with the *module's defining class loader*, using an array containing the selector byte plus the validated payload, then check the result and apply authorized actions using a typed XAX host. Class-loader identity, JNI exception handling, byte-array ownership/lifetimes, generation checks and runtime fuel/exception consequences require an actual device oracle. **No XAX native call edge to the router is present in this iteration.** The research `BinaryTransport.roundTrip([B)[B` continues to echo its bytes and never dispatches feature logic. This project still has no YouTube hooks, DexKit runtime, live SponsorBlock API, functional APK, or Android device verification.

## Iteration 13 — scalable inlined router

| Selector | Feature ID | Program |
| --- | --- | --- |
| 11 | `0x0403` | `sponsor_skip_pipeline` |

The router now inlines eleven genuine Brainfuck policy streams. To avoid the JVM 65,535-byte method-size cap, the bytecode emitter shares safety exception handlers within regions on large programs. Per-command fuel charges, pointer checks, and output limits remain mandatory. The resulting class remains a single executable `dispatch_all.run([B)[B` method. This is an AOT JVM result only, not proof of compiled DEX or XAX invocation.
