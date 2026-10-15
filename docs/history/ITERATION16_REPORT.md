# BrainfuckC integration and Android diagnosis — 2026-10-16

All twelve existing annotated Brainfuck policies compiled using the external
compiler at `D:\GitHub\brainfuckC` and executed successfully on the connected
Pixel 8 Pro: **4,463 native/reference comparisons passed**. This is a native
policy milestone; the project still has no working YouTube/Xposed module.

The requested principles were applied through separate source-validation,
compiler-adapter and device-verification responsibilities, reuse of the existing
parser/interpreter, and a small upstream API call. No new runtime feature layer,
dependency, backend framework or speculative SOLID hierarchy was introduced.
The attachment was background context; the existing project was preserved.

## Executed checks

- BrainfuckC: twelve callable AArch64 ELF images, 620–5,652 bytes each.
  Windows execution uses upstream `seed.exe` to execute upstream BF compiler
  stages through `PolicyCompiler`; native code generation stays upstream-owned.
- NDK 28.2.13676358: test-only C harness built for Android API 28 with
  `-Wall -Wextra -Werror`, then run via the requested platform-tools ADB.
- Pixel 8 Pro: Android 17, API 37, `arm64-v8a`; YouTube 21.41.525 installed.
  Exact native output matches cover all twelve policies, including 2,048
  category cases, 2,080 combined SponsorBlock cases, 256 seek cases and seven
  timestamp boundaries. The complete breakdown and hashes are in
  `evidence/brainfuckc_20261016/device-result.json` and `policies.json`.
- Full Python/JVM regression suite: **130 discovered, 117 passed, 13 skipped**.
  Skips are the existing Linux/GCC/JNI desktop harness on Windows; they are not
  counted as device or JNI passes. Full transcript is saved with the evidence.
- Language-boundary audit: twelve BF policy owners; no application-language
  fallback detected. The new native harness remains under `tests/`.

## Diagnosed and corrected

Existing JVM test/link helpers used `:` classpath separators, incompatible with
Windows drive paths. They now use `os.pathsep`. Generated router source now
uses explicit LF output so its byte-level provenance verification works on
Windows. The test fixture restores the same canonical bytes after tampering.
Fake D8 test tools now have a Windows launcher, and the language audit uses
platform-independent paths and recognizes the explicit device diagnostic.

ADB initially could not access its normal user directory from the sandbox;
device commands succeeded with host access. No framework settings, installed
apps or YouTube data were changed. Test artifacts remain in the dedicated
`/data/local/tmp/youtubehideads_brainfuckc` directory.

## Remaining limits

The selected compiler is bounded to 4,096 RLE records, 255 bracket levels and
1 MiB source input. Its loop-gas semantics differ from interpreter/JVM
per-command fuel. The combined BF router and newer dynamic DSO path were not
compiled. Shell `mmap`/native execution does not establish Bionic `dlopen`,
ART/JNI, app linker namespaces, XAX integration, a working APK, Xposed hooks,
live SponsorBlock seeking or ad removal. The compiler source checkout was used
externally without changes; MIT provenance and notice are saved.

Reproduction commands: `docs/BRAINFUCKC_ANDROID.md`.
