# Testing

There is no test suite in this repository: tests would be a third language. Verification lives with
the toolchains and on the device.

| Layer | How it is checked | Where |
|---|---|---|
| Brainfuck policies | brainfuckC validates every DSO (ELF layout, instruction templates, branch targets) before publishing it | brainfuckC `android_callable_elf_validate63`, `android_callable_code_validate64` |
| Policy behaviour | the module's self-check runs `suppress_video_slot` in YouTube; the settings page shows `settings_snapshot` output | Settings → YouTubeHideAds → *Brainfuck engine* |
| XAX store | XAX verifies the store on open, construct and build; `construct(export_carrier(store))` reproduces its root | XAX `android-libxposed-jvm` branch |
| APK | deterministic: the same store and inputs give the same BLAKE3 | [`evidence/xax_only_20261016/`](../evidence/xax_only_20261016/README.md) |
| On device | load, hooks, Settings row and page, toggles, live removals in the log | same |

## What was lost with the Python suite

The old suite ran every policy against a reference interpreter, exhaustively where the input space
allowed (for example all 243 settings states and all 2,048 SponsorBlock category combinations). Those
results stand for the unchanged `.bf` files and are recorded in [`history/`](history/). New policy
changes need the same proof again, written in Brainfuck or XAX.
