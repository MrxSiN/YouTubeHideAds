# Actual Android/YouTube compatibility matrix

| Android | YouTube | Framework | ABI | Module load | Ads hidden | SponsorBlock |
| --- | --- | --- | --- | --- | --- | --- |
| 17 / API 37, Pixel 8 Pro | 21.41.525 | Vector 2.2 / API 102 | arm64-v8a | PASS in YouTube; Settings toolbar/page and BF self-check | Not implemented/tested | Not implemented/tested |

The version-code-21 module is scoped only to YouTube and is left installed.
Three page open/close cycles, system Back, one toolbar entry and process survival
passed on the listed build. This establishes page integration only; it does not
establish ad removal, playback hooks, DexKit resolution or future compatibility.
See `history/ITERATION18_REPORT.md` and `evidence/module_20261016/device-result.json`.
