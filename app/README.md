# Android module

Application ID: `org.youtubehideads.module`. Scope: `com.google.android.youtube`.
The manifest declares **no Activities, services or launcher entry**. Configuration
belongs inside YouTube; no standalone manager app will be built.

`toolchain/xax/module_graph.py` constructs the actual XAX platform callbacks.
`toolchain/xax/module_build.py` verifies their canonical store and compiles the
managed program, emits the fixed libxposed lifecycle forwarder, links the
Brainfuck router through D8, and produces `build/module/YouTubeHideAds-debug.apk`.
libxposed API 102 is compile-only and checked against the upstream artifact pin.

On the tested YouTube 21.41.525 / Vector 2.2 device, open **YouTube → Settings →
YouTubeHideAds** in the toolbar. The page belongs to YouTube's Activity and
returns to it through the page button or system Back.

This build implements the actual module/page integration and an in-process BF
engine self-check. Advertisement suppression and SponsorBlock are not connected.
See `../docs/history/ITERATION18_REPORT.md` for commands, proof boundaries and compatibility.
