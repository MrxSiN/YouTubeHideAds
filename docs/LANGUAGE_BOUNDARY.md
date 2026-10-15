# Language boundary / purity audit

**Current module (2026-10-16):** `toolchain/xax/module_graph.py` authors the
canonical XAX platform program for libxposed lifecycle, Settings toolbar entry,
the in-YouTube Dialog page and its event callbacks. The pinned XAX JVM compiler
emits the Hooker and click-listener implementations. A project-owned build
adapter uses upstream `DexBridgeSpec`/`DexAssembledMethod` to emit the exact
API-102 `onPackageReady` → XAX static-entry forwarding ABI; this is new project
lowering, not an upstream feature falsely claimed as already supported.
The forwarder contains only the call and return; no application decisions.

The Android manifest is ordinary launcherless XML compiled with SDK AAPT2,
because the pinned XAX manifest carrier requires an Activity. D8 composes the
XAX and BF classes, and SDK apksigner signs with a local development key.
Python is build/test infrastructure; no authored Java/Kotlin/C/Python feature
runtime is packaged. The real BF router executes in YouTube when the page
checks its engine. This is a self-check, not synthetic evidence of ad removal.
No standalone manager remains in the current product scope.

**Latest XAX integration (2026-10-16):**
`toolchain/xax/managed_dispatch.py` authors a canonical graph containing one
typed external call to `org.youtubehideads.bf.dispatch_all.run([B)[B`.
The pinned XAX compiler verifies its binary store and emits a JVM class; D8
converts it and the source-attested BF router into DEX. ART ran 4,463 matching
cases through that call with no native library. No feature decision moved into
Python, Java or XAX. The Java driver under `tests/android/` only supplies inputs,
compares outputs and checks exception propagation; its DEX is never packaged
in the lifecycle module. The separate lifecycle APK has no BF invocation.

This managed path uses the existing project JVM BF backend, not BrainfuckC's
native backend. It is a raw internal policy call: framed input validation and
reply/action authorization still need an XAX runtime implementation.

**Current (2026-10-16):** All twelve feature policies live in executable `.bf`;
`toolchain/brainfuck/*.py` is compiler/test infrastructure, **not Android feature
runtime code**. Handwritten Java and C are restricted to `tests/`, including
the new `tests/android/brainfuckc_probe.c` native callable harness. None is
shipped as Android application logic. The external BrainfuckC compiler emits
native policy code from validated eight-command streams; the Python device
verifier supplies test vectors and reference results only. Its 4,463 passing
Android-shell comparisons do not implement the missing XAX host, JNI bridge,
Xposed hooks or live YouTube integration. See `docs/BRAINFUCKC_ANDROID.md`.

| Brainfuck owner | Input-dependent policy | Planned generic XAX capability |
| --- | --- | --- |
| `suppress_video_slot` | gate slot/safety, invert channel whitelist | validated player callback and lifecycle |
| `suppress_feed_item` | combine paid-renderer evidence | typed renderer interception |
| `suppress_search_result` | combine search surface and paid flags | feed/search renderer adapters |
| `suppress_shorts_slot` | require generation integrity | per-Short scoped events |
| `suppress_premium_upsell` | marketing eligibility | view/layout/data callbacks |
| `suppress_paid_shelf` | verify paid vs ordinary product surface | structural component data |
| `collapse_filtered_container` | decide conservative collapse | UI detach/update/cleanup |
| `reject_ambiguous` | ambiguity policy | DexKit query, typed candidate verification |
| `select_sponsor_category` | choose the matching category setting from eight user-controlled modes, using real executable Brainfuck; emit CATEGORY_AUTO_SKIP | parse the category string into the versioned eight-slot one-hot wire encoding; validate one-hot shape and pass to BF |
| `authorize_seek` | six input-dependent skip authorization gates and 64-bit segment-end output | video identity/time window, live-state verification, category protocol and actual seek; full range calculation still missing |

The host MUST NOT precompute a high-level `isAd` policy boolean while claiming Brainfuck classified the item. Current Boolean policy inputs are **unit-test abstractions**, not yet verified from low-level YouTube method evidence. That is an open architectural task. SponsorBlock seek-target **emission** is now Brainfuck-owned, but the surrounding time-range predicate and end-point derivation from raw segment data are still not complete. No SponsorBlock completion claim is made.

