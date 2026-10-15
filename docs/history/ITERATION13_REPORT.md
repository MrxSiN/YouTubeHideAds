# YouTubeHideAds — Iteration 13 engineering report

**Date:** 2026-10-15 (Asia/Kuala_Lumpur)

**Scope:** One-call SponsorBlock category-and-seek decision entirely within genuine Brainfuck, plus compact code generation for the eleven-branch AOT JVM router.

## Completed and executed

1. Added `source/brainfuck/sponsorblock/sponsor_skip_pipeline.bf` (ID `0x0403`). It consumes 16 interleaved category configuration/one-hot selector bytes, five runtime evidence Boolean flags, and an eight-byte little-endian seek endpoint (29 bytes total). It produces `PASS` or `SEEK_PLAYER` plus the original 64-bit endpoint. It does not receive a host-computed intermediate category permission.
2. Caught and fixed a genuine Brainfuck scratch-state issue: the eighth/last category, if selected but disabled, could leave cell2 nonzero. The combined program now clears cells1 and 2 before the five remaining conjunction gates. The bug is covered by direct tests.
3. Kept both older SponsorBlock programs and numeric IDs intact; the new one-call program is an additional, safer compositional alternative. The generic host still validates framing/one-hot encoding, timestamp range and generation without deciding feature eligibility.
4. Extended the source registry, versioned ABI, source-derived vectors and the inlined Brainfuck router to **11 policies**.
5. Addressed the Java 65,535-byte single-method Code limit exposed by the eleven-program router. Source-based AOT emission now deduplicates JVM exception paths per bounded region for large programs. Error handling is still executed on every source instruction, and optimized instructions still spend the original number of Brainfuck instruction units. A regression catches region boundaries skipped by optimizer coalescing.
6. Added seven new automated tests: six for category/pipeline behavior and one for JVM compact emitter guard behavior. Updated preexisting exhaustive, JNI, and framing tests for the 11th selector.

## Independently verified

| Verification | Result |
| --- | --- |
| Automated tests | **108/108 PASS** |
| Exhaustive category/settings equivalence | **2,048 cases**, plus five-guard and binary endpoint tests |
| Final disabled category regression | PASS |
| Baseline/optimized JVM policy and router | PASS |
| Test-only desktop JNI classloader probe | PASS in both modes |
| JVM compact-handler fuel/pointer/output safety | PASS in both modes |
| Source-to-JVM JAR integrity verification | PASS |
| Language purity audit | PASS |
| Android toolchain preflight | BLOCKED, recorded separately |

The combined shell build wrapper did not complete within the tool execution limit; independent execution of tests, four AOT builds, linkage verification, audit and environment diagnostics completed. No unsupported full-wrapper success is claimed.

## Android/XAX status

The canonical XAX Android host is still **not compiled**. The pinned XAX checkout, Android SDK, D8, ADB, libxposed/Vector runtime and device integration are absent here. Neither the new policy nor the router is wired to a real XAX hook, DexKit member resolver, SponsorBlock service, or Android playback engine. These are JVM research/build artifacts only; no installable APK or working YouTube ad removal has been produced.

The new policy continues to depend on the host supplying valid contextual Booleans, including the segment-window predicate, from verified live player state. It does not compute this predicate from start/current/end/duration times. Until an actual XAX runtime enforces those proofs, **positive seeks remain categorically blocked** by the off-device boundary.

## Next actionable dependency

Obtain a properly licensed checkout of pinned XAX `9e44eedfc241d25bb5062b38af105f75234000e2` plus Android SDK/D8 and compatible device runtime. Compile and verify the XAX graph; establish the actual classloader-qualified JNI call to the Brainfuck router, then implement the member resolver and hook lifecycle. No C/Java/Python Android feature fallback is authorized.
