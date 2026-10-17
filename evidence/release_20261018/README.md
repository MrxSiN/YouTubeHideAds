# Release 1.0.0 (versionCode 100), 2026-10-18

Release 1.0.0 is build 77 with two changes:

1. **One shared AND3 library.** The seven AND3 semantic paths (Premium upsell, Shorts ad slot,
   Playables, fullscreen swipe, feed section, AI channel, original audio) load and call one
   `lib/arm64-v8a/liband3.so` instead of seven identical copies. It holds the same native bytes
   (BLAKE3 `3c31b9d7…`). In the XAX graph, 56 string constants were rewritten (49 policy names and
   7 preload paths). Loading the same path again with `System.load` does nothing, so the seven
   preload calls were left in place.
2. **New package.** `org.youtubehideads.module` became `io.github.mrxsin.youtubehideads`, matching the
   author's other modules on Xposed-Modules-Repo. The module, binding classes and settings-entry tag
   use the new prefix. versionCode is 100 and versionName is 1.0.0. Preferences live in YouTube's own
   data, so they carry over. The module has to be enabled once in the manager under its new name.

## Build

- Before any edit, the build 77 carrier was reconstructed with the retained snapshot
  ([toolchain](../ai_audio_branding_20261018/toolchain.json)). It gave a byte-identical store
  (root `11569d32…`) and APK (SHA-256 `97a772bf…`), so the pipeline reproduces.
- The compiler and native/DEX inputs are unchanged. `branding.apk` was rebuilt with AAPT2 36.0.0 for
  the new package and versionName, and its new BLAKE3 is pinned in the store.
- The APK has 11 native paths instead of 17 and is 98,838 bytes smaller than 77.
- Identity: [build.json](build.json) and [aapt badging](apk-badging.txt).

## Device (Pixel 8 Pro, Android 17, YouTube 21.41.525, Vector)

- The intermediate shared-library build (versionCode 78) first failed with `UnsatisfiedLinkError`
  on `libsuppress_premium_upsell.so`, because the old preload paths were still in place. After
  those were rewritten, it passed all 531 checks ([log](and3-78-startup.log)).
- 1.0.0 was installed under its new package and the old package was removed. The installed
  `base.apk` SHA-256 matches `apk_sha256`.
- Cold start ([log](v1.0.0-startup.log)): ad 70, SponsorBlock 277, Playables 24, swipe 28, feed 72
  and AI/audio 60, for 531 self-checks, all true. Every hook installed: video ad, player layout,
  component, Premium, fullscreen dialog, engagement panel, SponsorBlock, Shorts selection and feed
  removal, swipe, original audio and lifecycle.
- Not repeated on 1.0.0: the per-feature off/on UI checks, the video-pixel comparison and the AI list
  fetches. The native bytes and decision call sites are unchanged from 77, so 77's evidence still covers them.