No exception for hiding/skip policies in XAX has been approved. If a future exception is unavoidable, document the exact failed approaches, typed API limitations and tests here before implementation.

## Iteration 2: checked ABI boundary, no Android policy in Python

`toolchain/brainfuck/host_abi.py`, `host_link.py`, and `abi_vectors.py` are **off-device test/compiler tooling**. The codec verifies transport framing and generic safety; only the original `.bf` executable commands calculate the feature action. Stable IDs and permissible action shapes are wire-contract definitions, not renderer classifiers. The test JVM loader only invokes `run([B)[B`. None of these test components are packaged as Android application code.

The request's Boolean count is sourced from executable Brainfuck commas, rather than editable comments. That avoids a hidden, annotation-based runtime behavior channel. A JAR is permitted for test linking only if all compiled class bytes exactly match current `.bf` code and its manifest source digests; this is now tested.

The Android/XAX language boundary is still unimplemented. No broad XAX exception for sponsorship policy, ad filtering, renderer classification, or seek selection has been granted. A well-formed `SEEK_PLAYER` action is emitted by Brainfuck for eligible fixture inputs, but is **always rejected for Android execution** by the off-device codec until the XAX runtime host and current-player validation exist.

## Iteration 3 — canonical XAX build-tool adapter

`toolchain/xax/smoke_build.py` is **off-device Python build orchestration** that invokes external XAX APIs to create canonical semantic objects and typed no-op JNI callbacks when the pinned XAX compiler is available. Its Java/Android implementation is emitted entirely by the external XAX backend; it does not author Java/Kotlin/C application runtime source. A test Activity is supplied by XAX's *external test fixture*, not by this repository. This is explicitly a controlled testing scaffold and cannot count as a completed independently authored YouTubeHideAds manager.

`toolchain/xax/verify_apk.py` only parses APK/DEX/metadata bytes during build verification. It neither classifies YouTube content nor hooks the Android runtime. The smoke build has **no Brainfuck feature invocation**, so it fails the final application language-integration acceptance criterion. `integrated` inspection detects only BF class declarations, not that any XAX hooks call their policy methods.

## Iteration 6 — category policy provenance

Prior to this iteration the test host supplied `category_auto_skip` as an already-computed Boolean in the `authorize_seek` request. That left a category policy decision outside Brainfuck. A new `select_sponsor_category.bf` now computes category eligibility from eight independent toggles and a structurally validated one-hot category. This does **not** solve temporal-window computation, segment matching, or Android coupling. The off-device `checked_sponsor_chain` ensures the next seek request's category gate matches the earlier BF category reply from the same generation. Future XAX host code must wire and enforce these exact semantics before enabling any live seek.

## Iteration 8 — Brainfuck-owned selector routing

The generated `dispatch_all` class consists only of genuine eight-command BF with the ten source bodies copied unmodified. Python emits the fixed control-flow wrapper but does not make feature or category decisions at runtime. A single BF `run([B)[B` method now handles the ten policy variants on the JVM, so the prospective XAX runtime needs only one JNI method signature. Its input selector is a wire-contract identifier, not a hidden classification rule. **No XAX/Android runtime method call exists yet**; the new optional D8 route is only source-verified JVM plus synthetic DEX structural conformance. See `docs/BRAINFUCK_ROUTER.md`.


## Iteration 9 — isolated test-native JNI proof

The actual JDK JNI smoke test compiles `tests/jni/jni_router_probe.c` and `tests/jni/JniRouterProbe.java` only inside a temporary test directory. The C function performs JNI class/method lookup and calls the BF-compiled static method directly; **it does not implement a single BF policy**, is never included in the JAR/D8 packaging command, and is forbidden as the Android feature fallback. `toolchain/xax/router_call_plan.py` authors an external-XAX-dependent internal semantic graph source with no executable Android caller. That graph has not been constructed or validated against the missing XAX compiler. See `docs/JNI_ROUTER_BOUNDARY.md`.
