# SponsorBlock slider candidate — 2026-10-22

Historical local-build snapshot before phone testing. Code 124 was subsequently rejected;
[code 127 phone acceptance](../sponsorblock_slider_device_20261022/README.md) records the fixes and final result.

1.2.1/code 124 is a locally built candidate. **It has not been installed or tested on the phone.**
The user requested finishing the code and testing on the phone later. The last device-accepted
build remains [1.2.0/code 123](../sponsorblock_ui_20261022/README.md); its screenshots and runtime
results do not validate this candidate.

## Change

All four color controls call one XAX factory, `sb_ui_slider`. It inflates the module's static
SeekBar layout, track and thumb resources and applies YouTube's active foreground color, with
a translucent inactive track. The layout has a rounded 16 dp track, a 4 × 44 dp handle with
6 dp spacing on each side, a 4 dp endpoint marker and a 48 dp touch target. RTL mirrors the track
and marker together. Android retains drag, keyboard, focus and accessibility behavior; keyboard
adjustment changes a component by one. Existing ARGB conversion, opacity, presets and save paths
are preserved.

The geometry reference is **the bundled `Widget.Material3.Slider` style in the copied YouTube
21.42.243 APK**, not a live screenshot comparison. [Reference tokens](reference.json) record
the source APK/dump digests and inspected values. Other shared SponsorBlock page, preference,
button and text helpers keep the accepted 1.2.0 presentation.

Sizing is declared in XML to preserve the Android 9 minimum: the alternative public
[ProgressBar sizing methods](https://developer.android.com/reference/android/widget/ProgressBar#setMaxHeight(int))
require API 29. No rendering dependency or conventional-language application source was added.

## Local verification

[Build identity](build.json), [preservation](preservation.json), [toolchain](toolchain.json)
and [verification](verification.json) distinguish static checks from runtime acceptance.

The candidate packages the original 636 startup cases and 64 live-context UI cases (the previous
28 plus 36 slider checks). **Neither suite has run on code 124.** New cases check the handle
dimensions, insets, native range, one-step keyboard increment, split track and required track layers
for each of the four sliders. The first-page check hook remains reachable.

## Deferred device checks

Install this exact APK, restart YouTube and confirm 636 startup plus 64 UI cases pass. Compare
the controls with current YouTube in light/dark themes, portrait/landscape and RTL. Exercise
touch, keyboard/TalkBack, endpoints, opacity, preset selection and saved-color round trips.
Verify track clipping, handle gaps and endpoint visibility on the actual device before accepting
the visual match. Production community writes are outside these UI checks.
