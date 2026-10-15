# YouTubeHideAds — Iteration 7 report (2026-10-15)

## Starting point and outcome

Continued from Iteration 6 (`ad4712e`) in the same greenfield Git repository. The preceding ten Brainfuck policy programs, source-attested JVM JARs, ABI framing, SponsorBlock decision chain and D8 preparation remain intact.

**59 / 59 automated tests PASSED** using `./scripts/build_fresh.sh` on this Linux container with Python 3.13 and installed JDK. See `YouTubeHideAds_iteration7_full_build.log`. The preflight still lists external XAX, Android SDK, D8 and ADB as absent. The pinned compiler and Android/device tests were **not run**; the project is **not** an installable Xposed module and does **not** remove YouTube advertisements.

## New implementation

1. `toolchain/xax/managed_transport.py` defines a frozen binary JNI transport contract: `BinaryTransport.roundTrip([B)[B`, managed with *real upstream XAX* `AndroidManagedClass`/`AndroidManagedMethod` semantics and `GraphBuilder`. The XAX native graph returns the **borrowed input reference itself**, with no feature logic or hidden copy. JNI symbol and signature are derived/checked by pinned XAX platform APIs at build time, if that compiler becomes available.
2. `toolchain/xax/smoke_build.py` includes the transport carrier, its XAX function and JNI export in the same canonical semantic module/store as the controlled-target lifecycle smoke. The evidence file includes carrier and function content IDs and explicit unexecuted/runtime false flags.
3. `toolchain/xax/verify_apk.py` adds `transport_smoke` mode: requires the correct transport class and a defined nonempty `roundTrip([B)[B` method body in an actual DEX method table. This does **not** verify DEX bytecodes or JNI execution.
4. `tests/test_managed_transport.py` adds five offline contract and corruption tests, taking the total to 59. It expressly rejects interpreting this smoke as a working YouTube module.
5. `scripts/build_xax_smoke.sh` now invokes the stronger transport gate. `.github/workflows/xax-transport-research.yml` is a **manual**, optional GitHub Actions research workflow to attempt an exact-pinned XAX checkout and real unsigned structural build on a networked runner. It does not redistribute XAX or generated APKs and **has not been run**.
6. Updated `README.md`, `docs/XAX_ANDROID_INTEGRATION.md` and `docs/XAX_SMOKE_BUILD.md` to distinguish a JNI transport carrier from an actual compiled-Brainfuck dispatcher.

## Verification and integrity

- Python unittest suite: **59/59 passed**. Synthetic fixtures are intentionally *not* installable APKs.
- Ahead-of-time compiled Brainfuck JAR: unchanged ten source-authored policies; both optimization modes rebuilt reproducibly.
- All host framing/source integrity tests inherited from Iteration 6 pass.
- `git diff --check` and Python syntax validation pass before archive generation.
- Exact `XAX` upstream source revision targeted: `9e44eedfc241d25bb5062b38af105f75234000e2`. No third-party XAX content is vendored or redistributed. Its redistribution permission remains unresolved.

## Outstanding engineering work

1. Execute `./scripts/build_xax_smoke.sh` with an externally obtained, pinned, permitted XAX compiler. Resolve API/graph lowering errors if any; inspect genuinely emitted DEX, libxposed metadata and JNI ELF exports.
2. On a controlled Android device, call `BinaryTransport.roundTrip([B)[B` with several binary arrays and verify byte identity and native library loading. No such execution occurred here.
3. Replace identity transport with a **typed XAX callback into the actual source-attested `org.youtubehideads.bf.*.run([B)[B` method**, then enforce BFH1/BFR1 validation, generation safety and per-feature action capability limits in the XAX host.
4. Add a real module startup and hook lifecycle, DexKit structural member discovery, active YouTube ad and SponsorBlock tests, settings, licensing review and release signing.

**Do not confuse structural transport with runtime dispatch**: no emitted XAX function currently calls Brainfuck and no YouTube hook exists.
