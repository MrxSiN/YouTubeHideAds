# Build

Release **1.1.0 (versionCode 153)** was built with the same `D:/GitHub/XAX` `3cca599` compiler SDK and a
rebuilt `libbrainfuckc_bridge.so` (source and flags in the [build 153 record](../evidence/device_perf_20261028/build.json)).
Development build 132 was built with `D:/GitHub/XAX` at `3cca599`, which now
contains the Android libxposed profile. Its `xax_construct.py` and `xax_android_libxposed_jvm.py`
are byte-identical to the compiler recorded for build 131; the separate `D:/GitHub/XAX-libxposed-jvm`
checkout no longer exists. XAX-MCP 0.5.0 does not yet implement the Android/JVM target, so the
compiler SDK is used directly. [Toolchain record](../evidence/ui_redesign_20261027/toolchain.json).

Development build **131**'s compatible external JVM SDK,
input digests, signed APK and scoped device checks are recorded in
[background playback evidence](../evidence/background_playback_20261027/README.md).
Development build 127:
[Build/input identities](../evidence/sponsorblock_slider_device_20261022/build.json),
[compiler hashes](../evidence/sponsorblock_slider_device_20261022/toolchain.json) and
[phone verification](../evidence/sponsorblock_slider_device_20261022/README.md) identify the exact accepted APK.
Compiler and native/DEX inputs are unchanged; the static archive includes shared slider XML.
These records take precedence over older milestones. Application source is BF plus one XAX store; branding XML is static data. There is no
repository build script.

For the background feature, the original temporary snapshot retains only some caches. The existing
`D:/GitHub/XAX-libxposed-jvm` checkout at `52e880895d0f6e57113cf0e74ededf2b7b25cc40`
supports the branding-v2 profile and round-trips the baseline store to the exact same root. It was
used without compiler edits; current source hashes are in the new toolchain record. The active
`D:/GitHub/XAX` and native `D:/GitHub/XAX-MCP` paths are not replacements for that JVM profile.

The designated `D:/GitHub/BBC/build/bbc.exe` compiled the authored AND3 policy as a standalone
Windows executable, with all eight inputs passing. Its current shared-library path needs a
65,536-cell tape and ignores the budget; this app retains the pinned 4,096-cell `bfc_call_v1`
library and bridge. Only BF annotations change. All 11 packaged native paths and the third-party
DEX pin remain unchanged; the branding digest intentionally changes for the development version
and bundled Morphe notice. No ABI, native dependency or signing-capability migration is performed.

## Required external tools

