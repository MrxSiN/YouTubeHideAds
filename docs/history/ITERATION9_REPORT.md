# YouTubeHideAds Iteration 9 — JNI dispatch proof and XAX bound call graph

Date: 2026-10-15. Research/build iteration; NOT a released Android module.

## Implemented

1. Added **real desktop JNI execution** via a *temporary, test-only* C shared library and test-only Java caller under `tests/jni/`. A Java native method calls JNI `FindClass`, `GetStaticMethodID` and `CallStaticObjectMethodA` to execute the actual AOT Brainfuck `dispatch_all.run([B)[B`, preserving the original BF feature logic. These harnesses are not application code and are excluded from runtime JARs and Android build adapters.
2. Added test vectors for all ten feature programs, optimized/unoptimized JVM modes, binary seek endpoint transport, incorrect selector, null input and missing policy class. The JNI probe propagates pending JVM exceptions rather than converting resolution errors into successful decisions.
3. Added `toolchain/xax/router_call_plan.py` with a pinned XAX JNI static-call type plan and a **bounded internal semantic graph** for the pre-resolved class/method. Both are external-XAX-dependent; the XAX compiler and graph were not run locally. No class resolution or managed export has been implemented in XAX.
4. Added `toolchain/xax/check_router_graph.py` with exact pinned Git revision gating for an optional external semantic graph construction check, and `docs/JNI_ROUTER_BOUNDARY.md` describing every still-unimplemented safety obligation.
5. Preserved the original ten `.bf` policies and derived Brainfuck router bytecode; no host-implemented ad suppression or SponsorBlock seek policy was introduced.

## Verification evidence

The full source baseline had 68 passing tests. Iteration 9 adds seven tests for the actual JNI execution and semantic-plan gate. Full `./scripts/build_fresh.sh` result: **75/75 tests passed** on Linux with GCC and Java 21. The complete current build log is distributed separately. JNI evidence is based on real JDK operations, not synthetic DEX/Android execution. The existing D8/APK tests still employ controlled synthetic fixtures because D8 and the Android SDK are absent.

Unoptimized and optimized policy/router JARs are byte-identical to Iteration 8. The complete build exit code is 0; language audit passes, and prerequisite diagnostics still report missing XAX/Android tooling.

## Honest completion boundary

- Actual JNI→Brainfuck router execution on **desktop JVM**: **verified**.
- Typed XAX pre-resolved `CallStaticObjectMethodA` graph source: **authored, external compilation unavailable**.
- XAX-owned classloader resolution, typed method-ID resolution, pending exception handling, exported managed JNI caller: **not completed**.
- XAX to Brainfuck **Android runtime invocation**, Android signed APK, DexKit hooks, API-102 framework attachment, SponsorBlock API client, device tests, actual YouTube ad removal: **not completed**.
- XAX redistribution permission: **unresolved**; no third-party XAX code was bundled.

Read `docs/JNI_ROUTER_BOUNDARY.md` for the exact callable contract and remaining safe-integration requirements.
