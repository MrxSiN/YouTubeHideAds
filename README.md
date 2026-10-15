<div align="center">

# YouTube Hide Ads

**An Xposed module for removing ads and skipping sponsors in YouTube, with its policy written in Brainfuck and its host written in XAX. Yes, really.**

The decisions are Brainfuck. The Android glue is a verified semantic graph. Nobody wrote the Java.

<br>

[![Release](https://img.shields.io/github/v/release/MrxSiN/YouTubeHideAds?include_prereleases&color=FF0000&label=release&style=for-the-badge)](https://github.com/MrxSiN/YouTubeHideAds/releases)
[![Android](https://img.shields.io/badge/Android-9.0%2B-3DDC84?logo=android&logoColor=fff&style=for-the-badge)](#requirements)
[![libxposed](https://img.shields.io/badge/libxposed-API%20102-E8A33D?style=for-the-badge)](https://github.com/libxposed/api)

</div>

---

> [!WARNING]
> **Work in progress.** Video ads and feed ad components are removed on a real device, and the
> settings page works. Shorts, search and shopping have policies but no hooks yet, and SponsorBlock is
> not connected. See the [compatibility](#compatibility) table for what has actually been tested.

## Why Brainfuck?

Surely nobody would write the decision logic of an ad blocker in Brainfuck.

Brainfuck was selected for its rich ecosystem, mature package manager, excellent Android SDK
bindings, comprehensive type system, first-class coroutine support, and famously pleasant
debugging experience.

Just joking.

The real idea is the one [ThreadsHideAds](https://github.com/MrxSiN/ThreadsHideAds) proved out and
[TwitterHideAds](https://github.com/MrxSiN/TwitterHideAds) and
[GmailHideAds](https://github.com/MrxSiN/GmailHideAds) followed: **keep every decision about
YouTube out of the Android code.** Which slot is an ad, which shelf is paid, which sponsor category
may be skipped, whether the playhead is inside a segment — that is the part that has to change when
YouTube changes, and it lives in one place that cannot touch anything else.

Brainfuck enforces that boundary, because it literally cannot call Android, Xposed or JNI. It reads
bytes and writes bytes.

This one goes a step further than its siblings. There is no Java host either. The Android side —
the package guard, the libxposed hooks, DexKit, the settings entry, the page — is one verified
[XAX](https://github.com/MrxSiN/XAX) program. The repository holds exactly two languages: `.bf`
files and one `.xax` store. No Java, Kotlin, C, Python or shell, not even a build script. The
compilers live in their own repositories and are welcome to be written in whatever they like.

|  | |
|---|---|
| 🧠 **Policy in Brainfuck, compiled** | Hand-written eight-command programs, compiled to AArch64 shared objects by [brainfuckC](https://github.com/MrxSiN/brainfuckC), whose compiler is itself Brainfuck. No interpreter in the APK. |
| 🧬 **Host in XAX** | One canonical XAX store. XAX lowers it to DEX, writes the manifest and signs the APK itself: no D8, no AAPT2, no apksigner. |
| 🚪 **No launcher** | The module opens its page from inside YouTube Settings. No companion app, no manager Activity. |
| 🛟 **Fails closed on seeks, open on content** | A malformed or stale request never seeks the player and never hides anything. |
| 🧪 **Proven identical** | Every policy is checked against the reference interpreter, exhaustively where the input space allows. 4,463 comparisons passed on an arm64 phone. |

---

## What it will remove

Each feature is one Brainfuck program in `source/brainfuck/`. Video slots, Premium upsells and the
component classifier (`brainfuck-runtime/ad_component`) ship as compiled libraries behind
DexKit-resolved hooks; the rest wait for theirs.

| Program | Decides |
|---|---|
| `ads/player/suppress_video_slot` | whether a player ad slot is suppressed |
| `ads/feed/suppress_feed_item` | whether a home feed item is an ad |
| `ads/feed/suppress_search_result` | whether a search result is an ad |
| `ads/shorts/suppress_shorts_slot` | whether a Shorts slot is an ad |
| `ads/promotions/suppress_premium_upsell` | whether a Premium upsell is hidden |
| `ads/shopping/suppress_paid_shelf` | whether a paid product shelf is hidden |
| `ui/collapse_filtered_container` | whether an emptied container collapses |
| `resolver/reject_ambiguous` | whether a DexKit match is trusted or the feature stays off |
| `sponsorblock/select_sponsor_category` | which of eight categories may auto-skip |
| `sponsorblock/sponsor_time_window` | whether `start <= current < end`, in 64-bit signed milliseconds |
| `sponsorblock/authorize_seek` | whether a seek is allowed, and to where |
| `sponsorblock/sponsor_skip_pipeline` | category and seek in one call, no host-computed permission in between |

Behaviour follows [Morphe Patches](https://github.com/MorpheApp/morphe-patches), reimplemented at
runtime. No Morphe source is copied.

---

## Status

**v0.4.0-dev.** Brainfuck and XAX only. The repository lost every line of Python, Java, C and shell;
the module is one XAX store plus the `.bf` programs. XAX builds the APK itself (DEX, manifest,
signature), the policies are Brainfuck compiled to AArch64 by brainfuckC, and the two meet through
one JNI call. Built and run on a Pixel 8 Pro: hooks install, the page works, and YouTube logged a
suppressed video ad and a replaced ad component while a video played
([evidence](evidence/xax_only_20261016/)).

**v0.3.0-dev.** Settings, built to look like YouTube's own. **YouTubeHideAds** is a row in the
Settings list, with a YouTube outline icon, and opens a full-screen page laid out like *General*:
section headers, title-and-summary rows, switches on the right, the theme's own colours.

<p align="center"><img src="docs/images/settings.png" width="300" alt="Settings page"></p>

The switches are stored in YouTube's own preferences. Defaults and the master switch are not host
code: `settings_snapshot.bf` turns the stored bits into the effective switches, and every hook reads
its `enabled` byte from that snapshot. The snapshot is rebuilt when a YouTube screen gains focus or a
switch changes, never on a hook's hot path.

Five DexKit-resolved hooks install on YouTube 21.41.525. SponsorBlock networking and the player
seek hook are next.

Earlier milestones, from the first JVM-only policies onwards, are kept in
[`docs/history/`](docs/history/).

### Compatibility

Each row is one setup somebody has actually run. If you try another, please open a pull request
adding a row.

| Device | Android | Framework | YouTube | Module | Result | Tester | Date |
|---|---|---|---|---|---|---|---|
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.41.525 | 0.4.0-dev (code 27) | XAX-built APK, brainfuckC policies: hooks and page work, Brainfuck self-check and snapshot pass, toggles persist; `Video ad suppressed` and `Ad component replaced` logged during playback ([evidence](evidence/xax_only_20261016/)) | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.41.525 | 0.3.0-dev (code 26) | Settings row and page; switches persist, reset works, Back and arrow close; one row only, none on subpages; 5 ad hooks installed; BF self-check passes. No ad served, so no live removal yet ([evidence](evidence/settings_20261016/)) | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.41.525 | 0.2.0-dev (code 21) | Loads in YouTube; Settings entry, page, Back and duplicate checks pass over three cycles; BF router self-check passes. No ad removed — not wired yet | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | — (ADB shell) | — | — | 12 policies via native BrainfuckC: 4,463 comparisons against the reference interpreter | @MrxSiN | 2026-10 |

### Known limits

- **No SponsorBlock, and no Shorts, search or shopping hooks yet.** The page says so for SponsorBlock.
- Live removals are proven by the hooks' log lines, not yet by a before/after screenshot.
- The XAX `android-libxposed` profile and the XAX-MCP tools that build this module live on branches
  of those repositories until they are merged.
- brainfuckC's DSO compiler runs its stages on an arm64 phone when the build host is not Linux x86-64.
- Settings live in YouTube's own preferences. libxposed RemotePreferences need a module-side writer,
  and this module has no Activity of its own. Clearing YouTube's data resets them.
- The Settings row sits above YouTube's list rather than inside it, so it stays at the top while the
  list scrolls.
- The XAX toolchain is pinned, not vendored; it has no recorded license, so it is not
  redistributed here.

## Requirements

| | |
|---|---|
| **Android** | 9.0 (API 28) or newer |
| **App** | YouTube (`com.google.android.youtube`) |
| **Framework** | [Vector](https://github.com/JingMatrix/Vector) or another libxposed API 102 framework |
| **Root** | Required by Vector; the module itself asks for none |

Built against the modern [libxposed API](https://github.com/libxposed/api)
(`io.github.libxposed:api`), not the legacy `de.robv.android.xposed` bridge.

## Install

There is no release yet. Build the APK (below), then:

```
1. Install the APK
2. Enable YouTube Hide Ads in Vector, scoped to YouTube
3. Force-stop YouTube once, then open it
4. YouTube → Settings → YouTubeHideAds
```

---

## How it works

```
YouTube / Android
  → libxposed hook (package guard, Activity focus, five DexKit-resolved ad hooks)
  → XAX host (one verified store: hooks, settings row and page, DexKit queries)
  → raw input bytes
  → Bfp1Bridge.run → lib<policy>.so  (brainfuckC: Brainfuck compiled to AArch64)
  → raw output bytes
  → XAX host accepts exactly the authorized reply, then acts
```

One rule decides where code goes: **if it needs Android, Xposed, DexKit or the network, XAX does it;
if it decides what to do with what XAX read, Brainfuck decides.**

<details>
<summary><b>The Brainfuck core</b></summary>
<br>

Every `.bf` file carries a header of `# @feature`, `# @abi`, `# @inputs`, `# @outputs` and
`# @cells` metadata. A line starting with `#` is a comment; every other line may hold only the eight
commands and whitespace. brainfuckC drops the comment lines and compiles what is left, so a
comment-only change never changes the compiled output.

Each policy that ships is its own shared object exporting `bfc_call_v1`: 8-bit wrapping cells, a
4,096-byte tape, zero at end of input, a bounds-checked pointer, a 64-byte output buffer and a
loop-entry budget. Any nonzero status reaches XAX as an empty reply, and an empty reply never matches
an authorized action. Shipped today: `settings_snapshot`, `ad_component`, `suppress_video_slot` and
`suppress_premium_upsell`.

Style rules are in [`docs/BRAINFUCK_SOURCE_STYLE.md`](docs/BRAINFUCK_SOURCE_STYLE.md).

</details>

<details>
<summary><b>The XAX host</b></summary>
<br>

XAX programs are semantic graphs, not text. [`source/xax/youtubehideads.xax`](source/xax/) is the
module's canonical store: 21 verified functions plus an `android-libxposed` module record (package,
scope, signer, and the BLAKE3 digests of every DEX and `.so` it packages). XAX compiles the
functions to JVM class files, lowers them to DEX, adds the `Module` lifecycle forwarder, the
`Bfp1Bridge` native declaration and the `AdBindings` holder, writes the manifest and libxposed
metadata, and signs the APK with APK Signature Scheme v2.

To change the module, open the store in [XAX-MCP](https://github.com/MrxSiN/XAX-MCP), export its
carrier, edit, construct, and export the new store. The carrier is transport; the store is source.

</details>

---

## Build

Everything runs through XAX-MCP's tools; the repository has no build script. See
[`docs/BUILD.md`](docs/BUILD.md) for the one-time inputs and the exact calls.

```text
brainfuckC   source/**/*.bf          → lib<policy>.so   (stages run on an arm64 phone over ADB)
xax-mcp      xax_workspace open      source/xax/youtubehideads.xax
             xax_build               → signed APK (inputs and key granted by the host)
             xax_export              → YouTubeHideAds.apk
```

## Design

```
source/brainfuck/          the policy programs, one decision each
source/brainfuck-runtime/  the programs that ship as .so: settings snapshot and component classifier
source/xax/                youtubehideads.xax, the whole Android side
contracts/                 the Brainfuck byte ABI and the component fact order
testdata/                  golden ABI byte vectors
evidence/                  device and build records behind every claim in this README
docs/                      architecture, build, limits; docs/history/ for the Python-era iterations
```

## Troubleshooting

| Problem | Try |
|---|---|
| Ads still appear | Check **Hooks installed** and **Removed this session** on the page. Only video slots, feed components, Premium offers and pop-ups are hooked so far. |
| No YouTubeHideAds entry in Settings | Check the module is enabled and scoped to YouTube, then force-stop YouTube once. |
| Entry appears twice | Should not happen; report it with the Vector log and the YouTube version. |
| A switch seems to do nothing | Check **Hooks installed** on the page. A `0` means that hook did not resolve on your YouTube build. |
| Broken after a YouTube update | Report the YouTube version and the module log lines. |

## Credits

| Project | Contribution |
|---|---|
| [Morphe Patches](https://github.com/MorpheApp/morphe-patches) | The behaviour reference for what counts as an ad. No source copied. |
| [libxposed API](https://github.com/libxposed/api), [Vector](https://github.com/JingMatrix/Vector) | The hooking API and the framework the module runs on. |
| [DexKit](https://github.com/LuckyPray/DexKit) by LuckyPray | Structural resolution of YouTube's obfuscated ad classes (LGPL-3.0). |
| [XAX](https://github.com/MrxSiN/XAX), [XAX-MCP](https://github.com/MrxSiN/XAX-MCP) | The semantic-graph language, its compiler, APK lowering and signing, and the tools that build this module. |
| [brainfuckC](https://github.com/MrxSiN/brainfuckC) | The Brainfuck-written compiler that turns the policies into AArch64 shared objects, and its JNI bridge. |
| [ThreadsHideAds](https://github.com/MrxSiN/ThreadsHideAds), [TwitterHideAds](https://github.com/MrxSiN/TwitterHideAds), [GmailHideAds](https://github.com/MrxSiN/GmailHideAds) | The idea, and the scar tissue. |

Licensed under GPL-3.0-or-later. Third-party terms are in [`NOTICE`](NOTICE) and
[`docs/UPSTREAM_PROVENANCE.md`](docs/UPSTREAM_PROVENANCE.md).

## Disclaimer

Not affiliated with, endorsed by or sponsored by Google LLC. "YouTube" is a trademark of Google LLC
and is used only to name the app this module targets. Provided for educational and personal use.
YouTube updates may break the hooks without notice.
