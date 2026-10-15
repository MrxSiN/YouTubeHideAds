# YouTubeHideAds — Iteration 11: defining-loader JNI guard and three-graph XAX store gate

Date: 2026-10-15. **Not an installable Android module. No real YouTube behavior has been verified.**

## Implementation

1. **Verified defining-loader desktop JNI path, in test harness only.** The `tests/jni/` probe obtains a router class from `ClassLoader.loadClass`, invokes `Class.getName` to require exactly `org.youtubehideads.bf.dispatch_all`, and checks `Class.getClassLoader` against the intended loader using JNI `IsSameObject`. It accepts only the exact `run([B)[B` static method and does not clear unrelated JNI exceptions. Local JNI references are released on error paths. These handwritten Java/C sources are strictly nonshipping test fixtures; application feature authority is still Brainfuck.
2. **Adversarial loader oracles.** A parent-delegating URLClassLoader is rejected with `ROUTER_LOADER_PROVENANCE_MISMATCH`; an overridden `loadClass` returning `java.lang.String` is rejected with `ROUTER_CLASS_NAME_MISMATCH`. Both BF compiler modes still execute valid policies; 80 alternating cycles of parent/misnamed/genuine resolution per mode test cleanup/exception survival, **not ART leak freedom**.
3. **Third real-XAX-API graph source.** `toolchain/xax/static_method_resolution.py` creates a typed `GetStaticMethodID` semantic subroutine whose *input* must be an already verified loader-qualified `jclass`, its live local owner, two preexisting C-string buffers and a JNI memory effect. It returns a typed method ID, owner and `ExceptionCheck` byte. It cannot yet guarantee non-null IDs, live string lifetimes or branch on exceptions; it does not claim to be a full Android callback.
4. **Fail-closed XAX canonical-store acceptance.** `toolchain/xax/store_evidence.py` rejects missing semantic reference dependencies and CID conflicts and calls upstream `write_store`, `StoreReader` and `verify_store` for all three authored graph functions. `toolchain/xax/check_router_graph.py --xax-source ... --store ... --out ...` emits success evidence only if the pinned external XAX compiler constructs the subroutines and verifies the store. A manually dispatched GitHub Actions research workflow includes this check but does **not** upload XAX artifacts.
5. **Expanded store-object closure.** The three graph source adapters now include JNI type-object closures and exact method-spec roots in their optional XAX object inventories to support future verification.

## Tests and reproducibility

- `python3 -m unittest discover -s tests -v`: **95/95 tests PASS** (Iteration 10: 85/85). Both captured full-suite runs passed; one took 30.263 s and the other 29.428 s.
- `python3 -m toolchain.brainfuck.build --out generated` and the optimized counterpart: ten policies reconstructed with unchanged SHA-256 hashes.
- `python3 -m toolchain.brainfuck.router --out generated` and the optimized counterpart: the BF-owned router reconstructed unchanged. The optimized build was also separately rerun successfully in 1.38 s.
- `python3 -m scripts.verify_linkage`: PASS for both compiled policy configurations and both routers.
- `python3 -m toolchain.brainfuck.audit`: PASS for the source-language boundary; correctly says XAX host is not implemented.
- Android preflight: `BLOCKED`; no SDK, D8, ADB, pinned external XAX checkout or on-device runtime.

Two *combined* `./scripts/build_fresh.sh` attempts exceeded the command execution limit after the full 95 passing tests and generation of the unoptimized router, without returning success; **do not describe them as successful combined builds**. The remaining stages were rerun individually and passed. See separate stage logs and `YouTubeHideAds_iteration11_verified_stages.log`.

## Boundaries and next critical work

The desktop JNI classloader checks prove **class binary name and defining-loader identity**, not code authenticity or Android runtime safety. The Android host must bind a trusted loader to source-attested DEX output; class name and loader equality alone do not establish the contents of a class.

The newly authored XAX subroutines are **not connected**: the loader graph yields a generic Class, while the static resolver requires a verified BF-class reference; the guarded refinement is missing. The class-name `String` and method/signature C strings have no XAX allocation/ownership graph. Method ID and result null checks, exception-dependent branching, memory ownership disposal and an actual managed libxposed callback remain incomplete.

The external pinned XAX compiler is not installed and could not be fetched from the command-line environment due to DNS restrictions. Therefore **no canonical XAX graph has been constructed or verified by the XAX compiler**, no Android DEX/JNI caller was generated, no APK was built, and no ART, DexKit, libxposed, SponsorBlock playback or YouTube ad removal was tested. The opt-in workflow has not been executed.

The next acceptable milestone is a real pinned-XAX canonical-store conformance run plus the verified `jclass` refinement and an exception-safe callback connecting to the BF router, followed by a controlled device test. Do not ship until those conditions hold.
