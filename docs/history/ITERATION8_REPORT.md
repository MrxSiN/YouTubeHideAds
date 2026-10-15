# YouTubeHideAds — Iteration 8 execution report

Date: 2026-10-15. This is a continuation of Iteration 7, not a completed Android module.

## Goal and implemented work

Introduce one actual executable Brainfuck callable entrypoint for the ten already-authored feature programs, without creating Python/Java/XAX-side policy switch cases. Preserve all existing Brainfuck source decisions and their digests while reducing the future typed XAX JNI call surface from ten method names to one.

1. **`toolchain/brainfuck/router.py`** derives a fixed one-byte selector mapping from the existing frozen BFH1 feature IDs; checks pointer confinement/loop balance for every Brainfuck source; inlines the unchanged executable eight-command bodies in conditionally executed Brainfuck branches; generates `generated/router.bf`, `brainfuck-router.jar` and `router.json`.
2. **Actual JVM execution**: emits `org.youtubehideads.bf.dispatch_all.run([B)[B` using the existing direct JVM AOT compiler, with baseline and optimized versions. A test-only Java reflection runner invokes the output. The router follows the `selector byte || source-policy payload` shape; the output is the original BF action bytes, unframed.
3. **Source/bytecode attestation**: class bytes are recompiled and matched exactly; the generated manifest binds source digest, command count, selector, feature ID, original file and compiled method; tampering fails.
4. **D8 optional linkage**: `toolchain/xax/link_d8.py` can send both the original ten-class policy JAR and the one-class router JAR through the same real D8 command when a capable host is available. `linked_router_smoke` verification requires a nonempty router `run([B)[B` DEX code item in addition to all ten originals, a controlled target scope, and no duplicate classes. Tests exercise the adapter with synthetic, noninstallable DEX and fake D8 only.
5. **Safety**: unsupported selectors emit zero bytes (reject, not pass), frame input is checked for generation and schema, and a correctly emitted BF seek target is rejected until a real Android player context is verified.

## Test evidence

The full `./scripts/build_fresh.sh` suite passes **68 of 68 tests**, including nine new Iteration 8 tests. Full transcript: `YouTubeHideAds_iteration8_full_build.log` (distributed as a separate report asset). Both generated JVM router variants pass the test oracle; all ten original BF policy sources and their compiled classes remain unchanged.

Tests encompass exhaustive selected-program equality over more than 2,300 valid inputs, both actual JVM compilation modes, `run([B)[B` reflection execution, 64-bit seek bytes, source/JAR tampering, invalid selectors, stale frames, and DEX synthetic linkage rejection. Source-level interpreter truth tables are not Android runtime evidence.

## Dependencies and blockers

- No pinned XAX checkout, its Python dependencies, Android SDK/D8, `adb`, Vector/libxposed runtime or Android device are present in this container.
- The existing canonical XAX smoke adapter and `BinaryTransport` remain **unexecuted against the real XAX toolchain**; the transport is still identity-only.
- The dispatcher is **real JVM bytecode executing real BF**, but there is **no XAX-to-router JNI call** and no ART invocation. No Android APK was built or installed; no ad suppression or SponsorBlock seek was executed.
- Resolving upstream XAX redistribution permissions remains necessary. No third-party XAX/Morphe source or binaries were bundled.

**Next blocking milestone:** construct a canonical XAX JNI invocation of the single router class using a verified module class loader, validate return arrays and exceptions, and run the controlled APK on a compatible Android device. Only after that should real DexKit-backed YouTube hooks be attempted. See `docs/BRAINFUCK_ROUTER.md`.
