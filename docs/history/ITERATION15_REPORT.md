# YouTubeHideAds — Iteration 15 report

Date: 2026-10-15. **Offline research/build milestone, not an installable Android module.** No YouTube hooks, on-device SponsorBlock seeking, DexKit member discovery, or Xposed runtime verification was performed.

## Implemented

1. **First direct semantic-call composition between existing XAX subroutines.** `toolchain/xax/checked_router_dispatch.py` constructs a fifth XAX graph that calls the pre-resolved `CallStaticObjectMethodA` router graph using `Operation.CALL_DIRECT`, compares the router's `ExceptionCheck` output against zero using XAX `IntCompare.EQ` and `INT_ZERO_EXTEND`, then calls the existing fail-closed XAX five-condition guard using a second `Operation.CALL_DIRECT`. The first guard condition is consequently derived from that router call, not supplied as an arbitrary caller flag.
2. **Proof/ownership flow.** The new graph preserves the returned local `byte[]` reference, its local owner token, the input class owner token, the maybe-pending-exception resource state, and the external JNI memory effect. The XAX caller must test the guard bit before inspecting the output; no player or hook action is emitted.
3. **Strict limits preserved.** The other four guard statuses (exact class name, defining loader, non-null method ID, and verified reply frame) are still supplied as untrusted external status bytes. These are NOT yet computed from actual on-device XAX checks. The graph still assumes a pre-resolved typed `jclass` and method ID; it is NOT an exported libxposed callback. JNI exception status is observed, not cleared.
4. **Canonical-store probe expanded.** The external pinned-XAX command now requests all five semantic functions and a `PROGRAM_ROOT -> MODULE` store. It rejects absent/mutated `CALL_DIRECT` graph dependencies, missing XAX objects, and duplicate/conflicting CIDs before calling upstream `write_store` and `verify_store`. The opt-in GitHub Actions research workflow verifies the new graph evidence if explicitly run in an environment with an exact pinned XAX checkout; it was **not executed here**.
5. **Tests.** Eight new tests (including two graph-edge tampering cases) exercise the off-device reference gate for all `4^5 = 1,024` combinations of JNI exception status plus four caller flags drawn from `{0,1,2,255}`. They also test malformed status types/lengths, missing/duplicate semantic call edges, import blocking, and the research workflow's negative claims. This is NOT a substitute for XAX type checking.

## Executed verification

| Item | Result | Evidence |
| --- | --- | --- |
| Unit tests, group 1 (7 modules) | **49/49 pass** | `YouTubeHideAds_iteration15_tests_group1.log` |
| Unit tests, group 2 (7 modules) | **45/45 pass** | `YouTubeHideAds_iteration15_tests_group2.log` |
| Unit tests, group 3 (6 modules) | **30/30 pass** | `YouTubeHideAds_iteration15_tests_group3.log` |
| **All 20 test modules** | **124/124 pass** | Three complete nonoverlapping groups |
| JVM policy/JVM router AOT both modes | Pass; original hashes preserved | `YouTubeHideAds_iteration15_build.log` |
| Source/bytecode linkage & language audit | Pass | `YouTubeHideAds_iteration15_build.log` |
| XAX canonical semantic writer and graph verifier | **Not run** | Pinned compiler checkout absent |
| Android D8, SDK and ADB | **Unavailable** | Prerequisite probe in build log |
| Android APK, ART, libxposed, DexKit, YouTube | **Not executed** | No build or device evidence |

### SHA-256: unchanged binary outputs

- Baseline Brainfuck policies JAR: `e5c9680bc0cbeb65b7b01cef9e934ea1d0427df416cdc3fe03ed95d72cce48d6`
- Optimized Brainfuck policies JAR: `5e5be3dd984a98ddb73a7e5a9e6568cf19ac9f4a71b9e35b49caef4c0d930bc3`
- Baseline/optimized 12-way Brainfuck router JAR: `4df9da181ad805450211f606b3d61f5a8e035ecfe3fce73d6f2d8a8e8ee2472b`

## External compilation acceptance gate

In an environment with exactly `MrxSiN/XAX` at revision `9e44eedfc241d25bb5062b38af105f75234000e2`, execute:

```sh
PYTHONPATH=. python3 -m toolchain.xax.check_router_graph \
  --xax-source /path/to/pinned/XAX \
  --out build/xax-router-graphs/evidence.json \
  --store build/xax-router-graphs/router-graphs.xax-store
```

Treat **any** import, graph, linearity, CID, or verifier diagnostic as failure; fix the semantic graph instead of weakening the gate. Do not publish third-party XAX source/artifacts absent permission. Even an upstream-verified store demonstrates only a research semantic graph, NOT a working Android ABI callback or an APK.

## Next dependency

Obtain/build an actual pinned XAX environment, verify the five-function graph and resolve its verifier diagnostics. Then bind the four untrusted statuses to live classloader/method/frame checks, handle exceptions and local-reference lifetime, export a managed callback into an Android module, perform actual BF DEX linkage and verify on ART/libxposed. The Brainfuck policy calculations remain authoritative; there is no application-feature Java/Kotlin/C fallback.
