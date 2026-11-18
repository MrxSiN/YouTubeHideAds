# Hot-path fixes, build 164 (2026-11-18)

Development source **1.3.0, build 164** = build 163 plus nine
[native transactions](../../source/xax/transactions/perf-20261118/README.md).
[Build identities](build.json) · [Structured device results](device.json).

Device: Pixel 8 Pro, Android 17/API 37, Vector 2.2/API 102, YouTube 21.45.88, Music 9.46.51.
Every comparison ran the same script on a separately named test package (`...perfdev`) that
temporarily replaced the release and Music development modules.

## What was found

- **Startup is already cheap.** With a warm DexKit cache the main-thread module window is about
  52 ms and creates no DexKit bridge. The one-time cache rebuild after an install or host update
  is about 0.8 s. Unchanged.
- **Progress-hook crash (builds 157-163).** YouTube reports progress in `PLAYBACK_PENDING` before
  the player response exists; the hook invoked a method on it. Vector logged
  `Hooker ... crashed after proceed` 1-2 times per video open and skipped that tick's work.
- **Regex compiled per call.** Three regex compiles per ordinary feed component and one per
  player-state callback.
- **YouTube global-layout listeners (downloads from build 162, SponsorBlock from 1.3.0).** Each layout pass
  called `Resources.getIdentifier("player_additional_view_container")` before checking anything,
  including with downloads disabled. The speed button did the same once per playback tick.
- **Music Audio/Video pill search (build 163).** Every touch-down in Music walked up to 1,024
  views and resolved two resource names per visible view, each inside a `CompletableFuture` chain.
- **Music ad classifiers (build 158).** Two AND3 JNI calls per component even when no ad marker
  matched.

## Before/after

| Status | Observation | Before | After |
| --- | --- | --- | --- |
| MEASURED | YouTube hook crashes per video open (3 opens) | 2, 2, 1 | 0, 0, 0 |
| MEASURED | YouTube warm startup, main thread (ms) | 53, 52, 52 | 57, 54, 53 |
| MEASURED | YouTube module global-layout listener, % of process CPU while scrolling | 1.32 | 0.27 |
| MEASURED | YouTube `Resources.getIdentifier`, same | 1.13 | 0.05 |
| MEASURED | YouTube `String.matches`, same | 0.10 | 0.03 |
| MEASURED | Music top module hook, % of process CPU (scroll, then play) | 1.86 | 0.42 |
| MEASURED | Music `Resources.getIdentifier`, same | 1.21 | 0.08 |
| MEASURED | Music Brainfuck JNI bridge, same | 0.08 | 0.01 |
| EXECUTED | YouTube removals in session (components / video ads) | 17 / 3 | 17 / 3 |
| EXECUTED | YouTube startup self-checks, hook installs, SponsorBlock controls, download button | pass | pass |
| EXECUTED | Music startup self-checks and hook installs | pass | pass |
| EXECUTED | Music Audio/Video switch: video to song through the native queue | - | completed |
| EXECUTED | Music background playback after Home and screen off | - | PLAYING |

Exclusive audio's bounded stack check was measured at 0.03 % and left unchanged. Application DEX
grew by 436 bytes.

Logs: [163 start](v163-start1.log), [163 video open](v163-link1.log), [164 start](v164-start1.log),
[164 video open](v164-link1.log), [164 Music start](v164-music-startup.log).

## Toolchain

XAX `fa6d2ed` (latest main, ledger 0036 Windows seed). Built with it, the unchanged build 163
store reproduces build 163's recorded production DEX byte for byte. BBC latest main `0039ccc` is
unchanged and no BF input changed. AAPT2 9.3.1 reproduces the pinned branding archive byte for byte.

**Worked around upstream:** one `xaxc edit` batch replacing two functions with shared owners can
write a store that `xaxc verify` rejects with `XAX.IDENTITY.OBJECT_MISSING`; each replacement alone
verifies. Those changes are separate stages.

## Device state and limits

Afterwards the release module was re-enabled for YouTube and the Music development module for
Music, with their original scopes, and the test package was uninstalled.

**NOT RUN:** Music Premium/welcome surfaces (not served during the run), downloads save/export end
to end, external downloader handoff, light theme, other devices or host versions, release publication.
