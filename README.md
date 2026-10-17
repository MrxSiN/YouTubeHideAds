# YoutubeHideAds

A libxposed module that removes YouTube ads and unwanted feed content, skips SponsorBlock segments,
and adds fullscreen brightness/volume controls and original-audio selection. Application behavior
is implemented in **Brainfuck and XAX**. Static XML branding and JSON contracts/fixtures are data;
there is no Java, Kotlin, C, Python or shell application source in this repository.

**Current build: 1.0.0, versionCode 100.** Tested on Pixel 8 Pro, Android 17/API 37,
YouTube 21.41.525 and Vector 2.2/libxposed API 102. All **531 startup checks pass**.
Other YouTube versions and devices have not been certified.

## Features

| Feature | Behavior and verification |
| --- | --- |
| Video, feed/search and shopping ads | Live suppression recorded on the tested Pixel |
| Sponsored Shorts | Video/image ad entries removed before pager creation; paired tracking data remains aligned and video frames advance |
| Premium, fullscreen and panel promotions | Controlled real-view/hook tests pass; naturally delivered positives remain unverified |
| SponsorBlock | Privacy-prefix retrieval and guarded seeks; sponsor and self-promotion enabled by default |
| Playables | Removes game shelves/cards and the Explore entry; toggle defaults on |
| Feed sections | Preview videos, Explore more topics and posts default hidden; feed Shorts defaults visible |
| AI channels | Independent high-confidence and medium-confidence AiSList filters; both default off |
| Fullscreen swipes | Left brightness and right media volume; separate toggles default on |
| Original audio | Prefers the original track on a new multi-language video; defaults on |

Reload a feed after changing its switches. The feed Shorts toggle retains the Shorts tab and player.
Sponsored Shorts removal does not advance the pager. AI filtering targets supported video/Shorts
cards, preserving channel rows and playlists. Original audio respects a manual language choice on
the same loaded track list.

[Settings and defaults](docs/README.md#settings-and-defaults) ·
[Feature coverage](docs/FEATURE_COVERAGE.md) · [Compatibility](docs/COMPATIBILITY.md)

## Install

Use an arm64 Android device with a libxposed API 102 framework. Android API 28 is the declared
minimum; the tested setup is the Pixel above. The module requests no Android permissions and has
no launcher Activity.

1. Install `YouTubeHideAds-v1.0.0.apk` from the [GitHub release](https://github.com/MrxSiN/YouTubeHideAds/releases)
   or the [Xposed module repository](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads).
2. Enable **YoutubeHideAds** in Vector, scoped to `com.google.android.youtube`.
3. Force-stop YouTube after installation settles, then reopen it.
4. Open **YouTube → You → Settings → YoutubeHideAds**.

Preferences and AI caches are stored in YouTube's own data. Clearing YouTube data resets them.
An update can briefly leave Vector using an old APK path; allow installation to settle and
force-stop/reopen YouTube if native loading fails immediately after an update.

## Implementation and build

YouTube hooks supply validated facts through the XAX host. Compiled Brainfuck policies authorize
removal, gestures or seeks; XAX accepts only an exact successful reply before acting. The canonical
store contains **123 functions**, **11 native library paths** and a pinned branding input.
There are **9 authored Brainfuck files**, one per shipped policy library, and **one canonical XAX store**. Seven gates share `and3.bf`.

External brainfuckC compiles policies to AArch64 shared libraries. XAX generates application DEX,
packages libxposed metadata and signs the APK. Android AAPT2 compiles only static branding resources;
D8 was used once for prebuilt third-party dependencies, not application implementation.

**Rebuilding requires the retained external XAX snapshot with the branding-v2 extension.** A clean
checkout of its base commit is insufficient. The application repository has no build script and
does not vendor compiler source or a private signing capability.

[Build instructions](docs/BUILD.md) · [Architecture](docs/ARCHITECTURE_BRAINFUCK_XAX.md) ·
[Language boundary](docs/LANGUAGE_BOUNDARY.md) · [Documentation index](docs/README.md)

## Evidence and limits

[Release 1.0.0 evidence](evidence/release_20261018/README.md) and [build 77 evidence](evidence/ai_audio_branding_20261018/README.md) includes artifact identities,
AI off/on search results, Hindi versus English-original audio, advancing video frames, restored
preferences and 531 startup checks. The [dated evidence index](evidence/README.md) separates current
results from older milestones and rejected experiments.

Explore more topics passed a controlled actual-hook test; Home did not deliver a natural topics
shelf. Preview/topics headings currently require English. A separate warnlist-positive live card,
other YouTube versions, real multi-pointer swipe cases and fixed-volume routes remain unverified.
Community AI lists can misclassify channels; the filters default off. SponsorBlock has no retry,
cross-video cache, submissions or colored seekbar. Full Morphe parity is not implemented.

## Credits and terms

- [Morphe Patches](https://github.com/MorpheApp/morphe-patches): behavior reference; no implementation copied.
- [Override92/AiSList](https://github.com/Override92/AiSList): optional lists credited to Override92
  and contributors under CC BY-NC 4.0; [lists and reports](https://aisloplist.com).
- [libxposed](https://github.com/libxposed/api), [Vector](https://github.com/JingMatrix/Vector) and
  [DexKit](https://github.com/LuckyPray/DexKit): hooking framework and structural discovery.
- [XAX](https://github.com/MrxSiN/XAX), [XAX-MCP](https://github.com/MrxSiN/XAX-MCP) and
  [brainfuckC](https://github.com/MrxSiN/brainfuckC): external build toolchains.
- [ThreadsHideAds](https://github.com/MrxSiN/ThreadsHideAds) and
  [TwitterHideAds](https://github.com/MrxSiN/TwitterHideAds): branding style and module approach.

Newly authored project material is GPL-3.0-or-later. See [NOTICE](NOTICE) and
[upstream provenance](docs/UPSTREAM_PROVENANCE.md) for third-party scope and terms.
The module is not affiliated with Google LLC. YouTube updates may break its hooks.
