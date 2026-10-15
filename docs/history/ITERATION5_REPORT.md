# YouTubeHideAds — Iteration 5 evidence

## Scope

This iteration turns the previously action-only SponsorBlock Brainfuck eligibility policy into a **real binary-output policy**: `authorize_seek.bf` reads six validated Boolean gates and eight binary bytes representing a 64-bit segment-end position (milliseconds, little-endian). It emits either `00` (PASS) or `04` plus those eight position bytes (SEEK_PLAYER). This is executable 8-command Brainfuck; annotations have no execution semantics. The output is not a precomputed constant from a host-side skip implementation.

All other eight `.bf` programs, Android D8 linkage adapter, and XAX smoke build adapter remain as before. The former code cannot yet execute in an Android module.

## Verification

- Exhaustive six-gate authorization cube (64 combinations) across seven boundary and ordinary endpoints.
- Genuine binary output for eight-byte values containing NUL, 0xff and different high-order bytes.
- Source interpreter and **directly compiled JVM** agreement (optimized and unoptimized; through both direct JVM tests and host-ABI framing tests).
- Absent/invalid/oversized destinations, non-Boolean gate inputs, spoofed endpoint, wrong generation, incomplete result and unexpected action payload rejected by off-device typed contract.
- Positive seek outcomes remain blocked by `SEEK_NOT_DEPLOYABLE` or `SEEK_RUNTIME_HOST_ABSENT` irrespective of a correct endpoint. No player action is issued.
- Original eight policies remain in the build; all nine compile from source in both modes.

## What is **not** implemented

A genuine XAX-authored Android runtime dispatcher, live YouTube player state, raw segment time comparisons, overlap merging, SponsorBlock HTTPS/network/JSON, category toggles, DexKit member discovery, libxposed hook lifecycle, Android DEX conversion with real D8, or a running APK. All would require separate implementation and device validation. No host-side code path is substituted for these.

## Environment and license

The local Python/JDK test toolchain is available. The pinned external XAX compiler checkout, D8, Android SDK, ADB and Android device are unavailable; `git ls-remote` fails DNS resolution in this container. The XAX project has no established redistribution grant here. No XAX code is vendored; no XAX-produced APK is redistributed.

Run `./scripts/build_fresh.sh` for the final machine-readable logs and checked-in test vectors. The log and file digest manifest in the packaged release record execution evidence.

## Observed full-run result

Command: `./scripts/build_fresh.sh` from the Iteration 5 repository. Exit status: `0`.

- `python -m unittest discover -s tests`: **47 tests passed**.
- Original and optimized source-attributed JVM JARs independently verified: **9/9 policies** each.
- Original AOT JAR SHA-256: `c3ad887e1513151f7a2a24832033f364c69788d4378e1caa5ca9a9aea873cd26`.
- Optimized AOT JAR SHA-256: `687db78b963a4e16e15a4c71f722f809630680b98fcd3f748a3e8e497e467b2d`.
- Android preflight: `BLOCKED`, ten explicit prerequisites or unimplemented integrations; no Android test ran.

Do not interpret any of the 47 offline tests as proof of SponsorBlock integration with an actual YouTube process.
