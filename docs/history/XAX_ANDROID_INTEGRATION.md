# XAX Android backend integration: verified research, blocked project integration

**2026-10-16 execution update:** the clean pinned checkout at `build/xax-pinned`
now builds the lifecycle smoke APK and canonical stores. Vector 2.2 loaded
that module into `com.example.target`; heap inspection confirmed one instance.
A separate canonical XAX managed graph calls compiled BF directly and passed
4,463 ART comparisons after D8 conversion. This managed route uses ART member
resolution and needs no JNI resolver. Neither test connects a YouTube hook to
the BF call. See `history/ITERATION17_REPORT.md`; absent-compiler and no-device claims
in the earlier research below are superseded.

Pinned research SHA: `9e44eedfc241d25bb5062b38af105f75234000e2` of [MrxSiN/XAX](https://github.com/MrxSiN/XAX). We inspected `XAX_SPEC.md`, `docs/09_AI_PROTOCOL.md`, `compiler/src/xax_libxposed.py`, `compiler/src/xax_construct.py`, `compiler/integration/android/README.md`, and `SURFACE_ACTIVITY.md` at that revision.

Verified upstream declarations (NOT locally run): XAX defines canonical graph objects/transactions, direct Android DEX and APK build paths, and modern libxposed metadata for API 102. `xax_libxposed.py` documents mandatory Java module entrypoint and `java_init.list` for Vector v2.2; a native-only module without a Java entry is ignored. The Android surface profile can generate a minimal SurfaceView Activity but does not provide a generic composed Android application. XAX calls itself a research prototype. `xax_construct-v1` explicitly lists `linux-x86_64`, `linux-aarch64`, `windows-x86_64` and `jvm` as its construction-platform set, **not Android**.

The XAX compiler is not on this host and the host cannot resolve GitHub git archives via its terminal. No verified semantic transaction, canonical XAX store, Android lowering, JNI bridge, libxposed runtime or APK exists in this project. Adding fake `.xax` text or handwritten Java entrypoint as a workaround would violate the specification. A genuine integration requires fetching the licensed pinned compiler externally in an Android-capable environment and constructing/verifying actual semantic state through its supported API.

Intended Android target `com.google.android.youtube`, manager application ID `org.youtubehideads.module`, modern Xposed API target 102; actual minSdk/targetSdk and ABI must be frozen after a complete build. Android 28 is only a provisional floor from one upstream DEX-039 carrier profile, not a validated support claim.

**Precise integration gate:** prove generated Brainfuck JVM classes can be converted/linked to XAX-issued DEX without handwritten feature code; prove XAX emits a libxposed lifecycle entry able to call those classes and pass through validated ABI events; prove Vector loads it; only then attempt YouTube-specific DexKit resolution. All four gates are NOT RUN.

## Iteration 2: verified blockers and safe preparation

The pinned XAX GitHub repository's REST metadata currently gives `license: null`; a `LICENSE` lookup returned HTTP 404, and the pinned root directory listing did not supply a license grant. **This does not establish redistribution rights**. No upstream XAX code was vendored here. The correct answer remains to request/verify explicit terms before bundling or adapting upstream compiler/runtime assets. The newly authored project source is GPL-3.0-or-later, independently licensed.

`python3 -m scripts.probe_android_integration` is a reproducible **preflight diagnostic**, not a host builder. It reports whether the exact pinned XAX git revision and modules, Android SDK, D8 and ADB are locally visible. It deliberately includes unresolved license, absent canonical host and unexecuted Vector tests, even when tools are present. `--require-ready` returns nonzero until the integration requirements are actually satisfied.

`contracts/bf_host_v1.md` and `testdata/bf_abi_v1_vectors.json` now specify/test a binary protocol that a canonical XAX host can implement. `tests/test_host_link.py` executes the real generated JVM classes through the ABI test oracle and verifies source/JAR identity. **Those facts prove neither DEX composition nor XAX Android artifact lowering**; the pinned compiler's own Android carrier documentation still limits what can be inferred.

Explicit next integration deliverable: use a licensed, pinned XAX compiler to create a verified canonical semantic-program store with a genuine managed libxposed entry and typed host operations. Verify a signed APK on Vector v2.2 against controlled non-YouTube target fixtures **before** YouTube hooks. No handwritten textual `.xax` or Java/Kotlin/C/Python Android fallback is permitted.

## Iteration 3 — external semantic build adapter, not compiled yet

See [XAX_SMOKE_BUILD.md](XAX_SMOKE_BUILD.md) for the new XAX semantic-construction toolchain adapter, pinned upstream API provenance, strict controlled-target smoke scope, reproducible external-build entrypoint and the independent APK/DEX structural verifier. The XAX checkout and Android toolchain are still missing locally, so no canonical store was actually constructed and no APK generated in this environment.


## Iteration 4 — separate D8 conversion and package composition preparation

A host-neutral D8 subprocess adapter, checked JVM-policy-JAR input, DEX method/code-item inspector and unsigned APK multidex packager are added under `toolchain/xax`. See [DEX_LINKAGE.md](DEX_LINKAGE.md). They are *not* canonical XAX Android-host semantic programs, and they do *not* enable a XAX host to call Brainfuck. The external XAX compiler and D8 are absent locally; there is no Android verification evidence.

## Iteration 7 — XAX-managed binary transport carrier (not yet compiler-run)

The canonical smoke builder includes an independent `BinaryTransport.roundTrip([B)[B`
DEX managed-method carrier and a native XAX graph returning the same borrowed
input reference. This directly follows the pinned Android managed-class
forwarding API (ADR-199) and is constrained to the controlled target. The
independent parser now has `transport_smoke` mode that enforces the class and
nonempty forwarding method body. Synthetic-fixture tests validate this gate,
but the actual pinned compiler, generated DEX, APK and ART/JNI execution remain
NOT RUN on this host. The project still has no XAX host dispatch to Brainfuck.
