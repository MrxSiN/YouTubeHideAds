# Settings page — device session 2026-10-16

Pixel 8 Pro, Android 17, Vector 2.2 (libxposed API 102), YouTube 21.41.525.
Module `org.youtubehideads.module` 0.3.0-dev, versionCode 26, debug key,
APK SHA-256 `a3b164d6dfbf78bbd66b6dc68dd42bc3cd62522c5e7bab7b92e422f39a7249d7`.

| Check | Result |
|---|---|
| Entry row in YouTube Settings list (icon, title, ripple, theme tint) | PASS, `settings-entry.png` |
| Entry only on the top-level list, not on subpages | PASS (General opened, no row) |
| Page opens full screen with toolbar, sections, title/summary/switch rows | PASS, `settings-page.png` |
| Row tap and switch tap both toggle and persist | PASS, `youtubehideads.xml` held `video_ads=false`, `fullscreen_promotions=false` |
| Reopened page reads state back through `settings_snapshot.bf` | PASS, `settings-toggled.png` |
| Reset to defaults clears preferences and closes the page | PASS, `<map />` |
| Back arrow and Android Back close the page | PASS |
| YouTube process survives every step | PASS, same PID |
| Brainfuck router self-check inside YouTube | PASS |
| Hooks honour the switches with a live ad | NOT TESTED: no ad was served while testing |

Defaults and the master gate are Brainfuck (`source/brainfuck-runtime/settings_snapshot.bf`,
243/243 preference states checked against the reference interpreter in
`tests/test_settings_snapshot.py`). Full suite: 140 tests, 17 skipped (GCC JNI and
device-only), 0 failures, with the Android Studio JBR on `PATH`.
