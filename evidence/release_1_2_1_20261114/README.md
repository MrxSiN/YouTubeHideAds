# Development build 156 (1.2.1), 2026-11-14

Pixel 8 Pro, Android 17, Vector 2.2 (libxposed API 102), YouTube **21.45.88**. [Build identity](build.json).
Every result below was EXECUTED on that phone over ADB unless marked otherwise. Logs are the module's
`YouTubeHideAds` lines only.

## 1.2.0 on YouTube 21.45.88 (before)

[Startup log](runtime-155-on-21.45.log): every hook installs and every self-check passes. Compared with the
[1.2.0 log on 21.43](../release_1_2_0_20261030/runtime-155.log) no line is missing. SponsorBlock fetched segments
here (`SponsorBlock response cached`), so the HTTPS-filter limit from 1.2.0 did not apply in this session.

Two problems:

| Problem | Evidence | Cause |
| --- | --- | --- |
| [Issue 6](https://github.com/MrxSiN/YouTubeHideAds/issues/6): dragging the live chat in fullscreen changes the volume | `Player swipe completed mode=2` and stream volume 1 → 0 after a vertical drag on the chat | The swipe gate split the whole window into brightness (left 40 %) and volume (right 40 %) zones. The player view spans the window and the chat is a `FullscreenEngagementPanelCoordinatorLayout` inside it (x 2032–2992 of 2992 in landscape), so the chat sat in the volume zone |
| Skip live Shorts never skipped | A probe logged every component id starting `reel_player_overlay` or containing `live`: 16 Shorts produced none from the Shorts pager (live-stream components in the regular player were logged) | The trigger waited for the `reel_player_overlay.e` component, which 21.45 never routes through the component hook. The feature could not fire, live Short or not |

The progress hook already reads `playbackType`: a live stream logged `playbackType=9 durationMs=0`, videos and
Shorts `playbackType=1`.

## Build 156

- **Issue 6.** On ACTION_DOWN in fullscreen, a touch inside a shown fullscreen engagement panel (live chat, comments,
  description) starts no swipe. With the panel docked on the right, the zones are measured across the width left of
  it. The panel is found by class: on 21.45 its id name returns 0 from `getIdentifier`.
- **Skip live Shorts** now keys on `playbackType=9`, once per playback. When the Shorts pager is shown, it sends the
  pager a short synthetic upward drag (authorized by the unchanged AND3 policy), so YouTube flings, settles and
  plays the next Short. The old component-name trigger and its four functions are removed.
- **Remember live stream position** (new, Player controls, off by default). Behavior follows Morphe's
  [RememberLiveStreamPositionPatch](https://github.com/MorpheApp/morphe-patches/blob/44031c5/extensions/youtube/src/main/java/app/morphe/extension/youtube/patches/playback/livestream/RememberLiveStreamPositionPatch.java).
  It is an independent XAX implementation on the module's existing player bridges. While a live stream plays, the
  position is saved every 5 s. When the same stream is reopened, the module seeks back with the player's own seek
  method, retrying up to 10 times until the position is within 3 s, then drops the entry. At most 100 streams are kept.
- The progress hook used to run only with SponsorBlock on. It now also runs when either live switch is on, and the
  SponsorBlock path (including its per-tick channel lookup) still needs SponsorBlock.

## Results on build 156 ([runtime log](runtime-156.log))

| Check | Result |
| --- | --- |
| Startup | 22 self-check lines pass; no `failed`, `unresolved`, `ambiguous` or exception line; no crash buffer entry |
| Ten normal Shorts | 10 playbacks, 0 `Live Short skipped` |
| Issue 6, drag on live chat | No swipe logged; the chat scrolled (YouTube showed its jump-to-latest arrow) |
| Issue 6, drag on the right of the video | `Player swipe completed mode=2` (volume) |
| Issue 6, drag on the left of the video | `mode=1` (brightness), on the build before the final rebuild with the same f249 |
| Save | `Live stream position saved` every ~5 s; three double-tap rewinds moved it from 890,940,202 to 890,916,872 ms |
| Restore after force-stop and reopen | `to restore: 890927887`, `restored: 890925023` (within 3 s) instead of the live edge |
| Restore, earlier session | rewound to 890,223,941; reopened 10 s later: `restored: 890223943` |
| Switch | Shown under Player controls after Background playback, off by default ([screenshot](settings-live-position.png)); toggling wrote `live_remember_position` to `youtubehideads.xml` |

## Probes (not shipped)

- **Skip live Shorts, inverted.** A probe treated `playbackType=1` as live. With `scrollBy` (the old method), the
  first skip took 13 s to start the next Short and a later one did not move the pager. Accessibility scroll-forward
  did not move it at all. The synthetic drag skipped every new playback within about 250 ms and the next Short
  played (`SponsorBlock playback generation changed` after each skip).
- **Shorts URL of a live stream.** `youtube.com/shorts/<live id>` opened in the regular player, not the Shorts
  pager; no skip happened.

## Limits

- **NOT RUN:** a real live Short in the Shorts feed did not appear, in this session or earlier ones. Skip live
  Shorts is shown only by the inverted probe and by `playbackType=9` on live streams in the regular player.
- Remember live stream position was tested only on Lofi Girl's 24/7 stream, whose positions stayed valid across
  the test window. Morphe warns that 24/7 streams can fail; the setting's summary says so too.
- The chat check used `adb input` drags. A left-docked panel (right-to-left layouts) keeps window-wide zones.
- New strings are English only. Dark theme, this phone and YouTube 21.45.88 only.
