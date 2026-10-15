# XAX managed policy calls and Vector lifecycle evidence — 2026-10-16

The project advanced through two real Android integration checks. It is still
not a working YouTube ad-removal or SponsorBlock module.

## Implemented in this pass

`toolchain/xax/managed_dispatch.py` constructs a canonical XAX graph containing
one typed managed external call:

```text
XAX entry([B)[B -> org.youtubehideads.bf.dispatch_all.run([B)[B
```

The clean pinned XAX checkout verifies the binary canonical store and emits
`xax.P52ac7999d1df7bb9.entry([B)[B`. Android D8 converts the compiler-issued
class and the source-attested Brainfuck router into DEX. ART resolves the
managed method reference directly. No project JNI resolver, native library,
handwritten Java host or C host is required for this call.

All twelve existing BF policy bodies remain unchanged and retain ownership of
their decisions. The current bridge is a raw internal call, with no BFH1/BFR1
frame validation, Boolean validation, generation checks or action authorization.
It must not be exposed directly as a production hook boundary.

`scripts/verify_managed_dispatch_device.py` rebuilds the router, constructs and
verifies XAX state, compiles the test-only Java oracle, runs D8, checks the DEX
entry, verifies ADB transport hashes, compares results on ART and records actual
device evidence. It reuses the existing corpus and reference interpreter.
`tests/test_managed_dispatch.py` proves deterministic compilation and rejects a
tampered BF JAR without leaving a stale build-success report.

The generic dependency probe now distinguishes the unimplemented production
YouTube host from controlled runtime tests. JNI lookup is no longer reported
as a mandatory blocker for the managed route. The source-owner audit reports
integration fields as uninspected, rather than falsely asserting that no store,
APK or device run exists.

This preserves SRP and separation of concerns: graph construction, compilation,
source integrity and device validation have separate existing responsibilities.
The graph depends on the frozen router signature. No framework, policy switch,
dependency or speculative SOLID class hierarchy was added.

## Tools actually used

| Tool/environment | Observed version/path |
| --- | --- |
| Python | 3.12.10 |
| JBR | OpenJDK 25.0.3; Java oracle compiled with `--release 17` |
| XAX | Clean `build/xax-pinned`, SHA `9e44eedfc241d25bb5062b38af105f75234000e2` |
| XAX implementation executing | Upstream bootstrap compiler; no self-hosting claim |
| SDK build tools / D8 | `C:\Users\SiN\AppData\Local\Android\Sdk\build-tools\36.0.0` |
| ADB | Requested `D:\Android\platform-tools\adb.exe`, platform-tools 37.0.1 |
| Device | Pixel 8 Pro, Android 17 / API 37, arm64-v8a |
| Framework | Vector 2.2, version code 3080, libxposed API 102 |
| YouTube installed | 21.41.525; not hooked or functionally tested |

The existing external `D:\GitHub\brainfuckC` adapter and native-policy evidence
remain available. **This new managed path uses the existing project JVM BF
compiler, not BrainfuckC's native ELF backend.** No new BrainfuckC compilation
or BrainfuckC-to-XAX native APK linkage is claimed in this pass.

## Executed checks

| Check | Command/procedure | Result | Evidence |
| --- | --- | --- | --- |
| Canonical graph/store and JVM artifact | `python -B -m toolchain.xax.managed_dispatch --xax-source build/xax-pinned --policies generated --out build/xax-managed-dispatch` after router build | PASS | `evidence/xax_20261016/managed-build.json` |
| Managed XAX → BF on ART | Device command below | PASS: 4,463 comparisons; three empty/unknown selector inputs; null exception propagation; recovery after failure | `evidence/xax_20261016/managed-device-result.json` |
| XAX lifecycle build | `python -B -m toolchain.xax.smoke_build --xax-source build/xax-pinned --out build/xax-smoke --local-research-only` | PASS: real canonical store and unsigned APK | `evidence/xax_20261016/lifecycle-build.json` |
| Vector controlled lifecycle | Test-sign, install, enable only for `com.example.target`, launch, inspect process log/maps and heap, uninstall | PASS: module loaded; one class and one instance; process survived | `evidence/xax_20261016/vector-device-result.json`, target log/maps and scope files |
| Full regression | `python -B -m unittest discover -s tests -v`, with JBR on PATH and `XAX_SOURCE_DIR` set | 136 discovered: 123 passed, 13 skipped | `evidence/xax_20261016/unit-tests.log` |
| Final changed diagnostic/build checks | `python -B -m unittest tests.test_android_probe tests.test_managed_dispatch -v` | 3 passed | `evidence/xax_20261016/final-checks.log` |
| Policy source boundary audit | `python -B -m toolchain.brainfuck.audit` | PASS: 12 BF owners; no unexpected conventional application sources | `generated/language_audit.json` |
| YouTube filtering / live SponsorBlock | Not implemented | NOT RUN | No success claim |

The 13 skips require Linux/GCC/JDK for the existing desktop C/JNI oracle.
They are not counted as passes. The full regression was followed only by the
focused checks for the final diagnostic changes.

### Reproduce the new managed device test in PowerShell

From this project directory, with the device attached:

```powershell
python -B -m scripts.verify_managed_dispatch_device `
  --xax-source build/xax-pinned `
  --java-home 'C:\Program Files\Android\Android Studio\jbr' `
  --build-tools 'C:\Users\SiN\AppData\Local\Android\Sdk\build-tools\36.0.0' `
  --adb 'D:\Android\platform-tools\adb.exe' `
  --serial 38021FDJG00610
