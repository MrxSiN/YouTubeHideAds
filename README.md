# YouTubeHideAds — greenfield Brainfuck-first project

**Current module (2026-10-16):** a launcherless libxposed API-102 module now
loads inside YouTube and adds **YouTubeHideAds** to the native Settings toolbar.
It opens its page inside YouTube; no companion Activity or manager app exists.
The XAX callbacks and real BF router executed in YouTube 21.41.525 on the
Pixel 8 Pro / Android 17 / Vector 2.2. Three page open/close cycles, Android
Back, duplicate-entry prevention and process survival passed.

APK: `build/module/YouTubeHideAds-debug.apk` (version code 21, local debug key).
It is installed and enabled for YouTube on the test phone. **Ad suppression
and SponsorBlock are still not connected.** See [module report](docs/history/ITERATION18_REPORT.md).
The older integration reports below are historical.

**Previous integration (2026-10-16):** a real canonical XAX graph now calls the
Brainfuck router through a typed managed `invokestatic`. Its XAX/JVM → D8 → ART
path passed **4,463 reference comparisons**, invalid-input and recovery checks
on the Pixel 8 Pro without a native lookup bridge. A separately built XAX
lifecycle smoke module loaded successfully through **Vector 2.2 / API 102**
in a controlled test app; heap inspection found one module instance. Both test
apps were removed afterward. See [the current report](docs/history/ITERATION17_REPORT.md).

**Still incomplete:** the raw managed call and Vector lifecycle are separate
proofs. No YouTube hook calls Brainfuck, and the on-device validated host ABI,
DexKit resolver, settings, live SponsorBlock and ad removal remain unimplemented.
The APK under `build/xax-vector-smoke/` is a test-signed lifecycle fixture,
not a usable ad-removal module. Older iteration statements below are historical.

**Update (2026-10-16):** the optional [BrainfuckC adapter](docs/BRAINFUCKC_ANDROID.md)
compiled all twelve policies using `D:\GitHub\brainfuckC`. A Pixel 8 Pro
(Android 17 / API 37) passed **4,463 native/reference comparisons** through ADB.
This verifies callable native code in Android shell; XAX host integration,
JNI, Xposed hooks and actual YouTube ad removal remain unverified. See
[device evidence](evidence/brainfuckc_20261016/device-result.json).

The iteration notes below describe the earlier JVM/XAX milestones.

**State (2026-10-15), Iteration 15: twelve source-owned Brainfuck policies and a twelve-way AOT router; verified desktop JNI execution through both ordinary and isolated module classloaders, five uncompiled XAX JNI/safety graph sources (including direct-call composition) with explicit exception-status queries, host-wire ABI, and synthetic D8/APK gates. XAX compilation and Android runtime remain NOT EXECUTED; NOT an installable Xposed module.** This new Git repository was initialized empty. It is not a fork, migration, conversion, or clone of YouTubeMalbolge. No YouTube ad-removal or SponsorBlock behavior has yet been exercised inside Android.

The checked-in `.bf` programs are genuine executable Brainfuck with meaningful binary-input-dependent policy computations. The on-device intended architecture is Brainfuck decisions + XAX semantic-graph Android host; the **runtime** host, hooks, DexKit binding, and working APK are **not yet implemented**. A plain JVM class file is not proof of an Android DEX build or Xposed integration.

## What currently runs

- Annotation-aware strict Brainfuck parser, source mapping and SHA-256 of executable commands only.
- 8-bit wrapping Brainfuck reference interpreter with 4096-byte tape, pointer checks, zero-at-EOF, 100,000-op default fuel budget (explicitly 2,000,000 for the 64-bit timestamp policy and its inline router) and 64-byte output limit.
- Direct AOT JVM class emitter, with optimized and unoptimized modes. It does not generate Java source or run an interpreter at runtime.
- Twelve `.bf` feature-decision programs: player slot, feed, search, Shorts, Premium promotion, paid product shelf, empty-container cleanup, resolver rejection, and four **partial** SponsorBlock policies (eight-category selection, eligibility/64-bit endpoint selection, a single-call Brainfuck-owned SponsorBlock category-plus-seek gate, and a genuine 63-bit signed-domain timestamp-window comparator).
- Exhaustive binary-policy truth tables, comment invariance, executable source mutation, reference/JVM differential tests, and **framed ABI/JVM link tests** with stale-generation and invalid-action rejection. Test harness Java lives only under `tests/`; it is not application code.

### Commands

Requirements: Python 3.11+ and JDK 21 (the compiler emits major-version-49 class files). No pip dependencies are required.

