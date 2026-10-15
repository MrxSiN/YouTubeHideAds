# BrainfuckC native policy check — 2026-10-16

The optional compiler adapter uses the external checkout at
`D:\GitHub\brainfuckC`. All twelve current YouTubeHideAds policies compiled
through its supported `bootstrap.run_policy_native.PolicyCompiler` API and ran
on a Pixel 8 Pro, Android 17 / API 37, ARM64. **4,463 native/reference
comparisons passed.** YouTube 21.41.525 was installed during diagnosis; no
YouTube behavior or Xposed hook was exercised.

The attached `YouTubeHideAds.md` was used as background requirements. Its
instruction to start from an empty directory was not applied to this existing
project. The existing JVM compiler and XAX work remain available.

## Responsibilities

- `toolchain/brainfuck/brainfuckc.py` uses the existing strict annotated parser,
  passes only its eight-command stream to the external compiler, validates the
  callable ELF layout, and publishes each output atomically. The existing parser
  remains the single authority for annotation stripping. Source, compiler and
  upstream BF stage hashes are recorded in `policies.json`.
- Upstream Brainfuck stages own native code generation. On Windows the upstream
  API executes those stages through its existing `seed.exe`; this is the bounded
  policy backend, not the newer Linux-only dynamic DSO backend.
- `scripts/verify_brainfuckc_device.py` builds test inputs, calculates reference
  outputs with the existing interpreter, checks current source/artifact hashes,
  and transports the corpus and artifacts through ADB.
- `tests/android/brainfuckc_probe.c` is a test-only buffer/ABI harness. It maps
  the unchanged ELF read/execute and calls its entry at offset 128. It contains
  no feature decisions, BF parser or compiler and is not shipped in an app.

This keeps source validation, compilation, transport and feature policies
separate without adding a backend framework or new application abstraction.

## Reproduce on Windows PowerShell

Python 3.11+ must be available as `python`. JDK `java` and `javac` are needed
for the existing JVM regression suite. In this session Python 3.12.14 and
Android Studio's JBR 25.0.3 were used.

```powershell
python -m toolchain.brainfuck.brainfuckc --checkout D:\GitHub\brainfuckC

$ndk = 'C:\Users\SiN\AppData\Local\Android\Sdk\ndk\28.2.13676358'
& "$ndk\toolchains\llvm\prebuilt\windows-x86_64\bin\clang.exe" `
  --target=aarch64-linux-android28 `
  "--sysroot=$ndk\toolchains\llvm\prebuilt\windows-x86_64\sysroot" `
  -std=c11 -Wall -Wextra -Werror -O2 -fPIE -pie `
  tests\android\brainfuckc_probe.c -o build\brainfuckc\probe

& D:\Android\platform-tools\adb.exe devices -l
python -m scripts.verify_brainfuckc_device `
  --adb D:\Android\platform-tools\adb.exe --serial DEVICE_SERIAL `
  --probe build\brainfuckc\probe

python -m unittest discover -s tests -v
python -m toolchain.brainfuck.audit
```

The verifier copies only test files into
`/data/local/tmp/youtubehideads_brainfuckc`. It does not install an APK, change
framework settings, clear device logs, or launch/stop YouTube. A new batch
removes prior success manifests before compiling. A new device run removes its
prior result before checking inputs. Failed builds preserve the previous ELF
for an individual policy; consumers must require the complete current manifest.

## Evidence and limits

Saved evidence: `evidence/brainfuckc_20261016/`. Rebuilt artifacts and the
comparison corpus are in `build/brainfuckc/`; the compiler manifest records all
twelve ELF hashes. Category coverage is exhaustive over 256 enablement masks
and eight selections; other policy coverage includes all Boolean combinations,
four seek endpoints and seven timestamp boundary cases. This is not exhaustive
timestamp-domain coverage or invalid-input fuzzing of the native backend.

The selected upstream backend has limits of 4,096 RLE records, 255 bracket
levels and 1 MiB transported source. All twelve individual policies fit. The
combined router was not compiled with this backend. Native loop gas is counted
by upstream compiled-loop semantics; it is not equal to this project's
per-command interpreter/JVM fuel. No application host should substitute these
artifacts without defining and testing that execution-limit boundary.

These files are **callable ELF images**, not `dlopen`-ready shared libraries,
JNI libraries, DEX or an APK. Mapping and executing them in Android shell does
not establish Bionic dynamic loading, ART/JNI integration, an app linker
namespace, a working XAX host or ad removal. No production compiler path was
replaced. Upstream compiler files were used externally and were not modified.
