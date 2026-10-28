# Background playback — 2026-10-27

Exact development artifact: **1.3.0-dev/code 131**, installed on Pixel 8 Pro / Android 17,
Vector 2.2/API 102, stock YouTube 21.42.243. No YouTube APK was modified.
[Build identity](build.json) · [Toolchain](toolchain.json) · [Preservation](preservation.json) ·
[Implementation](../../docs/BACKGROUND_PLAYBACK.md).

The canonical store and installed APK correspond to root
`601800dd96ddd149f6e2c2e5203df9dcb97c11c0b858225f9215b341151ccca6`.
APK SHA-256: `c2eb5f668af7d9c7742cd5d72bac15323cee17e8d9fad65ffb7ca555d86d4984`.
The APK is retained locally at `build/port/YouTubeHideAds-background-131.apk`; APKs are ignored,
not committed or published. Version 1.2.1/code 127 remains the tagged baseline.

## Automated and structural verification

- Canonical StoreReader verification and typed semantic construction pass. The existing JVM SDK
  round-trips the baseline to the identical root before editing.
- 281 unique functions: 19 added, three existing bodies changed, 259 existing bodies preserved.
  Existing policy/self-check graphs, native pins/bytes, third-party DEX and signing pin are unchanged.
- All 11 packaged native paths match the code 127 native SHA-256 map. The new branding archive is
  pinned deliberately; the APK contains the exact preserved Morphe notice.
- libxposed API 102 static acceptance and APK signature v2 verification pass.
- The designated BBC native Windows compiler compiles the authored AND3 command stream; all eight
  input/output cases pass. This is a standalone native test, not a claim that current BBC's different
  shared-library ABI replaced the pinned Android policy. [Raw cases](bbc-policy-checks.json).
- Existing 636 packaged startup checks and the new 28 background cases pass in code 131 device
  processes. The 28 include actual packaged AND3/JNI calls. Logs identify the worker thread separately
  from the main thread and show the complete validated hook installation.
- JSON contracts/fixtures parse; the BF executable stream is identical to the baseline. No new
  conventional-language implementation is retained in this repository.

The data-only [integration cases](../../testdata/background_playback_vectors.json) specify
acceptance expectations. They are not a runnable test suite or an assertion that every scenario passed.

## Actual device observations

[Media-session snapshots](device-cases.json) retain only the YouTube session and test titles.
Android keeps a PlaybackState position baseline between updates. Position advancement is therefore
checked at a subsequent explicit pause, which produces a fresh position, rather than by extrapolating
two copies of the same PLAYING snapshot.

| Scenario | Observation |
| --- | --- |
| Regular video, Home/launcher | Big Buck Bunny continued with the YouTube session active/PLAYING |
| Regular video, screen off | Device reported Dozing; a locked-screen pause reported 98,332 ms versus the prior 62,338 ms playback baseline |
| User pause and return | PAUSED remained PAUSED after returning; no automatic module play command |
| Repeated Home/return | Two additional cycles retained the same video; subsequent pause advanced approximately seven seconds, without a restart |
| Explicit native stop | After unlock, Close minimized player changed a playing regular video to STOPPED/inactive; Home/return left it stopped |
| Android media keys | Locked-screen PAUSE and explicit PLAY worked through Android's media-session path |
| Actual notification UI | Tapping the notification's play then pause changed PLAYING → PAUSED and advanced 105,982 → 108,081 ms |
| Setting UI/default | Exact requested title/summary appeared checked under Player controls; [screenshot](settings-enabled.png) and saved preference were verified |
| Setting disabled | UI saved false; after process restart the same regular video became STOPPED with the screen off, restoring native restrictions |
| Kids controller | Official Pinkfong Baby Shark test; the first authorized kids-policy override was logged |
| Kids video, independence | Background switch true with both Hide ads and SponsorBlock false; screen-off playback remained active, and an explicit pause reported content position 26,333 ms |
| Existing features | Existing startup suites and hook discovery pass; original-audio selection and SponsorBlock retrieval were also observed during development. The separate 64-case native SponsorBlock UI suite passed after unlock. A new actual SponsorBlock seek was not required or claimed |
| Preferences | Original preference entries were restored; test switches did not remain changed. [Restoration record](restoration.json) |

The Pinkfong test began with native ads because the ad master was deliberately disabled. Early
PlaybackState updates use ad-relative positions/actions; they are not presented as evidence of a
module restart. The later content position and pause are recorded separately. After the user unlocked
the phone, the native [Try YouTube Kids card and disabled Comments action](kids-native-ui.png) were
captured for the same Pinkfong test. The UI did not expose a separate raw Made for Kids metadata flag;
the observed native UI and kids-controller callback are recorded without asserting that raw flag.

The [64-case UI result](post-unlock-ui-check.log) was observed directly through ADB in PID 26526.
The [unrelated download action](premium-download-notice.xml) still showed Get YouTube Premium;
the prompt was dismissed with Not now. No download, purchase, comment or playlist change was made.

## Negative candidates and limits

Development candidate 128 stayed inactive with missing numeric matches. Candidate 129 found the
same accessor twice; encoded-identity deduplication fixes that without accepting distinct candidates.
Candidate 130 caught an enum-initializer reflection error on the worker and left readiness false.
Code 131 resolves the enum class directly and installs the complete hook set. These are negative
development observations, not tests against a second installed YouTube version. No target-missing
or ambiguous condition was deliberately injected into the final production process.

Unverified on real hardware: physical Bluetooth controls, incoming calls/audio-focus interruptions,
a mixed Shorts/regular stack and another YouTube/framework/device. Normal user pauses and termination
are not hooked, and the module contains no play/resume action, but that is distinct from exercising
every native route on a device.

After the longer lock test the phone required a normal secure unlock. No credential was requested
or bypassed. The user subsequently unlocked it for the native stop/Kids/UI follow-up above.
Stay-awake while charging was temporarily enabled for that follow-up, then restored to its original
value 0; the original 600,000 ms screen timeout was unchanged. Module preference entries remained
unchanged during the follow-up, and YouTube was left stopped. [Restoration](post-unlock-restoration.json).
The canonical source and installed APK identities are unchanged. No user data, account settings,
notification preferences, audio settings or security configuration was cleared or changed.

Automatic approval review rejected the ADB deep-link video launch with only “blocked by policy”.
The actual playback tests used the visible YouTube search and player UI instead.
