# YouTubeHideAds — Iteration 14 implementation and verification

Date: 2026-10-15. This iteration advances the **offline executable Brainfuck foundation**, not the Android runtime. No Android APK, Vector attachment, YouTube interception, DexKit resolution, or SponsorBlock HTTP/player operation was produced.

## Delivered implementation

- Added **`sponsor_time_window.bf`**, an annotated, strict eight-command Brainfuck policy. It consumes 24 bytes: three nonnegative signed-long-compatible millisecond timestamps, little-endian `start`, `current`, and `end`. It implements `start <= current < end` **by executing Brainfuck**. Its only results are `00` (PASS) and `06` (TIME_WINDOW_VALID); it never issues a seek.
- Registered stable ABI feature `0x0404`, allowed action `06`, exact input-length validation derived from the 24 executable commas, signed-long domain checks for all three timestamps, and source-generated golden binary vectors.
- Added the off-device `checked_sponsor_time_chain` validator. When *authentic* compiled Brainfuck results are provided, it requires matching generations, verbatim 64-bit endpoints (`window[16:24] == sponsor[21:29]`), and the follow-on SponsorBlock `valid_segment_window` gate to match the Brainfuck time-window action. It cannot authenticate player sources or perform a seek.
- Expanded both the standalone AOT JAR and the inline Brainfuck router to **twelve** programs, including the 24-byte timestamp input. Each program's deterministic registry now records its fuel limit. The router uses the maximum of its inlined policies' fuel limits.
- Added optional **header-only `# @fuel 2000000`** with strict canonical integer validation. Most policies retain the 100,000-command default. This 64-bit arithmetic policy uses a bounded two-million-command allowance and still enforces 4096 tape cells and 64 output bytes.
- Reduced long JVM method size by combining contiguous same-direction pointer commands. Before their combined displacement, the emitted JVM code checks whether resource exhaustion or tape bounds would have failed first, retaining the original error precedence. Bounded-region error handlers were tuned for large programs; baseline mode also applies mandatory size-saving transformations when needed. No program feature decisions were rewritten in Java or Python.

## Executed tests

| Stage | Result | Evidence |
| --- | --- | --- |
| Automated test group 1 | **67/67 passed** | `YouTubeHideAds_iteration14_tests_group1.log` |
| Automated test group 2 | **49/49 passed** | `YouTubeHideAds_iteration14_tests_group2.log` |
| Total complete, nonoverlapping test suite | **116/116 passed** | Both logs together, covering all 19 test modules |
| Timestamp windows and signed-long edge cases | **Passed** | Interpreter, baseline AOT, optimized AOT, inline router |
| Long pointer-run fuel/bounds ordering | **Passed** | Interpreter vs executed JVM classes |
| JNI classloader/desktop invocation | **Passed** | Existing JNI regression suite with all twelve policies |
| Normal/optimized standalone JAR construction | **Passed** | `YouTubeHideAds_iteration14_build.log` |
| Normal/optimized router construction | **Passed** | `YouTubeHideAds_iteration14_build.log` |
| Source/JAR byte-exact linkage | **Passed** | `scripts.verify_linkage` |
| Language-boundary audit | **Passed** | `toolchain.brainfuck.audit` |
| External XAX, D8, Android SDK, ADB | **Unavailable** | Environment preflight at end of build log |
| Android ART, libxposed, DexKit and YouTube | **Not executed** | No compatible runtime/APK generated |

The monolithic suite wrapper exceeded its command execution limit in some attempts. The two groups were then run independently and successfully cover all 19 discovered test modules without overlap. Neither an interrupted wrapper nor a synthetic DEX fixture is counted as Android execution.

## Deterministic compiled artifacts

- Baseline policy JAR SHA-256: `e5c9680bc0cbeb65b7b01cef9e934ea1d0427df416cdc3fe03ed95d72cce48d6`
- Optimized policy JAR SHA-256: `5e5be3dd984a98ddb73a7e5a9e6568cf19ac9f4a71b9e35b49caef4c0d930bc3`
- Baseline and optimized inline router JAR SHA-256: `4df9da181ad805450211f606b3d61f5a8e035ecfe3fce73d6f2d8a8e8ee2472b`

Large-program compaction is mandatory in both router modes; identical router hashes are **not** independent binary implementations. The standalone policy JARs do differ between modes. The generated `dispatch_all.run([B)[B` class still approaches Java's 65,535-byte per-method limit, so arbitrary future growth will need verified method segmentation or a more scalable backend.

## Boundary and remaining blockers

The timestamp validator has no knowledge of YouTube objects; it accepts only syntactically validated host-provided millisecond values. It cannot independently authenticate a SponsorBlock video ID, the player generation, live state, current position, or the active seek target. `checked_sponsor_time_chain` is off-device tooling; a production XAX caller must obtain and verify these facts, invoke the compiled Brainfuck, and handle Java exceptions, lifetimes and race conditions. `checked_reply` **still denies every positive seek** without a real XAX Android host.

The exact pinned external XAX compiler (`9e44eedfc241d25bb5062b38af105f75234000e2`), Android SDK/D8/ADB, and a suitable Vector/libxposed target are absent here. The XAX redistribution license remains unresolved. Therefore, this iteration **does not supply a deployable APK** and makes no claim that YouTube advertisements were suppressed.

## Next priority

Build and verify the real canonical XAX Android host with device-valid classloader acquisition, exception-state handling and a `dispatch_all.run([B)[B` call. Connect its actual SponsorBlock player-context evidence to the time-window and seek policies. Pass real ART, libxposed, DexKit and functional YouTube tests before describing the module as usable.
