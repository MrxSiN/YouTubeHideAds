# Iteration 3 — XAX semantic lifecycle smoke-builder

## Exact scope

`toolchain/xax/smoke_build.py` is a **project-authored build-tool adapter**, not an Android runtime. It invokes XAX constructors from an **external pinned checkout** of `MrxSiN/XAX` at `9e44eedfc241d25bb5062b38af105f75234000e2`. It constructs actual typed semantic graph fragments for **two no-op JNI lifecycle callbacks**, libxposed API-102 module metadata, an Android manifest carrier and a build request. It calls the external `resolve_packages`, `snapshot_store`, `write_store`, `verify_store` and `build` interfaces. The produced store (if the real compiler successfully runs) is binary canonical XAX semantic state, **not** a `.xax` text file or JSON alternative.

The smoke builder uses the external compiler's `benchmarks.bench_android_managed_bridge.ui_activity_fixture` as an independent *testing-only* Activity fixture. That fixture is **not** the proposed YouTubeHideAds manager or runtime source. The lifecycle callbacks are no-op: no DexKit, no preference access, no Brainfuck dispatch, and no YouTube API hooks. Scoped exclusively to `com.example.target`; the module's distinct package ID is `org.youtubehideads.module`. It must not be shipped as YouTubeHideAds.

This integration is grounded in pinned XAX sources:

- `compiler/benchmarks/bench_android_libxposed_managed.py`: JNI callback semantic graphs, imports, export symbols, package objects, reproducible build request.
- `compiler/src/xax_libxposed.py`: `LibxposedManagedEntryDescription`, `LibxposedModuleDescription` and carrier semantics.
- `compiler/src/xax_build.py`: `resolve_packages`, `snapshot_store` and `build` request APIs.
- `compiler/src/xax_compiler.py`: canonical store `write_store`/`verify_store` primitives.
- `compiler/integration/android/vector/README.md`: external Android/Vector runtime oracle expectations.

The host **cannot install/clone** this pinned compiler in the current environment: GitHub network resolution is unavailable to the container and no XAX checkout is supplied. Therefore the actual XAX API imports, semantic construction, store verification and APK generation in this project are currently **NOT RUN**, despite the adapter being written. Unit tests prove only local argument-gating and artifact-inspector behavior, not this code's integration with the compiler.

## Local, private research command

First obtain a legally usable external XAX checkout at the exact revision. Then:

```sh
XAX_SOURCE_DIR=/absolute/path/to/external/XAX ./scripts/build_xax_smoke.sh
```

When this external toolchain executes, output paths under ignored `build/xax-lifecycle-smoke/` include the actual `lifecycle-smoke.canonical-store`, `lifecycle-smoke-unsigned.apk` and JSON evidence. Only a **real run** may claim those exist. The builder always reports `signed=false`, `device_tested=false`, `brainfuck_dex_linked=false` and `youtube_hooks=false`. Redistribution of XAX-derived artifacts remains gated on an upstream license grant; GitHub `license=null` and no LICENSE file were observed at the pinned revision. This script is for local research, not release distribution.

## Artifact verifier, `toolchain/xax/verify_apk.py`

Runs independently of XAX on synthetically corrupt fixtures. Validates:

- APK ZIP sanity, unique and safe entry names, binary-XML root header;
- modern libxposed `java_init.list` entrypoint, `module.prop`, and a **single** matching scope (controlled smoke or YouTube integration);
- presence and ELF class/architecture of arm64 JNI library;
- DEX 035/037/038/039/040/041 magic, header size, endian, file size, SHA-1 signature and Adler-32 checksum;
- DEX class definitions via `string_ids`, `type_ids` and `class_defs` rather than naive raw string search;
- `smoke`: no BF class claims, with controlled target only;
- `integrated`: all current BF class descriptors (ten in Iteration 6) plus the XAX managed entry, YouTube scope only.

This is a **bounded structural gate**. It does **not** check DEX verifier correctness, class method implementations, JNI export table, Android binary XML resource bindings, actual compiler provenance, AOT class-byte equivalence after D8, libxposed hook behavior, root permissions, app stability, signing or device functionality. Unit-test DEX and APK binaries are deliberately skeletal fixtures and **not installable APKs**. Passing the verifier cannot establish that Brainfuck was linked correctly or that a module works. The authoritative JVM class integrity verifier remains separate until real DEX linkage exists.

