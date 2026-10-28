# Documentation

Current release: **YouTubeHideAds 1.1.0, versionCode 153** (tag `v1.1.0`).
[Build identity](../evidence/device_perf_20261028/build.json) owns artifact digests and counts;
[phone evidence](../evidence/device_perf_20261028/README.md) owns its scoped validation claims.
Development builds 111 to 152 between 1.0.0 and 1.1.0 are named by build number.
Dated evidence describes its named build, not the current checkout.

| Guide | Contents |
| --- | --- |
| [Feature coverage](FEATURE_COVERAGE.md) | What ships, live versus controlled proof, omissions |
| [Compatibility](COMPATIBILITY.md) | Tested environment and remaining limitations |
| [Build](BUILD.md) | External compilers, branding-v2 requirement, inputs and install |
| [Architecture](ARCHITECTURE_BRAINFUCK_XAX.md) | Responsibilities, callbacks, state and request bounds |
| [Language boundary](LANGUAGE_BOUNDARY.md) | BF/XAX implementation versus static data and external tools |
| [Native ABI](BRAINFUCK_ABI.md) | Packaged policies, byte layouts and authorization |
| [BF source style](BRAINFUCK_SOURCE_STYLE.md) | Annotations, commands and runtime limits |
| [DexKit resolution](DEXKIT_RESOLUTION.md) | Structural anchors, typed roles and failure behavior |
| [Testing](TESTING.md) | Startup checks, fixtures and device acceptance |
| [SponsorBlock](SPONSORBLOCK_API_RESEARCH.md) | Retrieval, playback controls, community actions and settings transfer |
| [Background playback](BACKGROUND_PLAYBACK.md) | Runtime gates, independent switch, policy, upstream research and limits |
| [Morphe inventory](MORPHE_AD_PATCH_INVENTORY.md) | Inspected references and implemented equivalents |
| [Provenance](UPSTREAM_PROVENANCE.md) | References, mutable lists, licenses and compiler history |
| [Evidence index](../evidence/README.md) | Dated milestones and rejected experiments |

## Settings and defaults

| Group | Setting | Default | Ad master dependency |
| --- | --- | --- | --- |
| Ads | Hide ads | On | Master switch |
| Ads | Video and Shorts ads | On | Yes |
| Ads | Feed and search ads | On | Yes |
| Ads | Premium promotions | On | Yes |
| Ads | Fullscreen promotions | On | Yes |
| SponsorBlock | Enable skipping | On | Yes |
| SponsorBlock | Sponsor, self-promotion | On | Yes, and SponsorBlock enabled |
| SponsorBlock | Interaction, intro, outro, preview, filler, music off-topic | Off | Yes, and SponsorBlock enabled |
| Content | Hide Playables | On | No |
| Feed | Hide preview videos | On | No |
| Feed | Hide Explore more topics | On | No |
| Feed | Hide posts | On | No |
| Feed | Hide Shorts in feeds | Off | No |
| Feed | Hide AI channels | Off | No |
| Feed | Hide likely AI channels | Off | No |
| Player controls | Swipe brightness | On | No |
| Player controls | Swipe volume | On | No |
| Player controls | Force original audio | On | No |
| Player controls | Background playback | On | No |
| Shorts | Hide like, comments, share, remix, save, sound, subscribe, title, suggestions/info panels, paused-overlay buttons (ten switches) | Off | No |
| Shorts | Skip live Shorts | Off | No |

Settings and pages follow YouTube's language: English, 简体中文, 繁體中文, Español, Português, Русский, 日本語, 한국어, Bahasa Indonesia and Bahasa Melayu. The diagnostics page is under About → Compatibility & diagnostics.

Ad and SponsorBlock defaults/master gating are computed by their BF snapshots. Independent content
and player preferences use XAX/Android defaults and final BF authorization. Turning Hide ads off
does not disable those independent features. Settings and AI caches live in YouTube's private data.
Reset uses the existing preference reset; clearing YouTube data also loses preferences/caches.
Reload feeds for removal changes. Original audio applies to a fresh track list/controller, normally
the next video; a manual choice on the current loaded list remains usable.
Background playback reads its independent saved switch on each eligible call. Restart YouTube
after changing it to discard native cached capabilities. [Implementation and limits](BACKGROUND_PLAYBACK.md).

## Source and contracts

[Canonical XAX source](../source/xax/README.md) · [Static branding](../source/branding/README.md)

- [Component facts](../contracts/ad_component_inputs.json)
- [Feed sections](../contracts/feed_section_inputs.json)
- [Swipes](../contracts/player_swipe_inputs.json)
- [AI channels](../contracts/ai_channel_inputs.json)
- [Original audio](../contracts/original_audio_inputs.json)
- [Background playback](../contracts/background_playback_inputs.json)

## Documentation changes

Keep current behavior in these guides and exact identities in dated build records. Label live
positives, controlled hook tests and fixtures separately. Preserve old logs, hashes and measurements.
Documentation-only edits do not rerun or extend device certification. Removed conventional-language
sources and history documents remain available in Git history.
