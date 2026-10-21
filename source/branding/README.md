# Static branding resources

App title: YoutubeHideAds. The shield/strike and black/white styling follows the local ThreadsHideAds
and TwitterHideAds projects; this YouTube mark is independently drawn. The same foreground serves
adaptive and monochrome icons. No launcher Activity or extra permission is introduced.

These XML files are declarative resource data. All application behavior remains in the canonical XAX
store and Brainfuck policies. Android AAPT2 compiles this folder to the branding.apk input; the
external XAX branding-v2 profile pins that input's BLAKE3 digest, substitutes the module versionCode
for manifest placeholder 1, and packages/signs it with XAX-generated DEX. See [build instructions](../../docs/BUILD.md).

The description is “Minimal LSPosed module that hides YouTube ads and unwanted feed content.”
The manifest declares package io.github.mrxsin.youtubehideads, minSdk 28 and targetSdk 37. Placeholder
versionCode 1 is not the final module version; the current tested build supplies 127.
[Packaged resource proof](../../evidence/ai_audio_branding_20261018/apk-resources.txt) and
[current branding evidence](../../evidence/ai_audio_branding_20261018/README.md) record the tested result.

The static resource archive also carries the shared SponsorBlock slider layout, track and thumb.
Its dimensions follow the modern slider tokens bundled in YouTube 21.42.243. XAX supplies the
current YouTube theme colors and retains native SeekBar interaction. XML sizing supports API 28
without calling API 29 ProgressBar sizing methods. This is declarative resource data, not an
additional implementation language. [Resource and phone checks](../../evidence/sponsorblock_slider_device_20261022/README.md) record accepted dark/light rendering.