```sh
cd YouTubeHideAds
./scripts/build_fresh.sh
PYTHONPATH=. python3 -m unittest discover -s tests -v
PYTHONPATH=. python3 -m toolchain.brainfuck.build --out generated
PYTHONPATH=. python3 -m toolchain.brainfuck.build --out generated-optimized --optimize
PYTHONPATH=. python3 -m toolchain.brainfuck.router --out generated
PYTHONPATH=. python3 -m toolchain.brainfuck.router --out generated-optimized --optimize
PYTHONPATH=. python3 -m toolchain.brainfuck.cli validate source/brainfuck/ads/player/suppress_video_slot.bf
PYTHONPATH=. python3 -m toolchain.brainfuck.cli interpret source/brainfuck/ads/player/suppress_video_slot.bf --input-hex 01010100
PYTHONPATH=. python3 -m scripts.verify_linkage
PYTHONPATH=. python3 -m scripts.probe_android_integration
# Research-only next stage if licensed pinned XAX and D8 are installed:
# XAX_SOURCE_DIR=... D8_BIN=... ./scripts/link_xax_smoke.sh
```

A stable `BFH1` request / `BFR1` reply contract with strict v1 framing is documented at [`contracts/bf_host_v1.md`](contracts/bf_host_v1.md); golden byte vectors are in `testdata/`. It is implemented as a **host-neutral OFF-DEVICE conformance test oracle**, not a canonical XAX host. Direct AOT JVM classes run through that oracle in both compiler modes. Invalid inputs, stale generations, spoofed SponsorBlock endpoints, and live seek requests fail closed. `authorize_seek.bf` now emits the complete little-endian 64-bit endpoint without platform feature code, but it still relies on validated segment-window evidence and cannot execute seeks until a verified XAX host exists.

A project-authored **XAX semantic build adapter** now exists at `toolchain/xax/smoke_build.py`, targeting a controlled libxposed lifecycle smoke test, plus a synthetic-test-verified APK/DEX gate at `toolchain/xax/verify_apk.py`. The adapter has **not run against the absent pinned external XAX compiler**. It cannot yet establish a running XAX caller for BF policies. A new **D8-based BF-DEX packaging adapter** (`toolchain/xax/link_d8.py`) can append a verified BF JAR's D8-generated classes into the XAX controlled-target smoke APK and structurally inspect actual `run([B)[B` code items, but **neither D8 nor the external XAX build has executed locally**. Synthetic package tests do not establish working Android behavior. See [DEX linkage](docs/DEX_LINKAGE.md) and [`docs/XAX_SMOKE_BUILD.md`](docs/XAX_SMOKE_BUILD.md).

The `generated/brainfuck-policies.jar` is a **JVM artifact**, not an Android APK. No Gradle tasks are advertised because the canonical XAX Android build and artifact composition have not yet been established for this project.

## Iteration 6 proof scope

`authorize_seek.bf` now consumes 6 Boolean input bytes and an 8-byte little-endian segment end (1..2^63−1 ms). It emits `00` or `04` + the eight bytes. The off-device codec checks the actual output against the request and generation and refuses all attempted runtime seeks because no Android XAX host exists. It does **not** yet derive window membership from raw timestamps, merge segments or fetch the SponsorBlock API. `select_sponsor_category.bf` now consumes 16 interleaved Boolean bytes (eight category-enable flags plus a one-hot category selection) and produces `00` (PASS) or `05` (CATEGORY_AUTO_SKIP). The source itself selects the active category; the generic ABI only checks the Boolean/one-hot encoding. Both real JVM compiler modes agree with reference Brainfuck on all 2,048 valid settings/selection combinations. The offline two-program chain checks that `authorize_seek` uses the preceding category action from the **same generation** rather than a host-computed category permission. No XAX/Android dispatcher exists, so this remains test-only. Read `docs/history/ITERATION6_REPORT.md` and run `./scripts/build_fresh.sh`.

## Proposed Android integration

- Module ID: `org.youtubehideads.module` (reserved; not shipped).
- Target application only: `com.google.android.youtube`.
- Minimum API provisionally 28 for the relevant XAX DEX 039 profile; finalize when the actual app is built and tested.
- Modern libxposed API 102 through the pinned, verified XAX semantic-graph pathway only, when feasible.
- DexKit used for bounded structural resolution; ambiguous evidence disables the feature.
- No handwritten Java/Kotlin/C/Python fallback feature implementation and no Malbolge dependency.

See [the integration blocker](docs/XAX_ANDROID_INTEGRATION.md), [language-boundary audit](docs/LANGUAGE_BOUNDARY.md), [test evidence](docs/TESTING.md), and [feature matrix](docs/FEATURE_COVERAGE.md). Do not install or describe this repository as a functioning ad-removal module yet.

## Licensing

The **newly authored** files in this repository are provided under GPL-3.0-or-later (see `LICENSE`). Morphe is a behavior reference only; this repository contains no copied Morphe source. XAX has not been vendored or redistributed; the pinned GitHub repository has no recorded license grant (`license: null`), so redistribution remains blocked until explicit terms are established. External links and separate copyright are recorded in `docs/UPSTREAM_PROVENANCE.md`.

