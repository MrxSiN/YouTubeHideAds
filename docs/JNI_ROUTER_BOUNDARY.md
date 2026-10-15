# Brainfuck router JNI boundary — Iteration 11

## Grounded ABI

Compiled Brainfuck class: `org.youtubehideads.bf.dispatch_all`.
Static public method: `byte[] run(byte[] payload)`; JNI descriptor `([B)[B`.
The input consists of one *BF-owned* selector (1–10) and the raw selected-program input bytes. Output is the selected program's original raw action bytes. Output framing, `BFH1` generation/feature checking, and device action permission remain obligations of a future XAX host. **No one may treat an empty result as permission to act.**

## Executed desktop JNI proof

`tests/jni/JniRouterProbe.java` loads `tests/jni/jni_router_probe.c` as a temporary JDK native shared library. That *test-only* C code invokes actual JNI operations `FindClass`, `GetStaticMethodID` and `CallStaticObjectMethodA` to reach the real Brainfuck-compiled router class. It implements no policy and ships to no Android artifact. The `tests/test_jni_router_probe.py` suite compiles it under a temporary directory and proves:

- For **both** BF AOT JVM modes, every tested JNI answer equals an independent reference interpreter answer for every chosen feature, all 64 six-gate SponsorBlock combinations, eight category positions and both toggle values, and all policy Boolean combinations.
- High-bit/zero byte data survives both sides of the JNI call, including a 64-bit little-endian SponsorBlock endpoint.
- A null input creates a Java `IllegalArgumentException`; a missing BF class propagates `NoClassDefFoundError` (not an invented success).
- Unsupported selectors emit empty bytes, which the future host must reject.
- Java and C test harness files are absent from production JARs and explicitly restricted to `tests/`.

### Iteration 10: isolated loader runtime proof

The same test-only Java/C JNI probe now supports an explicit `URLClassLoader`
with **null parent** and a separate classpath that deliberately **omits** the
Brainfuck router. The native loader-aware test resolves the compiled router
through `ClassLoader.loadClass("org.youtubehideads.bf.dispatch_all")` instead
of assuming `FindClass` will see the class. It then obtains the exact
`run([B)[B` method ID and executes the original BF AOT bytecode. The suite
proves in BOTH compilation modes:

- `FindClass` cannot see the router from the system loader while the explicit
  module loader can, for all ten source-owned policies.
- An absent module loader, missing class/JAR, null byte-array input, and a
  class containing an incompatible `run(int)` method do **not** authorize an
  action; the originating exception is observable by Java.
- Binary 64-bit seek endpoint bytes survive JNI, including zero and maximum
  unsigned 64-bit test payloads (policy authorization remains independent).
- No Java/C test fixture is included in the Brainfuck AOT JAR or APK linkage
  adapter. Java and C here are **only an off-device test oracle**.

This is a JVM JNI **runtime** proof, but not an ART, DEX, libxposed, Vector, YouTube, or XAX-host runtime proof.

## XAX-side semantic construction

`toolchain/xax/router_call_plan.py` freezes the module-loader-qualified BF class identity, exact method signature, `[B` argument identity and JNI 1.6 `CallStaticObjectMethodA` contract. When the external pinned XAX checkout is available, `make_xax_call_plan()` constructs actual upstream `jni_method_call_plan`, `jni_argument_pack_plan`, `jni_get_static_method_id_contract`, and `jni_stack_method_call_contract` objects. `make_xax_bound_router_call_graph()` authors a genuine XAX internal semantic function for a **pre-resolved** local class handle plus typed static method ID; it packs one borrowed `jbyteArray` reference into a fully initialized `jvalue[]`, calls the JNI function pointer, threads local-reference/exception/effect proofs, ends the stack allocation, and explicitly executes `ExceptionCheck`. A
checked exception flag is returned to the future caller, **without** treating
it as a successful dispatch.

