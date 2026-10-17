# Upstream provenance and terms

This guide describes the recorded sources used through build 77, not a fresh upstream-version or
license audit. Exact local compiler/input identities are in
[current toolchain evidence](../evidence/ai_audio_branding_20261018/toolchain.json).
No conventional-language compiler or application source is vendored in this repository.

## XAX and XAX-MCP

The application host is an independently authored XAX semantic store. Current builds use an isolated
external extraction of compiler/src from XAX commit
`0876b591f39908e98aa31f746ae2e26bb88c837e`, with local branding-v2 changes to xax_construct.py and
xax_android_libxposed_jvm.py. Their hashes and temporary path are recorded. The active D:/GitHub/XAX
checkout was not changed by the branding task; the isolated snapshot was changed. The clean base
commit alone cannot rebuild the branded store. Preserve the compatible snapshot.

The earlier integration recorded XAX-MCP commit
`e3f450fa08c6bb2aa0032d59a3007f8c465138a8` and existing local compiler modifications. Those identities
are historical, not proof that a clean or newer MCP checkout supports branding-v2. The external
compiler supplies generic APK/DEX/signing support, not YouTube feature decisions.

Initial research at XAX revision `9e44eedfc241d25bb5062b38af105f75234000e2` found no root LICENSE
and repository metadata with no identified license. That dated observation does not assert current
upstream licensing or redistribution permission. Compiler source is not redistributed here.

## brainfuckC

The external original checkout was D:/GitHub/brainfuckC; later dynamic-build evidence uses
D:/GitHub/BrainfuckCC. The inspected notice is MIT, copyright 2026 brainfuck-native contributors;
a copy is in [LICENSES/brainfuckC-MIT.txt](../LICENSES/brainfuckC-MIT.txt).
BF-owned compiler stages generate the AArch64 policy libraries. The external generic C JNI bridge
supplies loading and byte transport; it contains no application classification policy.

Initial native tests used bootstrap.run_policy_native.PolicyCompiler and seed.exe. Production
DSO builds use android_device_stages/android_dynamic_callable59 with BF stages on the arm64 phone.
These are different historical backends; do not describe the initial seed test as the current build.
No compiler source or seed executable is bundled as project implementation. Generated libraries
and the external bridge are pinned binary inputs in the APK.

## Morphe behavior references

Most inspected sources are pinned to
[e5464395441e916b643af4e2175c4e253e6df487](https://github.com/MorpheApp/morphe-patches/tree/e5464395441e916b643af4e2175c4e253e6df487):

- HideAdsPatch, AdsFilter, shared fullscreen/engagement helpers and fingerprints.
- SponsorBlock and channel whitelist patch/fingerprint sources.
- ContextInterface, LayoutComponentsFilter, ShortsFilter and HorizontalShelvesFilter.
- AiSListFilter, AiSListRequester and AiSListPatch.
- Shared/YouTube ForceOriginalAudioPatch and shared audio-track fingerprints.

The earlier Playables/swipe pass read moving-main LayoutComponentsFilter,
SwipeControlsConfigurationProvider, ClassicSwipeController and PlayerType. Those reads are behavior
references, not pinned implementation dependencies. No Java/Kotlin implementation was copied.
Runtime discovery, BF authorization and Android effects were independently authored. The inspected
Morphe repository uses GPL-3.0 and Section 7 notices; preserve applicable notices for any future
actual incorporation. [Inspected subset](MORPHE_AD_PATCH_INVENTORY.md).

Generic preview discussion in [Morphe issue 2746](https://github.com/MorpheApp/morphe-patches/issues/2746)
did not justify hiding all horizontal shelves. The Pixel supplied the actual preview root/title.
YouTube DEX supplied the independently discovered typed component and SABR audio roles.

## AiSList data

Optional lists come from [Override92/AiSList](https://github.com/Override92/AiSList), paths
AiSList/aislist_blocklist.txt and AiSList/aislist_warnlist.txt. Their inspected headers specify
**CC BY-NC 4.0**. Settings credit **Override92 and contributors** and link to
[aisloplist.com](https://aisloplist.com) for lists/reports. No list data is bundled with the app;
user-enabled public downloads are cached in YouTube's private preferences. No report is submitted.
The lists are mutable community data and can misclassify channels. Their terms are separate from
the project's source license.

## Other dependencies and services

- DexKit 2.3.0: prebuilt DEX/native input; inspected upstream terms identify LGPL-3.0.
- flatbuffers-java 23.5.26 and kotlin-stdlib 2.4.10: prebuilt third-party DEX inputs, not authored app code.
- libxposed API 102 / Vector 2.2: actual tested framework on the Pixel; no other framework is certified.
- SponsorBlock: read-only privacy-prefix API; no copied client implementation, votes or submissions.
  [Recorded request behavior](SPONSORBLOCK_API_RESEARCH.md).
- Android AAPT2 36.0.0: compiles static branding resources only. D8 was used for third-party DEX.
- ThreadsHideAds and TwitterHideAds: locally inspected branding style. The YouTube shield/strike
  vector is independently drawn; no sibling runtime source is included.

Newly authored project material is GPL-3.0-or-later. This does not replace separate third-party
terms or grant rights to external compiler source. See [NOTICE](../NOTICE), [build requirements](BUILD.md)
and [dated evidence](../evidence/README.md) for the recorded scope.
