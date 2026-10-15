# YouTubeHideAds — Iteration 4 implementation and verification report

Date: 2026-10-15 (Asia/Kuala_Lumpur)
Baseline: Iteration 3 Git commit `48b80ce`.
Outcome: **42/42 local automated tests passing** with preserved Brainfuck source/JVM digests. **Not a functioning Xposed module, and not an Android APK build.**

## Actual changes

1. `toolchain/xax/dex_methods.py`: bounded, checked parser for DEX type/prototype/method/class-data/code-item tables. Requires independently named `run([B)[B` method bodies for every BF policy during linked structural verification. Validates offsets and indexes; **not an ART verifier**.
2. `toolchain/xax/link_d8.py`: external D8 command adapter accepting only nine source-attested AOT-generated Brainfuck class files, verifying byte identity against the real annotated `.bf` sources, invoking D8 with API 28, and validating resulting policy DEX class/method definitions and byte-level DEX integrity. Rejects missing/extra/duplicate policies, suspicious signatures, unknown compression and malformed package data. An unsigned APK ZIP composer appends policy classes without overwriting XAX host classes. Does **not** link XAX host call sites to BF implementations.
3. `toolchain/xax/verify_apk.py`: `linked_smoke` mode (controlled test target only), reinforced `integrated` mode with checks that required `run([B)[B` entries have nonempty code items. Existing `smoke` mode remains limited to a controlled XAX lifecycle build with no policies.
4. `scripts/link_xax_smoke.sh`: pinned-external-XAX + separately provided real D8 invocation path; intentionally build-only, unsigned and controlled-target-scoped.
5. `tests/test_dex_link.py`: 10 new tests with intentionally noninstallable synthetic DEX/APK and one fake-D8 subprocess (explicitly not D8). Includes source JAR verification, deterministic ZIP, code-item gate, failures on source drift, signatures, missing DEX, corrupted tables, unexpected classes and duplicate classes.
6. `docs/DEX_LINKAGE.md` plus README, XAX integration and testing documentation and Android environment blockers updated.

## Test evidence

Command: `PYTHONPATH=. python3 -m unittest discover -s tests -q`.
Observed: **Ran 42 tests; OK**. Command: `./scripts/build_fresh.sh`. Observed: **Ran 42 tests; OK**, both optimized/unoptimized BF JAR builds, source-verified byte-identical classes, language audit, and an explicit BLOCKED Android preflight. Full real execution stdout/stderr is in the provided `YouTubeHideAds_iteration4_full_build.log`.

| Test or component | Actually run? | Result |
|---|---|---|
| Annotated BF conformance, policies and JVM differential suites | Yes | Pass |
| Host-wire ABI and source integrity tests | Yes | Pass |
| DEX method inspection and synthetic composition tests | Yes | Pass |
| Fake-D8 subprocess orchestration test | Yes (mock only) | Pass |
| Actual Google Android D8 converter invocation | **No** | Unavailable |
| Real canonical XAX build/store creation | **No** | External pinned compiler unavailable |
| Real Android APK generation/signing | **No** | Unavailable |
| XAX-hosted runtime call into BF classes | **No** | Not yet implemented |
| DexKit discovery and libxposed YouTube hook execution | **No** | Not yet implemented |
| Vector/Android device, ad removal and SponsorBlock integration | **No** | Not run |

Upstream XAX pinned research SHA: `9e44eedfc241d25bb5062b38af105f75234000e2`. No XAX source or generated XAX binaries vendored here. Current repository metadata has no explicit license grant; redistribution of upstream-derived artifacts is not authorized by this project.

Nine authoritative BF/JVM classes preserved:

- Unoptimized SHA-256: `6d633b4cb42fbd9d400269baa9ce7422db41b29bd8f8f82144f4db369b3e75c0`
- Optimized SHA-256: `7b1bf926184abf380f92030a3b2e8cb492bb969cf2b1f67477447073d1e37a92`

## Important safety and scope note

Synthetic DEX bodies used by these unit tests contain a dummy `return-object` code item, not executable Brainfuck. The tests only validate the *packaging and parser* mechanics; they are not an Android runtime oracle. The authoring language of feature decisions remains Brainfuck, but actual Android application policy execution has **not** been established. A method definition in DEX is not evidence that libxposed hooks call it.

The linker produces an **unsigned, research-only controlled-target smoke package**, never a release YouTube module, and a raw ZIP recomposition is not a substitute for zipalign, APK signing, device installation or the ART verifier.

## Next exact engineering task

Obtain and execute the legally usable, pinned XAX semantic compiler in an Android-capable environment; build the canonical lifecycle smoke store/APK and run the real D8 command with source-verified BF classes. Only after actual APK and device evidence should work advance to a type-safe, bounded **XAX semantic host method caller**, then to a controlled libxposed hook with BF-invocation proof, followed by DexKit/YouTube discovery and real feature testing. Continue to fail closed where a platform capability has not been demonstrated.