## Iteration 7: controlled managed byte-array transport (pre-runtime)

The smoke builder now **authors one XAX semantic JNI transport graph** for a
DEX-visible `BinaryTransport.roundTrip([B)[B` method. It returns the borrowed
input array unchanged. The corresponding `transport_smoke` APK gate checks the
forwarded DEX method's existence, not its runtime behavior. Both the build
through external XAX and a device oracle remain unexecuted here; Brainfuck
classes are still **not invoked by any XAX hook**. See
[`docs/XAX_SMOKE_BUILD.md`](docs/XAX_SMOKE_BUILD.md) and the optional manual
GitHub Actions workflow `xax-transport-research.yml`. No APK is releasable.

## Iteration 8: one genuine Brainfuck callable method

The deterministic build now constructs `generated/router.bf` by inserting all ten original Brainfuck command streams verbatim inside an **executable BF selector program**; there is no Python/Java feature switch at runtime. Its source-verified AOT class is `org.youtubehideads.bf.dispatch_all.run([B)[B`. A one-byte selector identifies the BF program and the remaining raw bytes are its input. Both optimized and unoptimized JVM modes run successfully and match the original ten programs across exhaustive input combinations. Unsupported selectors produce an empty output, which the host must reject. The full test suite passes **68/68**. See `docs/history/ITERATION8_REPORT.md` and `docs/BRAINFUCK_ROUTER.md`.

The optional D8 adapter can now structurally link **11** BF classes (ten policies + router) in an unsigned, controlled-target smoke APK if external XAX and D8 exist; the actual external build has not run. The current XAX `BinaryTransport` is still an identity echo; it is **not** wired to the BF router. There are no device results, YouTube hooks, live SponsorBlock operations or installable APKs.

## Iteration 9: actual JNI call proof on desktop, XAX graph research

The test-only `tests/jni/` harness now invokes `dispatch_all.run([B)[B` through real JDK JNI operations (`FindClass`, `GetStaticMethodID`, `CallStaticObjectMethodA`) in both AOT JVM modes. This is not a C-language application fallback: those files are tests only, excluded from the Brainfuck JAR and every Android package. A *pre-resolved* static-call XAX semantic graph is authored in `toolchain/xax/router_call_plan.py`, but cannot be compiled against the absent pinned XAX toolchain; classloader resolution and Android callback export are not implemented. The full suite now passes **75/75 tests**; the integration remains research-only. See `docs/history/ITERATION9_REPORT.md` and `docs/JNI_ROUTER_BOUNDARY.md`.

## Iteration 10 — isolated classloader JNI and typed XAX loader call source

The desktop JNI oracle now deliberately removes the BF router from the system
classpath and invokes the genuine Brainfuck router via a Java `ClassLoader`
object passed through JNI. This detects the failure mode where `FindClass`
cannot see a module-defined class. Every policy is tested in both AOT modes;
null input, absent loader, missing class, and a mismatched Java method signature
are all rejected without a success action. These Java/C files reside only in
`tests/` and are not application code.

Added `toolchain/xax/loader_resolution.py` containing upstream-XAX-dependent
`ClassLoader.loadClass` typed plan and bounded semantic call graph. The existing
pre-resolved Brainfuck invocation graph now queries JNI `ExceptionCheck` and
returns the status to a future checked caller; it still does **not** branch or
act on this status. Both graph sources require an external, pinned XAX
checkout before construction/type validation can be claimed. No ART build,
libxposed attachment, DexKit hook, signed APK or YouTube ad removal has run.
See `docs/history/ITERATION10_REPORT.md` and `docs/JNI_ROUTER_BOUNDARY.md`.

## Iteration 11 — checked JNI loader identity and XAX store-verifier gate

An off-device JNI oracle now validates the exact Brainfuck router **binary
class name and defining classloader object** before method lookup. The tests
reject parent delegation and spoofed `loadClass` overrides, and exercise
alternating failure/success cleanup using compiled BF output on the real JDK.
This is strictly `tests/jni` test-harness C/Java; neither language is used for
application features. All ten `.bf` policies and the router are unchanged.

A third XAX-only semantic graph source models typed `GetStaticMethodID`, and
the opt-in external research command now requires an actual XAX canonical
store (`write_store` + `verify_store`), refusing incomplete dependency closure.
The pinned XAX checkout is absent locally, so **none of these graphs have been
validated or executed by XAX**, and there is no XAX callback, Android APK,
DexKit hook, or real YouTube suppression. See `docs/history/ITERATION11_REPORT.md` and
[`docs/JNI_ROUTER_BOUNDARY.md`](docs/JNI_ROUTER_BOUNDARY.md).

