# XAX canonical semantic programs

The actual module program is authored in `toolchain/xax/module_graph.py` and
verified at `build/module/module.xax-store`. Its Hooker and page click callbacks
run inside YouTube. `toolchain/xax/module_build.py` emits the fixed libxposed
lifecycle forwarding ABI and packages the generated classes with the BF router.
There is no module Activity; the page is owned by YouTube. See
`ITERATION18_REPORT.md` for the current code-generation and device evidence.

The current managed-call program is authored through the pinned XAX object
constructors in `toolchain/xax/managed_dispatch.py`. A real verified binary
store is generated at `build/xax-managed-dispatch/dispatch.xax-store`, alongside
the compiler-issued `dispatch.jar`. Build and device evidence is recorded in
`evidence/xax_20261016/`; reproduction commands are in `ITERATION17_REPORT.md`.
The source graph binds one managed external call to the genuine BF router.
It is not the framed production host or a YouTube hook.

The lifecycle program has its own canonical store at
`build/xax-smoke/lifecycle-smoke.canonical-store`. Its no-op module was loaded
on Vector in a controlled target. The following early notes are historical.

This directory is not an XAX source-code program. XAX has no ordinary textual `.xax` source language; canonical semantic graph objects/stores must be constructed by the upstream verified toolchain. See `docs/XAX_ANDROID_INTEGRATION.md` for the exact pin, current blocker, and the rule against inventing text syntax or misleading JSON stand-ins. No canonical host has yet been generated or committed.

Iteration 2 adds `contracts/bf_host_v1.md` and a passing off-device AOT/JVM wire conformance suite. The real XAX implementation must be authored via supported graph-edit/store transactions, not by copying this Python test codec or manufacturing a JSON graph as source. The pinned XAX GitHub repository has no recorded license grant; no code was vendored.

## Iteration 3

`toolchain/xax/smoke_build.py` now provides a pinned **external-XAX-dependent** canonical-semantic-object build adapter for a controlled no-op lifecycle smoke module. The **authoritative XAX program store has not been generated yet**, since the pinned external compiler checkout is absent in this environment. No `.xax` text files should be added as source substitutes. See `docs/XAX_SMOKE_BUILD.md`; no Android host logic or feature decisions are implemented here.
