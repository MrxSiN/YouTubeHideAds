# SponsorBlock slider phone acceptance — 2026-10-22

**1.2.1/code 127 is installed and passed targeted checks** on the Pixel 8 Pro, Android 17/API 37,
YouTube 21.42.243 and Vector 2.2/API 102. The installed APK digest matches the tested artifact.
[Identity](build.json), [verification](verification.json), [preservation](preservation.json)
and [toolchain](toolchain.json) describe this exact build.

## Findings and fixes

The initial [local candidate, code 124](../sponsorblock_slider_20261022/README.md), crashed because
YouTube's package visibility prevented `createPackageContext` from finding the module. The final
XAX host retains the framework-provided `getModuleApplicationInfo()` result and loads module
resources through `PackageManager.getResourcesForApplication(ApplicationInfo)`. It constructs the
native SeekBar using YouTube's Context and XML dimension attributes, then applies the module's
drawables separately. No package-name visibility lookup, hidden API or additional library is used.

The binary XML parser now advances past START_DOCUMENT before reading the root tag. The color
picker finalizes keyboard increments after setting the 0–255 range, because Android resets them
when `setMax` runs. The inactive shape is opaque before tinting, so its 20% theme tint is applied
once. [Rejected candidates](candidates.json), [resource crash](crash124.log),
[parser crash](crash125.log) and [failed keyboard check](keyboard126.json) retain the diagnosis.

## Passed

- 636 startup cases and 64 live-context UI cases in both accepted dark and light processes:
  [dark runtime](runtime127.log), [confirmed light runtime](runtime127-light-confirmed.log).
- All four touch controls reach 0 and 255. Each remains a native 48 dp-high accessible SeekBar.
  Tab navigation reaches Red; Right changes 169 to 170.
  [Interactions](slider-interactions.json).
- Purple preserves 100% opacity. Saving stores `#FFA970FF`; reopening restores the exact RGB and
  opacity, and the saved value survives a process restart. [Round trip](save-roundtrip127.json).
- Real dark and light rendering, including active/inactive tracks, vertical handles, gaps,
  endpoint markers, labels, presets and Save action. [Theme measurements](themes127.json),
  [dark picker](dark-picker127.png), [light picker](light-picker127-confirmed.png),
  [native YouTube light settings](native-settings-light127.png).
- Original **Use device theme** selection and initial absence of module preferences restored.
  Only the known test preference keys were removed after their identities/values were checked;
  later light checks required no further preference removal. [Restoration](restoration127.json).
- APK signature and API-102 static acceptance; all 11 native libraries, third-party DEX and
  signer pins preserved. Existing startup-check graphs and ARGB/save callbacks are unchanged.

The first screenshot named `light-picker127.png` in the raw Logs folder remained dark during
the theme transition and was **not accepted** as light visual evidence. The confirmed light
screenshot above was inspected against YouTube's own white settings screen. Historical failures
and interim results do not count toward acceptance.

## Limits

Landscape, RTL, TalkBack, Android 9 and other devices were not tested. No production SponsorBlock
POSTs were sent, and this slider session does not certify new naturally delivered ad cases.
Raw phone captures and logs are under
`D:/Android/AndroidStudioProjects/Logs/YouTubeHideAds_Slider_20261022`.
YouTube is left open with the original settings restored.