```

Observed output:

```text
PASS managed_xax_bf=4463 invalid=4 recovery=1 native_libraries=0
```

The Java oracle is exclusively `tests/android/XaxManagedDispatchProbe.java`.
Its reflection enters the XAX method, whose generated code directly invokes BF.
The oracle never computes a feature decision. The test DEX contains the oracle,
XAX entry and BF router; it is separate from the lifecycle module APK.

### Controlled Vector procedure

The lifecycle APK was signed locally with the pinned upstream's **public test
signer**, through `benchmarks.bench_android_apk._signing_capability` and
`xax_apk_signing.sign_apk_v2`. The target came from upstream's
`bench_android_libxposed_target.build_fixture(debuggable=True)`. Both signatures
passed upstream `inspect_apk_v2`. This target is a compiler fixture, not a
YouTube application or project manager implementation.

Both test package names were confirmed absent before installation. Commands:

```powershell
$adb = 'D:\Android\platform-tools\adb.exe'
& $adb -s 38021FDJG00610 install -t build/xax-vector-smoke/target-signed.apk
& $adb -s 38021FDJG00610 install -t build/xax-vector-smoke/module-signed.apk
& $adb -s 38021FDJG00610 shell su -c '/data/adb/modules/zygisk_vector/cli modules enable org.youtubehideads.module'
& $adb -s 38021FDJG00610 shell su -c '/data/adb/modules/zygisk_vector/cli scope set org.youtubehideads.module com.example.target/0'
& $adb -s 38021FDJG00610 shell am start -W -n com.example.target/.XaxActivity
& $adb -s 38021FDJG00610 shell am dumpheap com.example.target /data/local/tmp/youtubehideads-smoke.hprof
```

The process log recorded `Loaded module org.youtubehideads.module successfully`
and successful loading of the module's `libxaxapp.so` in its isolated namespace.
The pinned Vector harness's HPROF reader found exactly one
`xax.generated.XaxModule` class and one instance in the controlled target.
No debugger was attached. Callback counts and hook interception were not measured.
The heap was inspected, hashed and removed; only its summary and digest are saved.

Both test packages were uninstalled afterward. A follow-up `pm path` check found
neither package, and Vector reported no scope records for the removed module.
YouTube settings/data and existing module scopes were not changed.

## Diagnosed issues

- ADB cannot reach its server from this sandbox. The supplied ADB works with
  host access; no alternate ADB installation or device reset was needed.
- Python imports can modify tracked `.pyc` files in the pinned XAX checkout.
  Only cache changes caused by this run were restored. The new adapter disables
  bytecode writes before upstream imports; the checkout remains clean.
- The first ART oracle expected `IllegalArgumentException` on null, but the
  actual BF JVM backend raises `NullPointerException`. Device logs identified
  the incorrect test expectation. The corrected test verifies propagation and
  recovery. There was no compiler or policy fix for this test-harness error.
- Sandbox temporary-directory ACLs prevented ordinary fixture creation during
  the initial unit-test attempt. The full suite passed with host access.

## Artifacts and proof boundaries

| Actual output | Purpose |
| --- | --- |
| `build/xax-managed-dispatch/dispatch.xax-store` | Verified canonical XAX program; SHA-256 `aec664a22e0b5b0e3dd94a067df1dcf0f73ff16913624f029fca876ac4438512` |
| `build/xax-managed-dispatch/dispatch.jar` | XAX compiler-issued managed call |
| `build/xax-managed-dispatch/probe.dex` | Test oracle + XAX managed call + genuine BF router |
| `build/xax-smoke/lifecycle-smoke.canonical-store` | Separate no-op lifecycle program |
| `build/xax-smoke/lifecycle-smoke-unsigned.apk` | Controlled lifecycle smoke APK |
| `build/xax-vector-smoke/module-signed.apk` | Same smoke module, public test signer; not a release |
| `build/xax-vector-smoke/target-signed.apk` | Upstream controlled test target |

There is **no production debug/release ad-removal APK**. No XAX-derived binaries
were published or redistributed. The upstream redistribution-license question
remains open; local build/test evidence does not resolve it. The workspace has
no top-level Git metadata, so no commit or PR was created.

## Remaining implementation, in dependency order

1. Implement the versioned host request/reply contract in canonical XAX: exact
   lengths/types, Boolean/one-hot validation, generations and stale-event checks,
   bounded output and action validation. Keep policy decisions in BF.
2. Connect that checked managed call to an actual libxposed hook callback.
   The current upstream hook carrier supports bounded pass-through/constant
   replacement; the current lifecycle exports are no-ops. Neither calls BF.
3. Implement DexKit loading, split-aware resolver identities, actual structural
   matching, ambiguity rejection and cache invalidation against installed
   YouTube. No target descriptor or ad fingerprint has been fabricated.
4. Add type-safe player/feed/search/Shorts/promotion/component actions and verify
   ordinary playback/navigation alongside each suppressed surface.
5. Add the XAX manager, RemotePreferences persistence and hot configuration flow.
6. Add SponsorBlock networking/parsing, video/timeline provenance, segment
   processing and real seeking, preserving BF category/window/seek decisions.
7. Run the full functional acceptance matrix and resolve distribution/signing
   requirements before producing a release.

The ad/SponsorBlock feature matrix in `docs/FEATURE_COVERAGE.md` remains
unchanged: twelve executable policy kernels exist, but every real YouTube
feature is still unimplemented/unverified. The attached document informed this
continuation; its instruction to discard the existing project was not applied.
