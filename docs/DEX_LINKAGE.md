# Current module path (2026-10-16)

`toolchain/xax/module_build.py` now packages a real launcherless module. A fixed
DEX API-102 entry forwards to the canonical XAX managed program; D8 links that
program and the source-attested BF router. The module loaded in YouTube and the
page's XAX callback invoked BF there. This is verified page/engine linkage only,
not advertisement-hook linkage. See `history/ITERATION18_REPORT.md` and
`evidence/module_20261016/`. The earlier linkage notes below are historical.

# Iteration 4 — source-attested Brainfuck JVM-to-DEX packaging (unexecuted D8)

## Scope and state

This iteration adds an actual **build script and Python build-tool implementation** for invoking the **external Android D8 compiler** on the verified, originally nine-class, genuinely compiled Brainfuck JVM JAR. Given an independently produced XAX Android libxposed *controlled-target smoke APK*, the linker appends the D8-emitted DEX files in unused multidex slots. It is not a generic Java/Kotlin app feature runtime: all feature policies remain compiled from the eight Brainfuck commands, and Java in the project exists only as test code. D8 and XAX are external toolchains.

**Important limits:** D8 is absent from the current environment, as is the pinned XAX checkout. The full D8 invocation, XAX APK build, Android verifier/dex2oat and device execution are **NOT RUN**. No new installable Android APK is claimed. The unit tests exercise the linker with intentionally **noninstallable, structurally formed** synthetic DEX/APK fixtures, including fake one-instruction method bodies; such passing checks are not evidence that the Brainfuck algorithm runs on Android.

The *XAX libxposed lifecycle smoke host* has **no calls** to the policy methods. Appending their DEX definitions **does not make a callable host bridge**, nor does it make ad suppression or SponsorBlock work. For this reason the only accepted output mode of the linker is `linked_smoke` with a scope of `com.example.target`, not a releasable YouTube module. A separate `integrated` structural verifier mode exists for later work but is not an integration claim. The project still requires an independently verified XAX-authored ABI dispatcher that performs real bounded `run([B)[B` calls, handles errors and applies typed actions.

## Build commands when the actual upstream toolchains are available

On a host with the legally usable XAX checkout at the exact pinned revision, D8, JDK and Android test tooling:

```sh
XAX_SOURCE_DIR=/absolute/path/to/pinned/XAX \
D8_BIN=/absolute/path/to/android-sdk/build-tools/VERSION/d8 \
./scripts/link_xax_smoke.sh
```

`toolchain.xax.link_d8` verifies the source-authoritative JAR byte for byte, invokes D8 with `--release --min-api 28 --output <dir> <jar>`, validates actual DEX definitions and `run([B)[B` code items, and appends the output to the unsigned XAX APK. It then performs a smoke-scope and payload check and emits an evidence JSON containing source digests, JAR/APK SHA-256, DEX hashes, class count and explicit nonverification flags. No post-composition APK signing is performed. Android APK signature schemes v2/v3 would be invalidated by ZIP recomposition; the linker refuses a base ZIP with signatures and does not claim deployment readiness or zipalign validity. It can only be used on unsigned artifacts.

The DEX method inspector checks public DEX table structure (`string_ids`, `type_ids`, `proto_ids`, `method_ids`, `class_defs`, `class_data_item`, `code_item`) and requires all currently registered concrete policy class definitions to contain a `run([B)[B` code item. It rejects missing members and malformed offsets. **It does not execute or decode the entire method body, verify type safety, enforce source-to-DEX behavioral equivalence, inspect JNI hook invocation, or run ART's bytecode verifier.** Independent interpreter/JVM differential testing remains separate evidence from Iterations 1–3.

## Build-time safety contract

- Fail when original `.bf` input differs from the JAR, if the source digest or class bytes change, or if an unexpected compiled class exists.
- Fail when the external D8 command is absent, exits with an error, times out, produces no DEX, or emits unrecognized extra classes, missing policies, missing `run` methods, duplicate classes or invalid DEX integrity.
- Fail on signed APKs (including Java/JAR-style signatures and APK Signing Block markers), unsafe paths, duplicate ZIP entries, malformed host DEX, or collisions with already included policy classes.
- Only add `classesN.dex` entries after existing XAX classes, without overwriting the upstream host. The output remains deliberately restricted to the controlled test scope.
- Produce fixed-timestamp ZIP entries, source hashes and a report of what was *actually verified*; no claim of YouTube behavior, XAX runtime call linkage, D8 behavior equivalence, or Vector execution.

## Future integration milestone

1. With a permitted, pinned checkout, execute the genuine `smoke_build.py` and record canonical XAX object IDs, store digest and emitted manifest/DEX evidence.
2. Execute real D8 on the source-attested JAR, check its DEX methods, then validate it on Android/ART with concrete byte inputs against JVM reference outputs. Establish safe `run([B)[B` execution, resource bounds and exceptions.
3. Construct a **canonical XAX semantic** method caller through verified typed Android/JNI APIs that validates the BF host-frame protocol; prove its Xposed lifecycle dispatch invokes the actual compiled classes, not a constant.
4. Integrate the first narrowly identified DexKit YouTube hook, run on a compatible Vector device, then scale coverage without weakening safe failure behavior. Resolve the unlicensed XAX redistribution question before shipping XAX-derived binaries.

## Iteration 6 registry expansion

The source-attested JAR registry and D8/DEX linker expectations now contain **ten** Brainfuck programs including `select_sponsor_category` (`0x0402`). All DEX class counts and method-shape checks are dynamically keyed to `FEATURE_IDS`, rather than accepting a formerly hardcoded nine-class count. This change was tested with synthetic (noninstallable) DEX fixtures and a fake-D8 subprocess only. No real D8 or Android execution took place.


## Iteration 8 — optional eleven-class BF router DEX path

`link_d8.py` now accepts `--router-jar generated/brainfuck-router.jar --router-manifest generated/router.json` in addition to the original ten-policy JAR. A second source-bytecode verifier rejects tampered router artifacts before D8 is called; both JAR paths are supplied to one `d8 --release --min-api 28` command. `validate_policy_dex(..., with_router=True)` and `inspect_module_apk(..., mode='linked_router_smoke')` require all 11 class definitions and concrete `run([B)[B` code items. `scripts/link_xax_smoke.sh` opts into that controlled research-only mode. The synthetic tests contain dummy `return-object` code items, **not** executable translated Brainfuck. This is not a valid signed/release APK, a verified XAX JNI call, or an Android runtime test.

## Iteration 13 revision

The feature registry now defines **eleven policy classes plus one router** (twelve total DEX class definitions for the controlled linker). The adapter keys this count from `FEATURE_IDS`, rather than a hardcoded count; all updated structural tests use synthetic fixtures and are **not** real D8/Android tests.