| Tool | Recorded location / role |
| --- | --- |
| [BrainfuckCC](https://github.com/MrxSiN/BrainfuckCC) (formerly brainfuckC) | Checkout D:/GitHub/BrainfuckCC (the original D:/GitHub/brainfuckC checkout produced the earliest builds); BF stages produce AArch64 policy libraries and its generic JNI bridge supplies transport |
| XAX | D:/GitHub/XAX is the active checkout; build 77 uses the isolated snapshot described below |
| XAX-MCP | D:/GitHub/XAX-MCP; external workspace/carrier/build/export tooling, when configured with the compatible XAX profile |
| Android SDK | AAPT2 build-tools 36.0.0 and android-37.0/android.jar for static branding only |
| Android platform-tools | D:/Android/platform-tools/adb.exe for arm64 compiler stages and device checks |

The retained XAX snapshot starts from commit
`0876b591f39908e98aa31f746ae2e26bb88c837e` and adds the **branding-v2 extension** to
`xax_construct.py` and `xax_android_libxposed_jvm.py`. Its path and used-file hashes are in the
current toolchain record. The active checkout removed its Android profile during earlier work;
do not assume it or a clean base checkout can build this store. Preserve the compatible snapshot.
Re-extracting the base commit alone does not reproduce the extension. No compiler source or private
signing capability is vendored here.

The 2026-10-21 inspection also checked `D:/GitHub/Ballsdeep_Brainfuck_Compiler` and
`D:/GitHub/XAX-MCP`. The current compiler uses a BFX/native path with a 65,536-cell ABI; this app's
pinned JNI inputs use `bfc_call_v1` and 4,096 cells. The current XAX checkout has no compatible JVM
module backend, and the native MCP construct operation is unavailable. This release therefore uses
the retained compatible SDK and unchanged native inputs. [Inspection identities](../evidence/sponsorblock_ui_20261022/toolchain.json).

Branded metadata uses `android-libxposed-jvm-module-v2` followed by NUL. The module record includes
an optional 32-byte branding digest and input closure. Unbranded v1 identities remain unchanged;
an older compiler must reject the branded store rather than silently discard branding.

## Policy inputs

Run the external compiler from its own checkout, keeping generated inputs under ignored
`build/inputs`. The recorded dynamic backend is `bootstrap.android_device_stages`, with whole-line
annotations stripped by `--annotated`. Example invocation from the external checkout:

```text
python -m bootstrap.android_device_stages --serial SERIAL --annotated D:/Android/AndroidStudioProjects/YouTubeHideAds/source/brainfuck-runtime/settings_snapshot.bf -o D:/Android/AndroidStudioProjects/YouTubeHideAds/build/inputs/libsettings_snapshot.so
```

Compile the nine `.bf` files under `source/` (`and3.bf` to `liband3.so`). All seven AND3 gates call
that one library; after editing `and3.bf`, verify all eight Boolean inputs through the packaged JNI boundary.

On hosts without Linux x86-64, BF compiler stages run on the arm64 phone over ADB. Those external
tools may use Python/C; neither their source nor generated conventional-language source belongs in
this application repository.

## Other pinned inputs

- From build 135, `libbrainfuckc_bridge.so` is a drop-in rebuild that caches resolved libraries and
  uses a native tape; its external source and flags are in the [build 135 record](../evidence/device_perf_20261028/build.json).
  Earlier builds used the generic bridge below.
- Generic `libbrainfuckc_bridge.so`, built externally from BrainfuckCC's JNI bridge with the Android
  NDK for AArch64/API 28, 16 KiB maximum page size and `-ldl`.
- DexKit 2.3.0 arm64 `libdexkit.so` from its AAR.
- A prebuilt third-party `classes.dex` combining DexKit, flatbuffers-java 23.5.26 and kotlin-stdlib
  2.4.10. D8 was used once with release/min-api 28 for these dependencies; application DEX is XAX-generated.
- Static `branding.apk`, compiled below. It is an input archive, not the installable module.

Every input is pinned by BLAKE3 in the canonical store. The toolchain record lists the input digests;
`build.json` lists final packaged native SHA-256 values. A mismatched input must fail the build.

## Branding input

Create ignored `build/branding` and `build/inputs` directories. Run from the application root with
AAPT2 36.0.0 available:

```text
aapt2 compile --dir source/branding/res -o build/branding/compiled.zip
aapt2 link -I C:/Users/SiN/AppData/Local/Android/Sdk/platforms/android-37.0/android.jar --manifest source/branding/AndroidManifest.xml -o build/inputs/branding.apk build/branding/compiled.zip
```

The external profile permits only AndroidManifest.xml, resources.arsc and res/*, rejects duplicate
entries and uncompressed totals above 2 MiB, validates binary manifest chunk bounds, and replaces the
single integer versionCode placeholder with the module record's value. The versionName stays in the
static manifest; update and repin the branding archive when changing it. XAX then packages its DEX,
metadata and native inputs and signs the final APK. The static manifest adds no launcher or permissions.

## Construct, build and export

The canonical source is `source/xax/youtubehideads.xax`. Ignored JSON carriers are editing transport.
The tested external APIs are `xax_construct.construct`, `xax_compiler.StoreReader` / `write_store`
and `xax_android_libxposed_jvm.build_module`. Configure external tooling to import the compatible
snapshot and resolve the pinned input closure. Signing uses the external private capability; never
copy it into the repo, carrier, evidence or logs.

With a compatible XAX-MCP server, the equivalent flow is workspace open → carrier export/edit →
construct → build → artifact/store export. Compatibility of a different server/compiler version is
not established by the local build evidence. The module configuration is `package.android` in the
construct carrier; bump its `version_code` for each device install.

After a behavioral edit, verify semantic construction, native policy/source correspondence and
input digests, then test the candidate on the device. Promote the exact tested store and signed APK.
Do not substitute temporary probe builds or rebuild with different inputs after device acceptance.
The release 1.1.0/code 153 build has 342 functions; development build 127 had 263 functions, 11 native paths, no topics probe or automatic Shorts navigation,
and packages 636 startup checks plus 64 UI checks when the first SponsorBlock page opens. Both suites pass in the accepted dark and light device processes. Store/APK identities belong in the dated build record.

## Install and validate

```text
D:/Android/platform-tools/adb.exe -s SERIAL install -r YouTubeHideAds-v1.1.0.apk
```

Enable **YouTubeHideAds** in Vector for YouTube, allow the package update to settle, then force-stop
and reopen YouTube. Verify the installed version/digest, startup checks and targeted behavior.
A transient old APK-path cache occurred after build 74; a later force-stop/reopen resolved it.
Do not uninstall or clear user data to work around an unverified older version.

See [testing](TESTING.md), [current evidence](../evidence/sponsorblock_slider_device_20261022/README.md), and
[dated milestones](../evidence/README.md). Documentation edits alone do not require a new build/install.
