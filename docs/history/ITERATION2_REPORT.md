# YouTubeHideAds — Iteration 2 implementation and build report

Date: **2026-10-15**. Baseline: greenfield Iteration 1, commit `fefe967`. This is **not** a working Android/Xposed application.

## Changes implemented in this iteration

1. Introduced a **strict, versioned binary host-wire protocol**: 14-byte `BFH1` request header, 15-byte `BFR1` response header, little-endian numeric types, 9 immutable feature IDs, 256-byte payload cap, exact framed lengths, strict normalized Boolean fields, active-context generation matching and feature-appropriate action constraints. The protocol is specified in `contracts/bf_host_v1.md`.
2. Added a host-neutral **off-device** codec/reference dispatcher (`toolchain/brainfuck/host_abi.py`) which executes the authoritative executable Brainfuck code with no host-authored ad classifier. Annotation text does not control runtime input arity: the arity is computed from the executable `,` instructions.
3. Added `toolchain/brainfuck/host_link.py`, a real JVM integration oracle that invokes the generated compiled Brainfuck classes, wraps outputs in response frames and rejects stale or altered JAR bytes, source SHA-256 mismatches, changed class names or extra JAR entries. Tests cover both optimization modes.
4. Added byte-exact conformance vectors in `testdata/bf_abi_v1_vectors.json`, generated from the current executable programs, with tamper and generation tests.
5. Added `scripts/probe_android_integration.py` to report real environment status and blockers without fake APK success, and updated CI and fresh build orchestration to run source-linkage checks.
6. Safely rejected all positive SponsorBlock `SEEK_PLAYER` actions: the current preliminary policy does **not** select a typed 64-bit timestamp and the Android host is absent, so seeking cannot be enabled.

## Verified test results

- **26/26 Python unittest methods PASS**, including interpreter correctness, BF purity, real JVM differential tests, protocol edge cases, source class-byte provenance and generation checks.
- **9/9 AOT-generated JVM classes verified against source**, with both unoptimized and optimized builds.
- **18 golden synthetic v1 envelopes** generated; eligible/disabled variations for 9 features.
- Source-equivalent reproducible JVM JAR SHA-256: `6d633b4cb42fbd9d400269baa9ce7422db41b29bd8f8f82144f4db369b3e75c0`.
- Optimized reproducible JVM JAR SHA-256: `7b1bf926184abf380f92030a3b2e8cb492bb969cf2b1f67477447073d1e37a92`.
- Primary command: `./scripts/build_fresh.sh`. Raw transcript distributed separately as `YouTubeHideAds_iteration2_full_build.log`.

## Explicitly blocked / not claimed

- **No canonical XAX semantic store/Android host** has been built. No XAX Android `DEX`, Xposed lifecycle bridge or APK has been linked to the Brainfuck programs.
- No Android SDK, D8, ADB, Vector test device or pinned XAX compiler are available in the test environment. The pinned public XAX repository's GitHub metadata has no recorded license, and redistribution terms need verification before using upstream assets.
- **No DexKit integration, YouTube interception, ad removal, SponsorBlock network client, Android settings UI or device compatibility testing.**
- The reference codec is compiler/test infrastructure, not a hidden third runtime implementation language. All application feature actions still originate in genuine checked-in executable Brainfuck; no Java/Kotlin/C/Python Android feature fallback exists.

## Next concrete milestone

Provision legally usable pinned XAX tooling with Android SDK and Vector; create and verify genuine canonical XAX graph programs for the libxposed entrypoint and typed versioned ABI handler; link the AOT Brainfuck JVM class methods into generated DEX and produce a controlled-target signed module smoke-test APK. Then implement actual DexKit resolution and YouTube hook fixtures. Do not mark advertisement or SponsorBlock behavior as supported without separate actual device tests.