## Remaining blocking milestones

1. Obtain the licensed and pinned XAX compiler and execute the semantic smoke-builder; correct any verified API differences.
2. Replace the testing Activity with a new XAX-authored manager and actual libxposed lifecycle host.
3. Build a real typed XAX-to-compiled-BF `run([B)[B` bridge. A class descriptor without callable linkage does not suffice.
4. Establish conversion/composition into real DEX; verify each generated method and its ABI, not merely descriptors.
5. Integrate and verify DexKit adapters, verified YouTube hooks and playback test oracles on a compatible rooted Android device.
6. Resolve XAX redistribution conditions and sign/release only after real device evidence.


## Iteration 4 addendum

The structural verifier now inspects DEX method tables and requires each policy class to have a nonempty `run([B)[B` code item when the mode is `integrated` or `linked_smoke`, rather than accepting descriptors alone. It still does not verify method instructions. A separate D8 compiler subprocess adapter and unsigned APK multidex composer were added, unit-tested using deliberately noninstallable code-item fixtures and a fake-D8 subprocess (not real Android D8). See [DEX_LINKAGE.md](DEX_LINKAGE.md). The XAX-to-BF call bridge is still absent.

## Iteration 6 scope reminder

The new tenth Brainfuck class and source-level SponsorBlock category selection are **not** invoked by the XAX lifecycle smoke builder. The smoke builder still emits no-op XAX lifecycle callbacks for a controlled test package and no YouTube hook. A source-attested policy class definition or D8 link does not establish a host invocation call path.

## Iteration 7 — canonical JNI byte-array transport construction (UNEXECUTED)

`toolchain/xax/managed_transport.py` now builds one additional *real XAX semantic*
Android managed carrier (no handwritten Java/Kotlin) using the pinned upstream
`AndroidManagedClass`, `AndroidManagedMethod` and `GraphBuilder` interfaces:

- Managed type: `Lorg/youtubehideads/bridge/BinaryTransport;`
- Forwarded method: `roundTrip([B)[B`
- Native JNI symbol: generated via `jni_short_native_symbol` (not guessed by name)
- XAX function: returns its borrowed JNI `byte[]` input *unchanged*. No new
  Java object, array allocation, policy decision, networking, reflection, or
  interpreter is introduced. JNI borrowed references belong to the caller.
- `check_export_signature` is run on the constructed canonical type graph by
  the **actual pinned XAX compiler** when available; a mismatch aborts build.
- XAX emits a normal managed DEX forwarder, required to have a nonempty code
  item in APK mode `transport_smoke`, with exact `roundTrip([B)[B` signature.
- The managed transport carrier joins the same package/store as the XAX
  lifecycle smoke module. It is **not invoked by libxposed callbacks** and it
  does **not** call any compiled Brainfuck policy.

`./scripts/build_xax_smoke.sh` now uses the stricter `transport_smoke` verifier.
The separate external-only workflow `.github/workflows/xax-transport-research.yml`
can be manually dispatched in a capable GitHub Actions environment to clone
exact pinned XAX into an ephemeral checkout, run the canonical constructor and
assert the emitted transport method exists. It explicitly does **not** upload
any XAX-derived artifact; upstream redistribution license remains unresolved.
This workflow has **NOT BEEN RUN** in the current session.

**Evidence on this machine:** only Python synthetic DEX/APK structural tests;
no pinned XAX sources were available to construct graph/store/APK and no device
was available to exercise the JNI array round trip. Passing a synthetic DEX
method check does not validate the contents of its instructions, link JNI
exports, prove class-loading behavior, or establish a XAX-to-Brainfuck call.
The next real step is to invoke the Java `roundTrip` method in a controlled
Android test with known binary inputs, then replace the identity graph with an
XAX graph invoking a source-attested Brainfuck `run([B)[B` target and proving
the returned bytes, generation and feature action at the host boundary.
