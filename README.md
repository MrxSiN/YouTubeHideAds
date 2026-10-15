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
> **Work in progress.** The module loads in YouTube, installs its ad hooks and adds its own page to
> YouTube's Settings. No ad has yet been seen removed on a device, because none was served while
> testing. SponsorBlock is not connected. See the [compatibility](#compatibility) table for what has
> actually been tested.

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
the package guard, the libxposed hooks, the settings entry, the page — is built from
XAX semantic graphs, compiled and verified, then lowered to DEX.
Project-authored Java, Kotlin, C or Python never ships in the APK. Python exists only as the build
toolchain and test harness, and it is honest about it.

|  | |
|---|---|
| 🧠 **Policy in Brainfuck, compiled** | Twelve hand-written eight-command programs, compiled ahead of time. No interpreter in the APK. |
| 🧬 **Host in XAX** | Hooks and UI are canonical XAX graphs, store-verified before they are lowered to DEX. |
| 🚪 **No launcher** | The module opens its page from inside YouTube Settings. No companion app, no manager Activity. |
| 🛟 **Fails closed on seeks, open on content** | A malformed or stale request never seeks the player and never hides anything. |
| 🧪 **Proven identical** | Every policy is checked against the reference interpreter, exhaustively where the input space allows. 4,463 comparisons passed on an arm64 phone. |

---

## What it will remove

Each feature is one Brainfuck program in `source/brainfuck/`. All twelve compile and pass their
tests. Video slots, Premium upsells and the component classifier (`brainfuck-runtime/ad_component`)
are wired to DexKit-resolved hooks; the rest wait for theirs.

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
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.41.525 | 0.3.0-dev (code 26) | Settings row and page; switches persist, reset works, Back and arrow close; one row only, none on subpages; 5 ad hooks installed; BF self-check passes. No ad served, so no live removal yet ([evidence](evidence/settings_20261016/)) | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | Vector 2.2 (API 102) | 21.41.525 | 0.2.0-dev (code 21) | Loads in YouTube; Settings entry, page, Back and duplicate checks pass over three cycles; BF router self-check passes. No ad removed — not wired yet | @MrxSiN | 2026-10 |
| Pixel 8 Pro | 17 | — (ADB shell) | — | — | 12 policies via native BrainfuckC: 4,463 comparisons against the reference interpreter | @MrxSiN | 2026-10 |

### Known limits

- **No live ad removal observed yet, and no SponsorBlock.** The page says so too. No switch pretends
  otherwise.
- Settings live in YouTube's own preferences. libxposed RemotePreferences need a module-side writer,
  and this module has no Activity of its own. Clearing YouTube's data resets them.
- The Settings row sits above YouTube's list rather than inside it, so it stays at the top while the
  list scrolls.
- The XAX toolchain is pinned, not vendored; it has no recorded license, so it is not
  redistributed here.
- The inline router sits close to the JVM 64 KB method limit. More programs need method outlining.
- Desktop JNI tests need GCC and are skipped on Windows.

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

There is no release yet. Build the debug APK (below), then:

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
  → libxposed hook (package guard, Activity.onWindowFocusChanged)
  → XAX host (compiled semantic graphs: hooks, settings entry, page)
  → BFH1 request frame: selector + raw bytes
  → dispatch_all.run([B)[B  (AOT-compiled Brainfuck router)
  → BFR1 reply frame: action + payload
  → XAX host validates generation and action, then acts
```

One rule decides where code goes: **if it needs Android, Xposed, DexKit or the network, XAX does it;
if it decides what to do with what XAX read, Brainfuck decides.**

<details>
<summary><b>The Brainfuck core</b></summary>
<br>

Every `.bf` file carries a header of `# @feature`, `# @abi`, `# @inputs`, `# @outputs` and
`# @cells` metadata. A line starting with `#` is a comment; every other line may hold only the eight
commands and whitespace. The checker strips comments with a source map, so an error points at the
annotated line, and a comment-only change never changes the compiled output.

The dialect: 8-bit wrapping cells, a 4,096-byte tape, zero at end of input, bounds-checked pointer,
64-byte output cap and a fuel budget (100,000 commands, 2,000,000 for the 64-bit timestamp policy).
The reference interpreter and the AOT compiler share these semantics, and the tests hold them to it.

`generated/router.bf` pastes all twelve command streams verbatim behind a Brainfuck selector, so
there is no host-side switch. An unknown selector produces no output, which the host rejects.

The frame format is in [`contracts/bf_host_v1.md`](contracts/bf_host_v1.md); the style rules in
[`docs/BRAINFUCK_SOURCE_STYLE.md`](docs/BRAINFUCK_SOURCE_STYLE.md).

</details>

<details>
<summary><b>The XAX host</b></summary>
<br>

XAX programs are semantic graphs, not text files. `toolchain/xax/module_graph.py` constructs them,
the pinned XAX compiler verifies the canonical store and compiles them, and `module_build.py`
emits a minimal DEX forwarder from `Module.onPackageReady` into the verified entry, builds the
router, runs D8, checks the Vector module contract and signs the APK. The forwarder holds no
policy and no UI.

Details in [`docs/XAX_ANDROID_INTEGRATION.md`](docs/XAX_ANDROID_INTEGRATION.md) and
[`docs/LANGUAGE_BOUNDARY.md`](docs/LANGUAGE_BOUNDARY.md).

</details>

---

## Build

```bash
./scripts/build_fresh.sh                                   # policies, router, linkage and the test suite
PYTHONPATH=. python3 -m unittest discover -s tests -v      # tests only
PYTHONPATH=. python3 -m toolchain.brainfuck.cli validate source/brainfuck/ads/player/suppress_video_slot.bf
python -B -m toolchain.xax.module_build --xax-source build/xax-pinned --java-home <jdk> --sdk <android-sdk> --api-aar <api-102.0.0.aar>
```

The last command writes `build/module/YouTubeHideAds-debug.apk`, signed with a local debug key.
`scripts/verify_module_device.py` checks it on a connected phone.

You need Python 3.11+, JDK 21, Android SDK with D8, the libxposed API 102 AAR and a pinned XAX
checkout. No pip packages.

## Design

```
source/brainfuck/   the twelve hand-written programs: every decision and limit
source/xax/         notes on the XAX sources
contracts/          the BF host ABI and host operations
toolchain/brainfuck/ checker, reference interpreter, AOT JVM compiler, router builder
toolchain/xax/      XAX graph construction, module build, D8 linkage, APK checks
app/                manifest and module metadata
tests/              Python suite, plus JNI and Android probes (tests only, never shipped)
testdata/           golden ABI byte vectors
evidence/           device and build logs behind every claim in this README
docs/               architecture, ABI, testing, limits; docs/history/ for past iterations
```

## Troubleshooting

| Problem | Try |
|---|---|
| Ads still appear | Expected. Ad suppression is not wired yet. |
| No YouTubeHideAds entry in Settings | Check the module is enabled and scoped to YouTube, then force-stop YouTube once. |
| Entry appears twice | Should not happen; report it with the Vector log and the YouTube version. |
| A switch seems to do nothing | Check **Hooks installed** on the page. A `0` means that hook did not resolve on your YouTube build. |
| Broken after a YouTube update | Report the YouTube version and the module log lines. |

## Credits

| Project | Contribution |
|---|---|
| [Morphe Patches](https://github.com/MorpheApp/morphe-patches) | The behaviour reference for what counts as an ad. No source copied. |
| [libxposed API](https://github.com/libxposed/api), [Vector](https://github.com/JingMatrix/Vector) | The hooking API and the framework the module runs on. |
| [DexKit](https://github.com/LuckyPray/DexKit) by LuckyPray | Planned structural resolution of obfuscated classes. |
| [XAX](https://github.com/MrxSiN/XAX) | The semantic-graph language and compiler behind the Android host. |
| [ThreadsHideAds](https://github.com/MrxSiN/ThreadsHideAds), [TwitterHideAds](https://github.com/MrxSiN/TwitterHideAds), [GmailHideAds](https://github.com/MrxSiN/GmailHideAds) | The idea, and the scar tissue. |

Licensed under GPL-3.0-or-later. Third-party terms are in [`NOTICE`](NOTICE) and
[`docs/UPSTREAM_PROVENANCE.md`](docs/UPSTREAM_PROVENANCE.md).

## Disclaimer

Not affiliated with, endorsed by or sponsored by Google LLC. "YouTube" is a trademark of Google LLC
and is used only to name the app this module targets. Provided for educational and personal use.
YouTube updates may break the hooks without notice.
