# Development build 157 (1.3.0), 2026-11-14

Pixel 8 Pro, Android 17, Vector 2.2 (libxposed API 102), YouTube **21.45.88**. [Build identity](build.json).
Logs contain only the module's `YouTubeHideAds` lines. Every result is EXECUTED on that phone over ADB unless it
says otherwise.

Build 157 is built on build 156 (1.2.1). Each feature was first developed and checked as a separate APK. They were then
combined into one store by transport scripts applied in this order: settings layout, playback speed, blacklist,
captions, Return YouTube Dislike, player tweaks, video quality, DeArrow, version. The XAX compiler, native policy
libraries, DEX and signer are the same as in 1.2.1. XAX `main` was still at `affbb53` on the build day.

## What is new

| Area | Change | Default |
| --- | --- | --- |
| Settings | One **YouTube Hide Ads** page in sections: Ads & promotions, SponsorBlock, Player, Shorts, Feed & content, About. Feature settings are inline, with no sub-pages except Captions, SponsorBlock and Shorts components | — |
| Swipe pill | Brightness docks at the right edge and volume at the left. With a fullscreen panel open, the pill docks beside the panel | — |
| Playback speed | Default speed for videos and for Shorts, each from 0.25x to 2x, applied once per playback. A manual change is kept. Live streams are left alone | YouTube default |
| Video quality | Highest quality not above a limit, set separately for Wi-Fi/Ethernet, mobile data, Shorts and live streams, applied once per playback | Auto |
| Captions | Ordered preferred caption languages; option to stop automatic captions | Off |
| Return YouTube Dislike | Dislike count (or percentage) under the dislike button on the watch page, from returnyoutubedislikeapi.com. Read only, no votes are sent | Off |
| Player tweaks | Tap to seek, Loop video, Speed button (1x, 1.25x, 1.5x, 2x) in the player's top bar | Off |
| Blacklist | Hide feed, search and related items by channel or keyword; optionally comments too | Off |
| DeArrow | Community thumbnails from DeArrow, or YouTube's still frame from the middle of the video. Titles are not replaced | Off |

A double-tap seek length setting was built and then removed before release. YouTube already has its own
**Double-tap to seek** setting with the same values.

## Fixes from the Opus audit (before the final build)

An independent audit read every feature script and dumped the combined carrier. It found no traced crash. Fixed:

- Startup installers are now guarded one by one (`carrier_lib.guard`), so a throwing installer skips only itself.
  Before this, one throw would have skipped every installer after it and the lifecycle hook.
- The new per-tick calls in the progress hook (speed, dislikes, speed button) are guarded, so a throw there cannot
  skip SponsorBlock's work for that tick. The speed button's click listener runs outside any hook and is guarded too.
- Video quality: the "module is selecting" flag is reset at each new playback, so a failed selection cannot make
  later manual choices look like the module's.
- DeArrow: rewritten thumbnail requests carry Glide's default headers, not YouTube's. The default comes from
  the only field of the headers interface (constructor argument 1). If that shape changes, the hook is not
  installed.

## Results on the final APK ([startup](runtime-157-startup.log), [playback](runtime-157-playback.log))

| Check | Result |
| --- | --- |
| Startup | 22 `installed` lines, including speed, captions, quality, loop, tap to seek, speed button and DeArrow. No `unresolved`, `ambiguous`, failure or exception line |
| Settings page | Version reads `1.3.0`. Default playback speed rows and the Blacklist group are inline ([player](settings-player.png), [blacklist](settings-blacklist.png), [dislikes and tweaks](settings-ryd-tweaks.png)). No double-tap row |
| Speed rows | Tapping **Videos** opened the choice dialog (YouTube default, 0.25x … 2x); picking 1.5x changed the summary to `1.5x` |
| Default speed | Next video: `Default speed applied: 1.5, player reports 1.5`. The fullscreen speed button read `1.5x` |
| Speed button | A tap logged `Speed button: 1.25x`. No crash |
| Blacklist Save | Typing a handle and pressing Save wrote `blacklist_channels` to the module's prefs |
| Video quality | Wi-Fi limit 480p: `selected 240p` on "Me at the zoo", where 240p is the highest it has. On the first combined build (before the audit fixes), `selected 480p` on `dQw4w9WgXcQ`. Shorts limit 240p: `selected 240p` on each of 5 Shorts ([feature-build screenshot](quality-shorts-240p.png)) |
| Captions | `Captions automatic selection DEFAULT reason 2: en / .en` on a video with captions |
| DeArrow | Thumbnails loaded on Home with DeArrow mode on (`DeArrow branding cached` lines). [Comparison from the feature build](dearrow-compare.png) |
| SponsorBlock, ads, Shorts | `SponsorBlock response cached` on each video, `Shorts sponsored entries removed before pager: 4`, feed ad components replaced |
| Swipes | Fullscreen left drag `mode=1` (brightness), right drag `mode=2` (volume) |
| Stability | 0 `FATAL EXCEPTION` in logcat across Home, a watch page, fullscreen and Shorts |

## Return YouTube Dislike

- **BLOCKED (real fetch on this phone):** `RYD request failed: … SSLHandshakeException: Certificate chain does not
  conform to required transparency policy: NOT_ENOUGH_SCTS` ([log](ryd-blocked-tls.log)). AdGuard is installed
  on the phone with HTTPS filtering, and its user CA breaks this host's certificate-transparency check inside YouTube.
  SponsorBlock connected in the same session. YouTube's buttons were left untouched, which is the intended
  failure behaviour. The API answered from a desktop on the same day (dislikes 521,845 for `dQw4w9WgXcQ`).
- EXECUTED with a probe build (not shipped) that pre-seeded that one entry: the count `522K` was drawn centred under
  the dislike icon ([crop](ryd-probe-count.png)).
- NOT RUN: percentage mode on the phone, light theme, a successful live fetch.

## Not run or limited

- **Playback speed:** music videos have no separate default, because YouTube 21.45 exposes no on-device music
  signal (BLOCKED). After a default speed is applied, YouTube's own speed menu still shows 1x, and the speed button
  read `1x` in portrait once.
- **Video quality:** the mobile-data path and live streams were NOT RUN (radios are never toggled). A manual pick
  made before the module's first selection, less than 1 s after start, is overridden.
- **Captions:** blocking automatic (ASR) captions was NOT RUN; no tested video had YouTube pick an ASR track.
  Bilingual captions are BLOCKED and not built.
- **DeArrow:** titles are BLOCKED and not built. Thumbnails already on screen change only when YouTube requests
  them again. The thumbnail URL sends the video ID to DeArrow's thumbnail host.
- **Blacklist:** filtering itself was checked on the feature build (a blocked channel's item left Home). The final
  APK was checked for the settings and Save only. Replies, posts, playlists and mixes are not filtered.
- **Player tweaks:** Loop and Tap to seek were checked on the feature build. Fullscreen tap to seek, Shorts and live
  streams were NOT RUN.
- **Seen, not fixed:** during the final swipe check the end-of-video **More videos** sheet opened. A right-side
  drag that may have started on it logged a volume change. Whether that sheet should block swipes like the live
  chat does was not looked into.
- The test settings written during these checks were cleared from the phone afterwards. New strings are English
  only. Dark theme, this phone and YouTube 21.45.88 only.
