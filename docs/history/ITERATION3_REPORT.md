# YouTubeHideAds — Iteration 3 implementation and verification

Date: **2026-10-15**. Continued from git commit `0d31383` (Iteration 2). This release is **compiler and XAX-integration preparation only**, not a working Android ad-removal module.

## Implemented in new project source

1. `toolchain/xax/smoke_build.py`: independently authored build orchestration for pinned XAX semantic builder APIs. Constructs two typed, no-op JNI lifecycle callback graphs (`onModuleLoaded`, `onPackageReady`) plus managed libxposed entry and scope metadata. Calls canonical XAX `resolve_packages`, `snapshot_store`, `write_store`, `verify_store` and `build`. Uses a pinned **external XAX testing Activity** solely for an unsigned controlled-target smoke build, not as application runtime or as a shortcut to the new manager UI.
2. `scripts/build_xax_smoke.sh`: guarded invocation requiring `XAX_SOURCE_DIR`; does not try to fabricate missing binaries, text-based XAX, or standalone Android hooks.
3. `toolchain/xax/verify_apk.py`: standalone structural verifier for actual future APK artifacts, with Android binary XML root checks, libxposed Java entrypoint/single-scope checks, arm64 ELF presence/type, DEX headers/signatures/checksums, resolved class definitions and smoke-vs-integrated BF linkage expectations.
4. `tests/test_xax_artifact.py`: synthetically generated *non-installable* DEX/ZIP corruption fixtures. Verifies metadata, scope, missing classes, checksum, duplicate descriptor and wrong-revision failures; reports structural checks without claiming runtime success.
5. Added [XAX_SMOKE_BUILD.md](docs/XAX_SMOKE_BUILD.md), updated XAX Android integration, language-boundary and testing notes, build orchestration and README.

## Actual test evidence

| Check | Command | Result |
| --- | --- | --- |
| All project tests | `./scripts/build_fresh.sh` | **PASS: 32/32** Python unittest methods; exit 0 |
| BF AOT class provenance | `python3 -m scripts.verify_linkage` (part of full build) | **PASS: 9/9** source-backed classes in optimized and unoptimized JVM jars |
| Reproducible JVM build | `python3 -m toolchain.brainfuck.build` (part of full build) | **PASS**, unchanged output digest from Iteration 2 |
| XAX absence gate | `python3 -m toolchain.xax.smoke_build --xax-source /mnt/data/does-not-exist --local-research-only` | **Expected rejection** `XAX_BLOCKED`; exit 2 |
| Non-APK rejection | `python3 -m toolchain.xax.verify_apk generated/brainfuck-policies.jar --mode smoke` | **Expected rejection** `MISSING_MANIFEST`; exit 2 |
| Real XAX compiler/imports/store build | External pinned compiler unavailable | **NOT RUN** |
| Real APK/DEX generation and signing | Android compiler/device unavailable | **NOT RUN** |
| YouTube ad suppression and SponsorBlock on Android | No module or runtime hooks | **NOT RUN** |

See separately shipped `YouTubeHideAds_iteration3_full_build.log`, `YouTubeHideAds_iteration3_missing_xax_probe.log` and `YouTubeHideAds_iteration3_nonapk_rejection.log` for raw outputs.

Source-equivalent JVM JAR SHA-256: `6d633b4cb42fbd9d400269baa9ce7422db41b29bd8f8f82144f4db369b3e75c0` (unoptimized); optimized JAR SHA-256: `7b1bf926184abf380f92030a3b2e8cb492bb969cf2b1f67477447073d1e37a92`.

## Current blockers, not hidden by new tests

The container has **no** XAX checkout/compiler, Android SDK, D8, ADB or rooted Vector device; the terminal cannot resolve GitHub hosts. The pinned upstream XAX GitHub repository lacks a confirmed redistribution license grant. Therefore **no canonical semantic store has been generated, no Android APK exists, and no libxposed or DexKit integration works yet**. The XAX adapter has not been exercised with actual external compiler modules; its API contract may need correction when available. Synthetic verifier fixtures and their positive tests do **not** establish that Android can install an APK or execute methods.

The forthcoming integration phase must execute the real pinned XAX toolchain locally, persist/verify its actual canonical store, build a signed controlled-target APK and observe loading on Vector. Only then proceed with BF class-to-DEX method linkage (not merely declared class names), XAX event ABI dispatcher, DexKit member resolution and actual YouTube advertisement/SponsorBlock hooking. The nine `.bf` policies remain genuine executable sources, but their high-level Boolean fixtures do not yet cover production YouTube semantics.

## Language and provenance

New project's runtime feature implementation remains Brainfuck-only; XAX will own typed Android host operations when available. Python scripts are off-device compiler/build/test tooling only. The external XAX source tree is never vendored. The new module package ID is `org.youtubehideads.module`; controlled smoke scope is `com.example.target`, distinctly separate from the eventual YouTube-only scope `com.google.android.youtube`. The smoke activity is an upstream compiler test fixture and is never claimed as the finished independent manager UI.
