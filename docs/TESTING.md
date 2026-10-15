# Testing and observed evidence

**Module/page test (2026-10-16):** `scripts/verify_module_device.py` verified the
actual installed APK hash, module load in YouTube, one Settings toolbar entry,
three open/close cycles, system Back, BF execution inside YouTube, no failed
BF self-check and a surviving YouTube process. Launcher resolution returned
`No activity found`. Results and screenshots: `evidence/module_20261016/`.
This is not an advertisement-removal or SponsorBlock playback test.

**Latest, 2026-10-16:** see `history/ITERATION17_REPORT.md` and
`evidence/xax_20261016/`. The managed XAX → BF path passed 4,463 reference
comparisons, three empty/unknown selector inputs, null exception propagation
and recovery on Android ART. Vector 2.2 loaded the separate XAX lifecycle
module in a controlled app; a heap dump showed one module instance. This
does not test a BF-driven hook, YouTube filtering or SponsorBlock playback.

For the 2026-10-16 external BrainfuckC build and **4,463 actual Android-shell
native/reference comparisons**, see [BrainfuckC Android check](BRAINFUCKC_ANDROID.md)
and `evidence/brainfuckc_20261016/`. Earlier entries below are historical;
no XAX, JNI, Xposed or YouTube feature integration is established by this check.

Host: Debian-based container, Python 3.13.5 via `/opt/pyvenv/bin/python3`; OpenJDK 21.0.12.1; no Android SDK/adb/D8/Vector device.

Run:

```sh
PYTHONPATH=. python3 -m unittest discover -s tests -v
PYTHONPATH=. python3 -m toolchain.brainfuck.build --out generated
```

Test suite:
- Annotation grammar, comment/whitespace invariance, malformed input, bracket matching.
- Brainfuck byte-wrapping, EOF, binary output, nested loops, pointer/fuel/output bounds.
- Exhaustive truth tables for the simple Boolean policies (including player whitelist inversion); all 2,048 one-hot category permutations and the seek Boolean authorization cube are tested separately.
- Executable BF mutation changing output, and normalized source digest change.
- JVM differential execution in *both* optimization modes, against independent interpreter outputs via a compile-only Java reflection harness.

26/26 automated test methods passed on 2026-10-15 (iteration 2, after adding 13 ABI/link/probe/vector tests). 488 JVM outputs were compared against reference feature outputs across both optimizer modes (plus 20 compiled runtime-failure/semantics outcomes and mutation checks).

An earlier parser metadata bug, a non-terminating BF tape-transfer loop, and a fixture strictness mismatch were identified and corrected locally before the final passing run; no suppression behavior was tested on device.

Android/libxposed/DexKit/APK/YouTube integration: **NOT RUN** (not falsely categorized as passed). SponsorBlock network API and playback: **NOT IMPLEMENTED**. Actual execution counts and final artifact hashes are in `history/BUILD_REPORT.md` at the repository root.

## Iteration 2 — executable host-boundary oracles

- Test frame exact layouts (14-byte request, 15-byte response), version, ID, endianness and byte-exact golden vectors.
- Test malformed/truncated/oversized packets, forged feature IDs, invalid Boolean inputs, and stale generation checks fail without an action.
- Execute AOT-generated JVM classes through framed messages and check actions, in both optimized and unoptimized modes.
- Verify byte-identical regenerated classes and SHA-256 source identity, rejecting tampered class bytes and stale manifests.
- Prove annotation-only input-description edits do not alter the executable-sourced ABI arity.
- Reject SponsorBlock seek activation without a Brainfuck-owned 64-bit target and Android type/lifecycle verification.
- Produce an honest environment probe report; no XAX semantic store or Android APK is claimed.

Commands: `./scripts/build_fresh.sh`, `python3 -m scripts.verify_linkage`, and `python3 -m scripts.probe_android_integration`. The full standard run also updates `generated/language_audit.json` and prints actual JAR hashes.

### Iteration 3 XAX/API integration preparation

Run `PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_xax_artifact.py' -v` for synthetic malformed APK and DEX fixtures, Xposed scope/entry checks, and external XAX revision-gate tests. The fixtures **are not installable** and are not evidence of compiler or Android execution. `XAX_SOURCE_DIR=... ./scripts/build_xax_smoke.sh` requires an external, licensed, precisely pinned compiler; this command has not run in the current environment. `python3 -m toolchain.xax.verify_apk actual.apk --mode smoke` is a structural verifier only, never a runtime test.


