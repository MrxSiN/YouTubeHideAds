# Build

The repository holds Brainfuck (`.bf`) and one XAX store (`source/xax/youtubehideads.xax`). It has no
build script. Three outside toolchains do the work, each from its own repository.

| Toolchain | Where | Role |
|---|---|---|
| brainfuckC | `D:\GitHub\brainfuckC` | Brainfuck → AArch64 `bfc_call_v1` shared objects; the `Bfp1Bridge` JNI bridge |
| XAX | `D:\GitHub\XAX`, branch `android-libxposed-jvm` | the `android-libxposed` profile: JVM → DEX, manifest, metadata, APK v2 signing |
| XAX-MCP | `D:\GitHub\XAX-MCP`, branch `android-libxposed` | the tools an agent uses: open, build, export, construct |

## 1. Brainfuck policies

brainfuckC's DSO compiler is a chain of Brainfuck stages. On a host without Linux x86-64 it builds
those stages for arm64 and runs them on a phone over ADB:

```bash
python -m bootstrap.android_device_stages --serial SERIAL --annotated D:/Android/AndroidStudioProjects/YouTubeHideAds/source/brainfuck-runtime/settings_snapshot.bf -o build/inputs/libsettings_snapshot.so
```

Run it from the brainfuckC checkout for `settings_snapshot`, `ad_component`
(`source/brainfuck-runtime/`), `suppress_video_slot` and `suppress_premium_upsell`
(`source/brainfuck/ads/...`). `--annotated` drops whole-line `#` comments first. The first run
compiles 17 stages on the phone (about two minutes); later runs reuse them.

## 2. One-time inputs

Put these in one directory, the build-inputs root (any names; XAX matches them by BLAKE3):

- the four policy `.so` files from step 1;
- `libbrainfuckc_bridge.so`, built from brainfuckC `tools/android_bfp1_bridge/bfp1_jni_bridge.c` with
  the NDK (`aarch64-linux-android28-clang -shared -fPIC -O2 -Wl,-z,max-page-size=16384 ... -ldl`);
- `libdexkit.so` from the DexKit 2.3.0 AAR (`jni/arm64-v8a/`);
- the DexKit, flatbuffers-java 23.5.26 and kotlin-stdlib 2.4.10 classes as one `classes.dex`, made once
  with D8 (`--release --min-api 28`). This is the only third-party bytecode; XAX does not transcode it.

The store names each input's digest, so a different file is a build error, not a different APK.
The current digests are in [`evidence/xax_only_20261016/`](../evidence/xax_only_20261016/README.md).

## 3. Build the APK

Register XAX-MCP with the inputs root, the private signing capability and an output directory:

```bash
xax-mcp --store-root D:/Android/AndroidStudioProjects/YouTubeHideAds/source/xax --android-inputs D:/Android/AndroidStudioProjects/YouTubeHideAds/build/inputs --android-signing C:/Users/SiN/.xax/signing/youtubehideads.cap --output-root D:/Android/AndroidStudioProjects/YouTubeHideAds/build/out
```

Then, as tool calls:

1. `xax_workspace` `{"action": "open", "store": "youtubehideads.xax"}`
2. `xax_build` `{"workspace": WS}` — the signed APK
3. `xax_export` `{"kind": "artifact", "handle": ART, "name": "YouTubeHideAds.apk"}`

The signing capability never enters the store or the repository; only the certificate's SHA-256 does.

## 4. Change the module

Transactions edit what exists. To add calls or functions:

1. `xax_export` `{"kind": "carrier", "handle": WS, "name": "carrier.json"}` — tooling, not source
2. edit the carrier
3. `xax_construct` with the edited carrier
4. `xax_build`, test on a device
5. `xax_export` `{"kind": "store", ...}` over `source/xax/youtubehideads.xax`, and commit the store

Bump `version_code` in the carrier's `android` record for each install; Vector reloads on it.

## 5. Install

```bash
adb install -r build/out/YouTubeHideAds.apk
```

Enable it in Vector, scoped to YouTube, and force-stop YouTube once.