`toolchain/xax/loader_resolution.py` now also freezes the typed signature
`ClassLoader.loadClass(Ljava/lang/String;)Ljava/lang/Class;` and constructs an
additional bounded XAX graph for `CallObjectMethodA` on an injected module
loader, a pre-resolved `loadClass` method ID, and a pre-existing Java string.
Its returned local `java.lang.Class` is NOT automatically accepted as the
loader-qualified Brainfuck router class; a separate check/refinement is needed.

**Limitations:** Neither XAX graph has been constructed against the pinned XAX
checkout in this environment. The graphs do not create the Java class-name
string, obtain the module ClassLoader from an actual libxposed callback,
resolve the dynamic method IDs on-device, **branch** on pending exceptions,
release all local owners, return safely to an exported managed callback, or
connect to libxposed and DexKit hooks. It must not be packaged as an Android dispatcher until those obligations and the canonical graph verifier are satisfied. The in-test C JNI path is not an allowed production substitute.

Run an *opt-in* external canonical-store conformance probe with:

```sh
PYTHONPATH=. python3 -m toolchain.xax.check_router_graph --xax-source /path/to/pinned/XAX --out build/xax-router-call-plan.json --store build/xax-router-call.xax-store
```

It attempts construction of **five** typed graphs (the three JNI subroutines, a fail-closed dispatch guard, and their composed router caller) and rejects a checkout without commit `9e44eedfc241d25bb5062b38af105f75234000e2`. The updated probe also requires actual XAX canonical binary-store write and verifier success, not just graph construction. Even canonical-store verification would not constitute an Android APK or executable integration. The graph probe deliberately refuses to create a "success" report without importing the actual XAX implementation.

## Required next step

Complete the **XAX-owned** classloader-correct resolution/verification graph and the managed callback that uses the typed plan, handles exceptions/null return safely, and converts the result into host-authorized actions. Only after externally built DEX/ART validates that path can the actual YouTube module be implemented. Keep playback seeking disabled until a live validated context exists.

## Iteration 11: class identity and canonical method resolution

The test-only native oracle now performs **two explicit checks after
`ClassLoader.loadClass`** and before `GetStaticMethodID`:

1. `Class.getName()` must match `org.youtubehideads.bf.dispatch_all` exactly.
2. `Class.getClassLoader()` must be the **identical JNI object** to the
   supplied intended module loader (`IsSameObject`, not name equality).

An explicitly parent-delegating loader is rejected with
`ROUTER_LOADER_PROVENANCE_MISMATCH`; an overridden `loadClass` that returns
`java.lang.String` instead of the requested class is rejected with
`ROUTER_CLASS_NAME_MISMATCH`. These checks run on desktop Linux + JDK in
both BF compilation modes. Alternating rejection/success loops exercise
JNI local-reference cleanup but **do not prove leak freedom on ART**.

The checked desktop test remains a *test-only reference oracle*, not an XAX
or Android application host. Even a matching name and defining loader alone
are insufficient to prove bytecode authenticity; the future host must bind
its trusted loader to source-attested, verified DEX/code artifacts.

`toolchain/xax/static_method_resolution.py` now authors a third XAX
subroutine around the upstream `GetStaticMethodID` contract. It accepts a
**prevalidated, loader-qualified local Class**, its linear owner, two live
NUL-terminated C strings for `run` / `([B)[B`, and a JNI memory frontier;
it returns the typed method ID, threaded owner, and an `ExceptionCheck`
status. It does not prove the class handle or strings, guard a null method
ID, or branch on a pending exception. The preceding loader graph still returns
a **generic** `java.lang.Class` and cannot yet feed the static resolver by
claiming a type refinement it has not demonstrated.

`toolchain/xax/store_evidence.py` adds canonical-store evidence: the three
actual imported XAX functions must pass CID/reference-closure inspection,
`write_store` and `verify_store(StoreReader(...))` before the external check
can report structural success. Missing objects and CID conflicts fail closed.
No local XAX compiler was available to run that check, so these three
semantic subroutines are **authored but not compiled or verified**.
The optional GitHub Actions research workflow now requests the same canonical
store conformance check, with no artifact upload. It has not been run here.

