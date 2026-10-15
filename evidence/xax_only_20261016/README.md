# Brainfuck + XAX only build — device session 2026-10-16

Pixel 8 Pro, Android 17, Vector 2.2 (libxposed API 102), YouTube 21.41.525.
Module `org.youtubehideads.module` 0.4.0-dev, versionCode 27.

## What built it

| Step | Tool | Output |
|---|---|---|
| Brainfuck → AArch64 `.so` | brainfuckC `bootstrap.android_device_stages` (Brainfuck stages run on the phone) | four policy libraries |
| JNI bridge | brainfuckC `tools/android_bfp1_bridge` (NDK) | `libbrainfuckc_bridge.so` |
| Third-party DEX | D8 once over DexKit 2.3.0 + flatbuffers + kotlin-stdlib | `classes.dex` |
| Module | XAX `android-libxposed` (branch `android-libxposed-jvm`), through XAX-MCP `xax_build` | signed APK |

Store `source/xax/youtubehideads.xax`: root `5ebdd37b9f69626002179ad16d248f4e9e685f703e63bcd4dcdbef1e469d0378`.
It round-trips exactly: `construct(export_carrier(store))` has the same root.
APK BLAKE3 `1a21fbeb7a50abf12c97274526f25f2f943cb08f59d2dd64fcaac0f88c864b54`, identical from the
direct XAX call and from XAX-MCP. Signed by certificate SHA-256
`3c4644a021b4e1994d4f31c36d41854f86bf6a471a8f3d667fbfc62b7e42926b`.

Declared inputs (BLAKE3):

| Input | BLAKE3 |
|---|---|
| `libad_component.so` | `5a3df82b9778bb5c9b771921ff4b7f7b01f569ea2fc7c1dc1540b24d5da937ab` |
| `libbrainfuckc_bridge.so` | `679a9d8af91999cdd556d9032596686774e853186ebcc30d1167b5042390a319` |
| `libdexkit.so` | `69e142100d6599c48b7315941ce4c3fea72784a55f6ed013177efb5ec015a159` |
| `libsettings_snapshot.so` | `174f1a556d05d0f30319ecfc436e26e5dfc323435d3f1dce29373c8b3ded0ac3` |
| `libsuppress_premium_upsell.so` | `3c31b9d7b4ca123f12c8ed714309763484587b8ed10907680ad8e5061dc1c598` |
| `libsuppress_video_slot.so` | `34cb3b55ba4d10a0ff20c71e8edc2ed5ab2f0bdb239d2e67d41fc280f0ff9c22` |
| DexKit `classes.dex` | `07f22ff643ac6c650036550355084f3b02034493201a2e5a8c8e487a393d4b90` |

## What ran

| Check | Result |
|---|---|
| Vector loads the module; five ad hooks, lifecycle hook, Settings row | PASS |
| All six native libraries load from the APK (`System.load`) | PASS, no `UnsatisfiedLinkError` |
| Brainfuck self-check through `Bfp1Bridge` → `libsuppress_video_slot.so` | PASS |
| Settings page reads switches from `libsettings_snapshot.so` | PASS, `settings-page.png` |
| Toggle persists, page reopens with the stored state | PASS |
| Live removal while a video played | `Video ad suppressed`, `Ad component replaced` (`module.log`) |
| YouTube process survived every step | PASS, same PID |

The log lines are the first-occurrence messages the hooks print; they prove the hooks fired and the
Brainfuck policy authorized suppression. The screen was off when they fired, so there is no
screenshot of the missing ad.
