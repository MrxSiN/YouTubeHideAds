<div align="center">

<img src="docs/icon.svg" width="120" alt="YouTube Hide Ads">

# YouTube Hide Ads

**English** · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [Español](README.es.md) · [Português](README.pt.md) · [Русский](README.ru.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md)

**An Xposed module that removes ads from YouTube, with every decision written in Brainfuck and the rest in XAX. Yes, really.**

Ads, sponsored Shorts and promotions are taken out before YouTube shows them, and SponsorBlock segments are skipped.

<br>

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?color=5B3DF5&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Downloads](https://img.shields.io/github/downloads/MrxSiN/YouTubeHideAds/total?color=3DDC84&logo=android&logoColor=fff&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](#requirements)
[![libxposed](https://img.shields.io/badge/libxposed-API%20102-E8A33D?style=for-the-badge)](https://github.com/libxposed/api)

</div>

---

> [!NOTE]
> YouTube renames its obfuscated classes with almost every update. The module finds its targets
> again by shape at each start. When a role is missing or ambiguous, it leaves that feature alone
> rather than guess. See the [compatibility](#compatibility) table for what has actually been tested.

## Why Brainfuck? And what is XAX?

- **Brainfuck decides.** Whether this component is an ad, whether Premium marketing may go, whether
  the player may seek to the end of this sponsor segment, whether a swipe is a brightness change.
  Brainfuck cannot call Android, Xposed, DexKit or JNI. It reads bytes and writes bytes, and the host
  acts only on an exact successful reply.
- **XAX does everything else.** Hooks, DexKit discovery, reflection, the settings page, HTTPS and
  JSON for SponsorBlock are one canonical [XAX](https://github.com/MrxSiN/XAX) semantic store. The
  external XAX compiler turns it into DEX and signs the APK. There is no Java, Kotlin, C, Python or
  shell application source in this repository.

It is not slow either. The nine policies are compiled ahead of time to AArch64 shared libraries by
[BBC](https://github.com/MrxSiN/BBC). There is no interpreter in the APK.

|  | |
|---|---|
| 🧹 **Removed, not hidden** | Ad components are replaced before YouTube lays them out, and sponsored Shorts leave the feed before the pager is built, so there are no blank slots or frozen clips. |
| ⏭️ **SponsorBlock built in** | Prefix lookups with bounded retry/cache, category modes and colors, manual skip/undo, segment creation and voting, exclusions, statistics and settings transfer. |
| 🔎 **Survives renames** | DexKit finds every hook by structure at each start. A missing or ambiguous role installs nothing for that feature. |
| 🧠 **Policy in Brainfuck, compiled** | Nine hand-written programs compiled to native code; packaged policies and SponsorBlock controls are checked at every start. |
| 🛟 **Fails closed** | If a self-check fails, that feature stays off. Network errors and unknown playback types never seek. |
| ⚙️ **Native-looking settings** | Its own **YouTube Hide Ads** section in **You → Settings**, above Account, built from YouTube's own rows, with every switch independent and a Compatibility & diagnostics page. |
| 🎛️ **Player-native SponsorBlock** | A SponsorBlock icon beside autoplay opens the same floating menu as the player's settings gear; segments are colored on the seekbar. |
| 📱 **Cleaner Shorts** | Hide individual Shorts buttons and panels, and move past live streams in the Shorts feed. |
| 👆 **Swipe controls that read at a glance** | Brightness on the left, volume on the right, shown as a pill with an icon, a level and the value. |
| 🌐 **Your language** | Follows YouTube's language: English, 简体中文, 繁體中文, Español, Português, Русский, 日本語, 한국어, Bahasa Indonesia and Bahasa Melayu. |

---

## What it removes

| Group | Setting | Default |
|---|---|---|
| Ads | Video and Shorts ads · Feed and search ads · Premium promotions · Fullscreen promotions | On, under the **Hide ads** master switch |
| SponsorBlock | Sponsor, self-promotion | On |
| SponsorBlock | Interaction, intro, outro, preview, filler, music off-topic | Off |
| Content | Playables (game shelves, cards, Explore entry) | Hidden |
| Feed | Preview videos · Explore more topics · Posts | Hidden |
| Feed | Shorts in feeds | Shown |
| Feed | AI channels · Likely AI channels ([AiSList](https://github.com/Override92/AiSList)) | Off |
| Player | Swipe brightness (left) · Swipe volume (right), fullscreen only | On |
| Player | Force original audio on multi-language videos | On |
| Player | Background playback, including Made for Kids videos | On |
| Shorts | Like, comments, share, remix, save, sound, subscribe, title, suggestions and info panels, paused-overlay buttons | Shown (each can be hidden) |
| Shorts | Skip live Shorts | Off |
| About | Check for updates when YouTube opens | On |

Turning **Hide ads** off does not disable the content and player features. Reload a feed after
changing its switches. Original audio applies to the next track list and respects a manual choice.
Full table: [settings and defaults](docs/README.md#settings-and-defaults).
With **Check for updates** on, the module asks GitHub once each time YouTube starts. If a newer
release exists, a YouTube-style dialog offers **Update**, which opens the release page, or **Later**. To report a
problem, use **About → Compatibility & diagnostics → Report a problem**: it opens a new GitHub issue
with the compatibility report filled in, for you to describe the problem and submit.
Background playback is independent of Hide ads and SponsorBlock. Restart YouTube after changing
its switch to discard native cached capabilities. [Implementation and tested limits](docs/BACKGROUND_PLAYBACK.md).

<details open>
<summary><b>🧱 Where each removal happens</b></summary>
<br>

| Surface | Where | What it does |
|---|---|---|
| **Video ads** | player ad activation and ad layout | Suppresses the ad slot when Brainfuck confirms a structural ad fact and a safe transition. |
| **Feed, search and shopping ads** | the component parser, found by DexKit | Replaces a confirmed paid component with YouTube's own empty component. |
| **Sponsored Shorts** | Shorts response, insertion and pager seed | Removes video/image ad entries together with their tracking data, before the pager exists. |
| **Premium, fullscreen, panels** | offer view, fullscreen dialog, engagement panel by typed identifier | Hides marketing surfaces without touching entitlement or subscription management. |
| **Feed sections, Playables, AI channels** | the same component hook | Removes only the matched section or card; channel rows and playlists stay. |
| **SponsorBlock** | player seek/duration bridges and native seekbar | Bounded prefix retrieval, category modes, colored markers, manual controls and explicit community actions. |

</details>

---

## Status

**v1.2.0** (versionCode 155) supports YouTube 21.43.523, where background playback and SponsorBlock skipping had stopped working. It adds an update check with a YouTube-style dialog (on by default, under About) and a **Report a problem** button that opens a prefilled GitHub issue, and the module is now called **YouTube Hide Ads**. [Device checks](evidence/release_1_2_0_20261030/README.md).

**v1.1.0** (versionCode 153) was the first release since 1.0.0. It adds background playback, the module's own section in YouTube Settings, a Compatibility & diagnostics page, YouTube-style SponsorBlock controls, Shorts component hiding, live-Short skipping, redesigned swipe controls and nine more languages. It is also much lighter on the phone: Brainfuck policy calls no longer reopen the APK, and DexKit results are cached, so YouTube opens about 0.35 s sooner after the first launch. [Device checks](evidence/device_perf_20261028/README.md).

Development builds between releases (111 to 155) are listed in the [changelog](CHANGELOG.md), with evidence for each under [evidence](evidence/README.md).

### Compatibility

Tested on a Pixel 8 Pro with Android 17 and Vector 2.2 (libxposed API 102). Tried another setup? Please open a pull request adding a row.

| YouTube | Module | Status |
|---|---|---|
| 21.43.523 | 1.2.0 | ✅ Working |
| 21.42.243 | 1.1.0 | ✅ Working |
| 21.41.525 | 1.0.0 | ✅ Working |

### Known limits

- Premium, fullscreen and engagement-panel promotions have only been removed in controlled hook tests; naturally delivered ones have not appeared yet.
- Preview-video and Explore-more-topics shelves are matched by their English headings only.
- AI channel lists are community-maintained and can misclassify channels, which is why they default off.
- HTTPS filtering apps (AdGuard and similar) stop SponsorBlock and the update check from connecting. See [SponsorBlock or update check never connects](#sponsorblock-or-update-check-never-connects).
- Background playback needs a YouTube restart after its switch changes and leaves Shorts to YouTube. Bluetooth controls and incoming calls are untested.
- SponsorBlock submission and voting have not been tried against the live server. See [features and limits](docs/SPONSORBLOCK_API_RESEARCH.md).
- Skip live Shorts has not met a real live Short yet; it, the swipe pill and YouTube language switching were checked with development probes.
- Module pages were checked in dark theme only. Light theme, tablets and right-to-left layouts are untested.
- The first launch after a YouTube or module update rebuilds the hook cache and starts about 0.4 s slower.
- arm64-v8a only. Only the setup and YouTube versions above have been tried; LSPatch has not.

Details: [feature coverage](docs/FEATURE_COVERAGE.md) and [compatibility](docs/COMPATIBILITY.md).

## Requirements

| | |
|---|---|
| **Android** | 9.0 (API 28) or newer, arm64 |
| **App** | YouTube (`com.google.android.youtube`) |
| **Framework** | [Vector](https://github.com/JingMatrix/Vector) or LSPosed with libxposed API 102 |
| **Root** | Required by Vector/LSPosed; the module itself requests no permissions |

## Install

```
1. Install the APK from Releases or the Xposed module repository
2. Enable YouTube Hide Ads in Vector or LSPosed, scoped to YouTube
3. Force-stop YouTube once, then open it
```

Get it from [GitHub Releases](https://github.com/MrxSiN/YouTubeHideAds/releases) or
[modules.lsposed.org](https://modules.lsposed.org/module/io.github.mrxsin.youtubehideads). Settings
are under **YouTube → You → Settings → YouTube Hide Ads**. Preferences and AI caches live in
YouTube's own data, so clearing YouTube data resets them.

If you used a development build (`org.youtubehideads.module`), uninstall it first. Your settings
carry over.

The framework log shows what happened, in lines beginning with `YouTubeHideAds:`:

```text
Ad policy self-check passed (70 cases)
SponsorBlock self-check passed (277 cases)
Ad component hook installed
Shorts feed removal hooks installed (paired, insert, response, restore, seed)
Video ad suppressed
```

---

## How it works

```
YouTube process
  XAX module (DEX) ──────────────► Bfp1Bridge.run ──JNI──► lib<policy>.so
  hooks, DexKit roles               input bytes            nine AOT Brainfuck policies
  settings page, HTTPS/JSON              ▲                       │
  typed actions                          │   exact reply only    │
                                         └───────────────────────┘
```

One rule decides where code goes: **if it touches YouTube, Android, the network or JNI, XAX does it;
if it decides whether to act on what XAX found, Brainfuck decides.**

<details>
<summary><b>The Brainfuck policies</b></summary>
<br>

| Library | Decides |
|---|---|
| `settings_snapshot` | ad switch defaults and the master gate |
| `sponsor_settings` | SponsorBlock category defaults and gating |
| `ad_component` | a component from 54 structural facts: suppress or pass |
| `ad_panel` · `ad_fullscreen` | engagement-panel and fullscreen promotions |
| `suppress_video_slot` | a player ad slot, given a safe transition |
| `sponsor_time_window` | whether `start <= current < end`, on three 64-bit timestamps |
| `sponsor_skip_pipeline` | category, generation, window and playback type, then echoes the seek endpoint |
| `and3` | own switch AND fact AND valid context, shared by Premium, Shorts, Playables, swipes, feed sections, AI channels and original audio |

Each call gets a fresh 4,096-byte tape, a 64-byte output buffer and a 2,000,000-loop budget. Byte
layouts are in [`docs/BRAINFUCK_ABI.md`](docs/BRAINFUCK_ABI.md), source conventions in
[`docs/BRAINFUCK_SOURCE_STYLE.md`](docs/BRAINFUCK_SOURCE_STYLE.md).

</details>

<details>
<summary><b>Finding the hooks</b></summary>
<br>

DexKit runs once per process and resolves typed roles by structure: component parser and
serializer, player seek and duration bridges, Shorts response and pager seed, the original-audio
controller. Each role must match exactly one target. Anything missing or ambiguous leaves its feature
off, and the log says so. See [`docs/DEXKIT_RESOLUTION.md`](docs/DEXKIT_RESOLUTION.md).

</details>

<details>
<summary><b>SponsorBlock without leaking what you watch</b></summary>
<br>

Automatic segment retrieval sends a four-hex-digit SHA-256 prefix of the video ID. The response is bounded to
256 KiB, 1,024 records and 100 segments, with 4-second timeouts and redirects disabled. Before a seek,
the main thread checks the player instance, video ID and playback generation again. Live streams and
unknown playback types never seek. Manual submissions and votes send their required video/segment data
and private identity to the selected server. View reporting defaults off; settings exports exclude the
private ID by default. See [`docs/SPONSORBLOCK_API_RESEARCH.md`](docs/SPONSORBLOCK_API_RESEARCH.md).

</details>

---

## Build

There is no build script in this repository. A release is built with external tools:

```text
BBC          source/**/*.bf  ->  lib<policy>.so (AArch64)
AAPT2        source/branding ->  branding.apk (static resources only)
XAX          source/xax/youtubehideads.xax + pinned inputs -> signed APK
```

Every input is pinned by BLAKE3 in the store, so a mismatched input fails the build. Rebuilding
uses the [XAX](https://github.com/MrxSiN/XAX) checkout with its Android libxposed profile (commit `3cca599` or the
compatible branding-v2 snapshot). Steps and identities are in [`docs/BUILD.md`](docs/BUILD.md) and
[`evidence/release_20261018`](evidence/release_20261018/README.md).

Releases are published by hand with the locally built APK. GitHub Actions then checks it
([`release.yml`](.github/workflows/release.yml): package, version, release signing certificate and the
SHA-256 in `RELEASE_NOTES.md`) and mirrors it to
[Xposed-Modules-Repo](https://github.com/Xposed-Modules-Repo/io.github.mrxsin.youtubehideads)
([`xposed-sync.yml`](.github/workflows/xposed-sync.yml)), which feeds modules.lsposed.org.

## Design

```
source/brainfuck/          and3, video slot, SponsorBlock window and pipeline
source/brainfuck-runtime/  settings snapshots, ad component, panel and fullscreen policies
source/xax/                the canonical XAX store: hooks, discovery, settings, network, actions
source/branding/           manifest, icons, shapes and translated strings (static XML)
contracts/                 input byte orders for the component, feed, swipe, AI and audio gates
testdata/                  fixtures recorded for the startup self-checks
evidence/                  dated build identities and device logs
docs/                      architecture, ABI, build, testing and compatibility
```

The layering is in [`docs/ARCHITECTURE_BRAINFUCK_XAX.md`](docs/ARCHITECTURE_BRAINFUCK_XAX.md) and
[`docs/LANGUAGE_BOUNDARY.md`](docs/LANGUAGE_BOUNDARY.md); the full index is [`docs/README.md`](docs/README.md).

## Troubleshooting

| Problem | Try |
|---|---|
| No module log lines | Check that the module is enabled with YouTube in scope, then force-stop YouTube. |
| `UnsatisfiedLinkError` right after an update | Let the install settle, then force-stop and reopen YouTube. The manager can briefly keep the old APK path. |
| A self-check reports `false` | That feature stays off. Report the `YouTubeHideAds:` log lines. |
| A feed switch seems ignored | Reload the feed; removals apply to newly loaded components. |
| Broken after a YouTube update | YouTube may have changed its internal classes. Use **Report a problem** on the Compatibility & diagnostics page, or report the log lines with the YouTube version. |

### SponsorBlock or update check never connects

Segments never appear on the seekbar, or no update is ever offered, and the log shows
`SponsorBlock request error` or `Update check failed` with `NOT_ENOUGH_SCTS`.

An HTTPS-filtering app is intercepting the connection. AdGuard, for example, re-signs secure
traffic with its own certificate, and when that certificate is installed as a system certificate
(such as with the AdGuard Certificate Magisk module), Android sends YouTube's traffic through it.
YouTube enforces Certificate Transparency, which AdGuard's certificate cannot meet, so Android
refuses the connection. The module does not weaken this check.

**Fix:** in AdGuard, open **Settings → Filtering → Network → HTTPS filtering → Exclusions** (the
path can differ by version) and add both domains:

- `sponsor.ajay.app` for SponsorBlock
- `github.com` for the update check

Then force-stop and reopen YouTube. If you use a custom SponsorBlock server, exclude that domain too.

## Credits

| Project | Contribution |
|---|---|
| [DexKit](https://github.com/LuckyPray/DexKit) by LuckyPray | Structural discovery of obfuscated classes and methods (Apache-2.0). |
| [libxposed API](https://github.com/libxposed/api), [Vector](https://github.com/JingMatrix/Vector), [LSPosed](https://github.com/LSPosed/LSPosed) | The hooking API and frameworks the module runs on. |
| [XAX](https://github.com/MrxSiN/XAX), [XAX-MCP](https://github.com/MrxSiN/XAX-MCP), [BBC](https://github.com/MrxSiN/BBC) | External compilers for the store and the policies. |
| [SponsorBlock](https://sponsor.ajay.app) | Community segment data. |
| [Override92/AiSList](https://github.com/Override92/AiSList) | Optional AI-channel lists, CC BY-NC 4.0, not bundled ([aisloplist.com](https://aisloplist.com)). |
| [Morphe Patches](https://github.com/MorpheApp/morphe-patches) | Background behavior and fingerprint reference, adapted natively in XAX; [preserved notice](LICENSES/Morphe-NOTICE.txt). |

Newly authored project material is GPL-3.0-or-later. See [NOTICE](NOTICE) and
[upstream provenance](docs/UPSTREAM_PROVENANCE.md) for third-party terms.

## Disclaimer

Not affiliated with, endorsed by or sponsored by Google LLC or YouTube. Provided for educational and
personal use. YouTube updates may break the hooks without notice.
