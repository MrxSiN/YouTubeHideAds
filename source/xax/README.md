# XAX source

youtubehideads.xax is the canonical binary semantic store for the Android host. Device-tested
1.2.1/code 127 contains 263 functions and 11 native library paths plus a pinned static resource input.
Package io.github.mrxsin.youtubehideads; scope com.google.android.youtube; API 102.
All 636 startup and 64 live-context UI checks pass on the Pixel in dark and light contexts.
[Exact build, phone checks and limits](../../evidence/sponsorblock_slider_device_20261022/README.md).

It owns libxposed lifecycle, ad and SponsorBlock hooks, sponsored Shorts pre-pager removal,
Playables/feed/AI filters, fullscreen controls, original-audio selection, settings and bounded network
transport. New AI/audio functions reuse the existing native AND3 gate under separate semantic paths.
SponsorBlock separates retrieval/cache, playback authorization, rendering, settings and explicit
community actions into typed functions. Category data and settings keys are shared by their callers.
Static branding XML is data; it introduces no conventional-language implementation source.

The module record pins the certificate, third-party DEX, native libraries and branding digest.
The signing capability remains external. JSON carriers under ignored build/port are editing transport,
not source. The external compiler requires the branding-v2 extension; see
[BUILD.md](../../docs/BUILD.md) and [exact tested identity](../../evidence/sponsorblock_slider_device_20261022/README.md).

Current [settings/defaults](../../docs/README.md#settings-and-defaults),
[native contracts](../../docs/BRAINFUCK_ABI.md) and [historical evidence index](../../evidence/README.md)
separate current runtime behavior from the removed offline codec. Documentation edits do not change
the store or extend its device certification.