## Iteration 4 — D8 linkage path, structural-only evidence

`tests/test_dex_link.py` tests deterministic unsigned APK/DEX composition using deliberately noninstallable synthetic fixtures, actual Brainfuck source-to-JAR identity, rejection of missing or duplicate class/method definitions, corrupt DEX tables, signed-APK modification, and failure to invoke an unavailable D8 executable. The verifier additionally requires concrete `run([B)[B` code items for every policy in `integrated` and `linked_smoke` mode. This is **offline packaging/code-item evidence, not D8 execution, ART verification, XAX-to-Brainfuck invocation or YouTube feature testing**. Read `docs/DEX_LINKAGE.md` before interpreting the result.

## Iteration 5 — typed SponsorBlock endpoint, offline only

`tests/test_sponsor_seek.py` exhaustively checks 64 gate combinations across multiple binary endpoints and direct JVM optimizations, plus malformed-length, stale-generation, spoofed-destination and unsigned-to-signed overflow safety. The only permit result is a typed action candidate, never a device seek. `testdata/bf_abi_v1_vectors.json` is regenerated from the executable Brainfuck and checked byte-for-byte. See `history/ITERATION5_REPORT.md`.

## Iteration 6: category policy and chain tests

`tests/test_sponsor_category.py` exhaustively tests all eight category selections against all 256 enablement masks through executable Brainfuck (2,048 cases) and recompiles/runs all combinations through both independent JVM AOT modes. One-hot mismatches, invalid Boolean values, stale cross-policy generations, forbidden inter-policy category gate modifications, unauthorized actions, source mutations and comment-only invariance are covered. `checked_sponsor_chain` is **not** Android runtime code. Overall suite: 54 tests if all requirements are available; exact current run in `history/ITERATION6_REPORT.md`.

## Iteration 7 controlled XAX transport

Run `PYTHONPATH=. python3 -m unittest tests.test_managed_transport -v` for
five offline tests, or `./scripts/build_fresh.sh` for the complete 59-test
suite. These tests construct *synthetic* noninstallable DEX fixtures and gate
`roundTrip([B)[B` method presence; they are not JNI device execution. The
upstream-XAX actual graph/DEX path remains NOT RUN. If a legally usable pinned
XAX checkout is installed, the nonrelease `./scripts/build_xax_smoke.sh` or the
manual `xax-transport-research.yml` workflow attempts that external build.


## Iteration 12 guard tests

`tests/test_dispatch_guard.py` exhaustively checks 1,024 status vectors
(4^5 from {0,1,2,255}), rejecting every value except five exact ones.
These test a standalone offline reference predicate, **not XAX execution**.
The same file checks root-reachable object selection, duplicate-CID
conflicts, missing root and missing referenced objects. Actual XAX graph
construction and `verify_store` must be run in the separate opt-in workflow.

## Iteration 14 offline validation

`tests/test_sponsor_time_window.py` verifies actual 64-bit timestamp-window semantics against the Brainfuck interpreter, optimized and baseline AOT JVM classes, twelve-way router, byte-exact generation and endpoint propagation, malformed signed-long input, and a strict execution budget. `tests/test_pointer_run_codegen.py` compares the interpreter and actual JVM runtime's precedence for fuel exhaustion and monotonic pointer out-of-bounds. The newly introduced action 6 and the twelve-policy registry are also reflected in golden vectors and JNI classloader tests. The full suite is 116 test methods, verified in two complete non-overlapping groups (67 and 49). This remains entirely off-device.

## Iteration 15 offline composition tests

`tests/test_checked_router_dispatch.py` exercises the new XAX semantic-call
composition's **reference** decision without pretending to run upstream XAX. It
exhausts `4^5 = 1,024` combinations of JNI exception status and four untrusted
integrity statuses from `{0,1,2,255}`, plus malformed inputs and missing or
duplicate direct-call reference edges. The opt-in upstream compiler/writer
workflow remains mandatory for actual XAX verification. Independent test
groups pass 49/49, 45/45, and 30/30 (124 total), with JVM linkage and language
audit separately passed. No Android executable testing has been performed.
