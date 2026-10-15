# YouTubeHideAds — Iteration 10: isolated module loader and XAX exception-query scaffolding

Date: 2026-10-15. This is **not** an installable Android module.

## Implemented

1. **Real desktop JNI module-classloader isolation proof.** Extended the nonshipped `tests/jni` Java/C oracle to load the genuine compiled Brainfuck router using an explicit `URLClassLoader` with no application parent. The system classpath intentionally does not contain the BF router. Native `ClassLoader.loadClass`, JNI `GetStaticMethodID` and `CallStaticObjectMethodA` execute the real BF AOT output. C and Java are never packaged as Android application logic.
2. **Fail-closed class resolution.** Added tests covering all ten policies through the isolated loader; baseline and optimized Brainfuck JVM modes; all-zero and high-byte SponsorBlock endpoint transfer; missing loader, missing router, invalid method signature, and null input. Negative tests propagate JVM exceptions; there is no assumed success path.
3. **Two XAX-only bounded typed-call graphs (source authored, not built).** `toolchain/xax/loader_resolution.py` models `ClassLoader.loadClass(Ljava/lang/String;)Ljava/lang/Class;` via the pinned upstream JNI type, stack-argument, and effect APIs. The previous `make_xax_bound_router_call_graph()` now emits a separate JNI `ExceptionCheck` query after the static call and returns its pending-exception status. A successful graph construction is available only with the exact external XAX compiler checkout.
4. **Provenance and runtime gates.** The opt-in `toolchain.xax.check_router_graph` command now requires both semantic-call graphs to construct before writing its research-only report. Environment diagnostics continue to reject missing XAX toolchain, D8, Android SDK, API-102 framework, and unfinished JNI module class lookup/exception branch.

## Verified build result

`python3 -m unittest discover -s tests -v` completed: **85/85 tests PASS** (Iteration 9: 75/75). The complete source/JAR integrity check and build/audit scripts passed independently. Baseline and optimized Brainfuck policy/router JAR hashes are unchanged from Iteration 9. No XAX checkout, D8, Android SDK, ADB, or compatible device was available; Android integration preflight reports `BLOCKED`. See `YouTubeHideAds_iteration10_full_build.log` and `generated/language_audit.json`.

## Verified boundaries

- Genuine Brainfuck `dispatch_all.run([B)[B` reached over native JNI with and without an isolated module classloader: **verified only on desktop JDK**.
- All ten BF policies retain their original source and compiled behavior; the build still verifies both AOT configurations.
- XAX `ClassLoader.loadClass` semantic graph and XAX BF static-call graph: **authored, not constructed or lowered here**.
- `ExceptionCheck` source node/query is present; the **exception-dependent branch** and loader-qualified class token validation are still missing. No successful Android dispatch is claimed.
- Canonical XAX graph/store verification, real XAX DEX linking, device ART, libxposed module lifecycle, DexKit hooks, ad removal and SponsorBlock playback: **unexecuted**.

## Remaining critical sequence

1. Obtain the pinned external XAX compiler and satisfy the upstream redistribution/license requirements. Construct and typecheck both graphs; fix any verifier failures against the actual toolchain instead of assuming that source-level plans compile.
2. Create a real XAX-owned module-loader acquisition and class-name string, resolve the router class from it and validate classloader provenance, check the static method ID, and branch on JNI exceptions without clearing unexpected exceptions or leaking local owners.
3. Link the Brainfuck DEX and XAX module so a managed libxposed callback can safely invoke the BF policy router. Run ART and Vector/API-102 device smoke tests and collect evidence.
4. Only then implement and test real DexKit member discovery, YouTube hooks, and SponsorBlock API/player behavior. Keep unverified seek actions disabled.

The per-iteration full build log and archive manifest are distributed alongside this report. No test harness is bundled as application feature logic.
