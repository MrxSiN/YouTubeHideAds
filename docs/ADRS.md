# Greenfield architectural decisions

## ADR-001: Brainfuck as executable policy, not annotation
Every feature source is standard 8-command BF. Annotation stripping is exact and source maps are preserved. No macro or comment affects behavior.

## ADR-002: direct JVM bytecode for the first AOT oracle
We emit an old JVM classfile (49) from the checked-in 8-command stream and test it directly on Java 21. This is a bounded cross-platform stepping stone, **not** proof of D8/Android compatibility. Generated Java/Kotlin feature source is prohibited; direct bytecode preserves provenance.

## ADR-003: refuse Android stand-ins
The current host cannot fetch the pinned XAX compiler into the test container or run an Android SDK/Vector framework. Until a verified canonical graph and DEX/APK composition exist, no handwritten third-language Android substitute is introduced. Source directories indicate missing components explicitly rather than misleading placeholders.

## ADR-004: safe failure and source attribution
A policy is not deployable until low-level evidence and action safety are proved against real runtime objects. Source research is pinned; patch behavior is described as research and must not be marked ported on the strength of JVM unit tests.

## ADR 002 — Host-wire contract before Android integration (2026-10-15)

**Decision:** Freeze a small, well-specified binary `bf-host-v1` message format and prove that genuinely compiled Brainfuck feature classes can be called through it on a JVM. Keep the codec/interpreter/JVM invoker strictly off-device; reject dangerous untyped actions. Derive Boolean input arity from the executable Brainfuck stream instead of textual metadata. Check byte-for-byte JAR identity against its original authoritative `.bf` source digest. Do not invent a canonical XAX semantic store or claim that a JVM JAR is a DEX/APK.

**Evidence:** `tests/test_host_abi.py`, `tests/test_host_link.py`, `tests/test_abi_vectors.py`, `contracts/bf_host_v1.md`; 26 passing automated tests; `scripts/probe_android_integration.py` records remaining blockers. **Risk:** The real XAX host is not yet proven to support all these operations, so this is transport design and conformance evidence, not Android feature readiness.

## ADR-006 — SponsorBlock category policy must be Brainfuck-owned (2026-10-15)

**Decision:** Represent the eight supported automatic-skip category IDs by fixed interleaved enablement and one-hot selector flags in the versioned binary host ABI. Validate only their shape at the generic host boundary. `select_sponsor_category.bf` computes the selected category's permission and emits action `5` (CATEGORY_AUTO_SKIP), which becomes the second gate of `authorize_seek`. Require the same generation at both stages; reject mismatched categories, stages and actions.

**Rationale:** Allowing the Android host to precompute category eligibility would contradict the Brainfuck-first policy boundary. The new executable `.bf` owns the exact decision without custom operators or annotation semantics. This does not authorize Android playback actions.

**Evidence:** all 2,048 source/JVM category cases, invalid one-hot and type rejection, multi-stage generation and gate spoofing regressions in `tests/test_sponsor_category.py`.
