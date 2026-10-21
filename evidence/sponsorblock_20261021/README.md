# SponsorBlock, 2026-10-21

Current source is XAX plus the unchanged nine BF policies. The signed APK uses the existing pinned
native/DEX inputs and refreshed static 1.1.0 branding. [Build identity](build.json) and
[compiler findings](toolchain.json) identify the exact canonical store and artifact.

Initial target: Pixel 8 Pro, Android 17/API 37, Vector 2.2/API 102, YouTube **21.41.525**. The phone
updated to **21.42.243** at 21:17:26 local time. The final settings round trip, malformed-import digest
check and 23:33:29 post-restore startup are on 21.42.243; earlier playback/preview/marker evidence
remains attached to 21.41.525. Previous 21.20.405 observations do not certify either version.

## Checks

- Baseline 531, network 18, controls 20 and integration 67 checks run in the packaged Android host.
  The integration checks cover API origins/routes, desktop modes, opacity conversion, invalid imports,
  segment bounds, decimal times, exact draft signatures, preview lifecycle and Bitmap/Canvas pixels.
- Startup resolves one seekbar constructor, one draw method and one public/final instance Rect role.
  Resolution uses structure and type/modifier checks, without pinned obfuscated class/field names.
- Real network observations include a cross-video cache hit and transient failures followed by bounded
  retry and a terminal stop; valid responses continue to be cached. Earlier diagnostic builds established
  these transport positives; the final build also retains its packaged regression checks.
- Final 111 settings export/import commits all ten category modes/colors, preserves opacity and re-exports
  identical JSON. Private ID is excluded by default. Malformed input preserves the exact preference
  digest and shows an error. Original preference-file absence was restored after this reversible test.
- Native player button, main menu, category editor/spinner, settings export, segment editor, preview
  and review are exercised on the phone. Before preview, review is refused; after preview the confirmation
  shows exact video/range/category/server. The confirmation is canceled, without a production write.
- A draft marker is visible on the actual native track; native controls/seek thumb and advancing video
  remain visible. Green range rendering, thumb-area clipping, outside-track pixels and white draft pixels
  are also checked with an actual Android Bitmap/Canvas.

Raw device logs and UI captures are kept locally under
`D:/Android/AndroidStudioProjects/Logs/YouTubeHideAds_20261021_21.41.525`.
Only filtered runtime evidence and non-secret build metadata belong in this repository.

## Scope and limits

Implemented features and bounds are in the [SponsorBlock guide](../../docs/SPONSORBLOCK_API_RESEARCH.md)
and [contract](../../contracts/sponsorblock_inputs.json). Production segment/vote/username/view-report
POSTs are intentionally untested; no fabricated community data was published. No second device,
landscape/RTL matrix or exhaustive network/server-error matrix was available. Natural community-color,
manual-skip and undo positives are distinct from the controlled drawing checks and historical seeks.

Shorts hooks install on 21.41.525 and live sponsored batches were removed during diagnosis. No new
missing-buttons heuristic was added: a genuine live preview also lacks those controls. This change
preserves the existing pre-pager sponsored-entry removal.

The shell-based release mirror was removed to satisfy the BF/XAX-only executable-source constraint.
Mirroring a release to Xposed-Modules-Repo is now manual. Existing user README edits are preserved.