## Iteration 12 — XAX dispatch safety gate (structural research only)

A fourth XAX semantic construction function, `make_xax_dispatch_guard_graph`,
expresses exception-dependent and provenance-dependent **conditional branches**
that deny dispatcher authorization unless all five caller-supplied integrity
statuses are exactly one. The semantic writer's input set is pruned to the
actual root-reachable XAX object closure, while missing references and CID
conflicts remain errors. Source-level reference tests and the repository's
Python/JVM/JNI suite cover these changes, but the XAX graph has **not** been
validated by the external pinned compiler, joined into an Android managed
callback, linked to DEX, or executed on a device. See `docs/history/ITERATION12_REPORT.md`.


## Iteration 13 — one-call Brainfuck SponsorBlock gate and large-router AOT

The new `source/brainfuck/sponsorblock/sponsor_skip_pipeline.bf` (`0x0403`)
consumes **29 raw bytes**: eight interleaved category enabled/one-hot selector
pairs (16 Booleans), five player/context predicate Booleans, and eight
little-endian endpoint bytes. The same executable Brainfuck invocation both
chooses category eligibility and gates/outputs the endpoint. There is **no
intermediate host-computed or host-replayed category authorization flag**.
This reduces the dependency on two separately authorized policy calls without
claiming that live video-window evidence is already calculated in Brainfuck.

An actual defect was caught during construction: a disabled final category
could leave selector scratch in cell 2, corrupting the subsequent Boolean
conjunction. The Brainfuck code now clears that cell before testing player
gates, and `tests/test_sponsor_pipeline.py` covers every one of the 2,048
category/settings combinations plus the final-category regression.

The eleven-branch inlined router exceeds the JVM 65,535-byte `Code` ceiling
with the original one-error-handler-per-instruction emission. The AOT backend
now uses region-local shared **fuel, pointer-bounds and output-limit** error
handlers for large streams; the checks still execute for each source command.
Both AOT modes run on the actual JVM, including the JNI test-only classloader
probe. Build-time tooling remains Python, not Android application feature code.

**No real XAX compiler, D8, libxposed runtime or Android device check was
performed.** The adapter's XAX classloader and exception-branch components
remain authored but not compiled or interconnected with the complete Android
caller. No APK and no YouTube ad removal are claimed. See
[`docs/history/ITERATION13_REPORT.md`](docs/history/ITERATION13_REPORT.md).

## Iteration 14: Brainfuck-owned timestamp-window proof (offline)

`source/brainfuck/sponsorblock/sponsor_time_window.bf` consumes 24 bytes: three signed-long-compatible, little-endian `start`, `current`, `end` millisecond timestamps. It computes `start <= current < end` **inside genuine Brainfuck** and emits `06` (`TIME_WINDOW_VALID`) or `00` (`PASS`), with no Android seek action. The off-device `checked_sponsor_time_chain` verifies that this Brainfuck result, its generation and the exact endpoint are transferred into the established one-call SponsorBlock category/seek policy. This does not attest the authenticity of a live player's timestamps or eliminate the XAX host's obligation to run both compiled programs.

The generic Brainfuck resource budget remains 100,000 commands; the timestamp policy explicitly declares a bounded 2,000,000-command limit because its worst-case 64-bit arithmetic can exceed the old default. Both direct JVM compilation modes and the 12-way inline router execute the new policy correctly. For long programs the compiler compresses safe monotonic pointer runs while preserving pointer-versus-fuel failure precedence and shares exception handlers within bounded regions. The current router remains close to the JVM 65,535-byte `Code` limit; broader arbitrary-sized callables require future method outlining or another verified backend.

**Verification:** 116/116 tests passed in two complete groups (67 + 49), with byte-exact source/JAR integrity checks and no Android execution. See `docs/history/ITERATION14_REPORT.md`.

## Iteration 15 — XAX direct-call composition of router and guard (uncompiled)

`toolchain/xax/checked_router_dispatch.py` now authors a **fifth XAX semantic
graph** that directly invokes the XAX JNI router subroutine, derives
`jni_exception_clear` from that call's actual `ExceptionCheck == 0` byte,
and directly invokes the XAX fail-closed dispatch guard with the derived value.
Its other four guard inputs are **not yet trusted runtime proofs**; the source
is still neither an exported Android callback nor an Android application.
The composed function preserves JNI reference-owner and effect results rather
than dropping resource tokens, and the external canonical-store probe now
requires real upstream verification of all five linked functions using a
`PROGRAM_ROOT` store. The external XAX/D8/Android toolchain is absent locally;
local tests cover only reference-guard semantics, source intent, and failure
of external-dependency checks. See `docs/history/ITERATION15_REPORT.md` and
`docs/JNI_ROUTER_BOUNDARY.md`.