### Outstanding end-to-end obligations

Acquire a real module loader from a libxposed lifecycle callback; create and
own the Java router name and C-string method/signature; verify class name,
loader identity and class-byte origin; refine the generic class reference to
one typed module `jclass`; handle pending JNI exceptions through a branched
XAX graph while disposing of all reference ownership; then link and execute
on Android ART. No playback action may proceed before these steps and a
separate live-action authorization test pass.

## Iteration 12 — explicit conditional guard and canonical-store reachability

`toolchain/xax/dispatch_guard.py` authors a fourth canonical XAX graph with
**real conditional control-flow nodes** (`IntCompare.EQ`, `cbr`). Its five
inputs are proof-status bytes: no pending JNI exception, exact class binary
name, exact defining loader, non-null resolved method ID, and verified output
frame. Every status must equal **exactly 1**; zero or any non-Boolean byte
branches to denial. This is generic platform gating, not YouTube policy logic.

The graph is **not attached** to the three JNI subroutines and does not itself
compute any proof status. The caller must first establish these facts with
loader-qualified typed JNI calls, class-origin integrity, current exception
state, and Brainfuck-frame validation. Until then the gate is not authorization
to modify YouTube or invoke any seek. No XAX graph was compiled or tested on
Android in this environment.

`toolchain/xax/store_evidence.py` now emits only semantic objects reachable
from the single store root and refuses missing reachable references or CID
conflicts, rather than writing every optional construction helper. The opt-in
research workflow must build all **four** XAX functions and pass the genuine
upstream `write_store`/`verify_store` call before reporting a canonical store.
That independent external verification has not been run locally.

## Iteration 15 — composed XAX router-call safety gate (uncompiled)

`toolchain/xax/checked_router_dispatch.py` now **composes two actual XAX
semantic functions** using `Operation.CALL_DIRECT`: the typed
`CallStaticObjectMethodA` subroutine and the five-condition dispatch guard.
The first guard argument is no longer a free-standing, caller-supplied
Boolean. It is calculated from the returned JNI `ExceptionCheck` byte via
`IntCompare.EQ(..., 0)` and `INT_ZERO_EXTEND`:

```text
router_call(...)->(result_array, array_owner, class_owner,
                   exception_check_byte, maybe_exception_state, JNI_effect)
no_pending_exception = (exception_check_byte == 0)
dispatch_guard(no_pending_exception, name_verified, loader_verified,
               method_nonnull_verified, reply_frame_verified)
```

The composer returns the guard result **alongside** the untrusted JNI output
reference, both reference-owner tokens, exception-state token, and JNI effect.
A future on-device caller MUST branch on the guard result **before reading or
acting on the returned array**; receiving a reference is not itself proof of
its validity. The four remaining proof bytes have not been bound to
trustworthy XAX-produced checks, and the `ExceptionCheck` status does not
clear a pending exception. The graph is not an exported JNI callback.

`check_router_graph.py` now requests an upstream canonical store with **five**
functions (loader call, method resolution, router call, guard, and composed
router/guard caller). `store_evidence.py` uses `PROGRAM_ROOT -> MODULE` and
rejects a missing direct-call dependency before writing only the root-reachable
objects. The optional GitHub workflow asserts the composed edge and its
unresolved runtime proof obligations. These steps are **only executable with
the pinned external XAX checkout** and were not performed locally.

The local test oracle exhaustively enumerates all 1,024 combinations of one JNI exception value and
four external status values drawn from `{0, 1, 2, 255}`: a nonzero exception status always rejects. This is off-device host
integrity testing, not Brainfuck feature logic and not XAX type-checking.

The next actual blocker is to build the source against the pinned XAX compiler,
fix any verifier diagnostics, then implement loader provenance, genuine
method-ID validation, response-frame validation, exception cleanup, and a
libxposed-managed exported callback. No Android APK or YouTube hooks result
from this composition alone.
