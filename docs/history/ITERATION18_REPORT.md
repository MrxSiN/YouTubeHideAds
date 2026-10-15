# Actual module and in-YouTube page — 2026-10-16

Built, installed and enabled `org.youtubehideads.module` for YouTube only.
It adds **YouTubeHideAds** to YouTube's Settings toolbar and opens its own
page inside YouTube. There is no launcher Activity or standalone manager.

**APK:** `build/module/YouTubeHideAds-debug.apk`, version code 21,
53,870 bytes, signed with a local development key.
SHA-256: `b39e1139cc2f4c8a42126b2bacd65e28a172beb0f75783baaede1b9187b28722`.

The page is currently a status page. Ad suppression and SponsorBlock are not
implemented, and the page states this explicitly. No ineffective feature
switches or success claims were added.

## Implementation

- `app/AndroidManifest.xml`: module metadata and an empty application; no
  Activity, service, receiver or launcher declaration.
- `toolchain/xax/module_graph.py`: canonical XAX graphs implement the package
  guard, libxposed hook installation, settings-toolbar entry, page and click
  callbacks. The hook proceeds once, checks the focused Activity, and uses a
  View tag to avoid duplicate entries. The toolbar and SettingsActivity
  identities were verified on the actual installed YouTube build.
- `toolchain/xax/module_build.py`: validates the clean XAX pin and exact
  libxposed API-102 AAR, verifies the canonical store, compiles XAX JVM code,
  emits a minimal DEX lifecycle forwarder, builds the source-attested BF router,
  converts with D8, checks the Vector module contract, and signs the APK.
- `scripts/verify_module_device.py`: checks the installed APK hash and exercises
  the actual page, navigation, duplicate handling and process survival.
- `tests/test_module_graph.py`: real XAX callback compilation, launcherless
  manifest validation, and wrong-dependency/stale-success rejection.

The lifecycle forwarder is a **project-authored platform lowering adapter**,
using upstream `DexBridgeSpec` and `DexAssembledMethod`. Its generated
`Module.onPackageReady(param)` forwards `(this, param)` into the verified XAX
static entry and returns. It contains no hook policy or UI behavior. This is
not an invented claim that upstream's fixed JNI lifecycle carrier supports
arbitrary managed callbacks. All callback bodies are compiled from actual
XAX graphs; no handwritten Java/Kotlin/C/Python application runtime is packaged.

The manifest uses SDK AAPT2 because the pinned XAX manifest carrier requires
an Activity. The APK contains two DEX files and modern libxposed metadata,
without native libraries, bundled libxposed API classes or test harnesses.

Opening the page also invokes genuine `dispatch_all.run([B)[B` inside the
YouTube process and checks its output. This is an engine self-check using a
known input, not a fabricated live ad event. No ad removal is inferred from it.
The managed route uses the existing JVM BF backend; the external BrainfuckC
native adapter remains available but is not used by this APK.

## Device evidence

Tested environment: Pixel 8 Pro, Android 17 / API 37, YouTube 21.41.525,
Vector 2.2 / libxposed API 102. The module is left installed and enabled with
scope `com.google.android.youtube/0`; YouTube data was not cleared.

| Check | Observed result |
| --- | --- |
| Module discovery and loading | PASS inside the real YouTube process |
| Lifecycle hook | PASS, `Activity.onWindowFocusChanged(boolean)` |
| Settings entry | PASS in the existing toolbar; no settings rows covered |
| Page open/close | PASS, three cycles |
| Android Back | PASS, returns to YouTube Settings |
| Duplicate prevention | PASS, one entry after every cycle |
| BF call inside YouTube | PASS, three successful engine self-check logs |
| YouTube process survival | PASS, same process through all cycles |
| Launcher resolution | `No activity found` |
| Full regression suite | 138 discovered: 125 passed, 13 skipped |
| Final module contract tests | 3 passed, including wrong-AAR rejection |
| Final module/preflight checks | 5 passed after correcting production-ad-only diagnostic labels |
| Source-owner audit | PASS, twelve BF policies; no unexpected conventional app sources |
| Live ad suppression / SponsorBlock | NOT IMPLEMENTED / NOT TESTED |

The 13 skips are the existing Linux/GCC-dependent desktop JNI tests on Windows.
The final added dependency-rejection test was run in the focused module group
after the full suite; it is not included in the 138-test full-suite count.

Evidence: `evidence/module_20261016/device-result.json`, `build-result.json`,
`module.log`, `unit-tests.log`, `module-tests.log`, `settings.xml`, `page.xml`,
`settings.png` and `page.png`. The installed APK hash matches the delivered APK.
Future checker runs write under `build/module-device` by default, preserving
the archived session evidence.

## Reproduction

From the project root in PowerShell:

```powershell
python -B -m toolchain.xax.module_build `
  --xax-source build/xax-pinned `
  --java-home 'C:\Program Files\Android\Android Studio\jbr' `
  --sdk 'C:\Users\SiN\AppData\Local\Android\Sdk' `
  --api-aar 'C:\Users\SiN\.gradle\caches\modules-2\files-2.1\io.github.libxposed\api\102.0.0\cfded6d221db78fadd94d90cffaee5417a2e2047\api-102.0.0.aar'
```

Install/enable with the supplied ADB and Vector CLI, then restart YouTube:

```powershell
$adb = 'D:\Android\platform-tools\adb.exe'
& $adb -s 38021FDJG00610 install -r build/module/YouTubeHideAds-debug.apk
& $adb -s 38021FDJG00610 shell su -c '/data/adb/modules/zygisk_vector/cli modules enable org.youtubehideads.module'
& $adb -s 38021FDJG00610 shell su -c '/data/adb/modules/zygisk_vector/cli scope set org.youtubehideads.module com.google.android.youtube/0'
& $adb -s 38021FDJG00610 shell am force-stop com.google.android.youtube
```

Open **YouTube → Settings → YouTubeHideAds**. Repeat the automated device check:

```powershell
python -B -m scripts.verify_module_device `
  --adb 'D:\Android\platform-tools\adb.exe' --serial 38021FDJG00610
```

The checker expects the module to be installed and scoped first. It leaves the
module installed and the phone on YouTube Settings. It does not enable unrelated
modules, change YouTube preferences or clear app data.

## Relevant diagnosis and limitations

The manifest's `Shell_SettingsActivity` redirects to the real SettingsActivity.
The early resume callback ran before the window was attached, so the final hook
waits for window focus. YouTube's AppCompat `Toolbar.getMenu` is obfuscated; the
final implementation uses only the stable Android `ViewGroup.addView` API.
These were diagnosed on-device before selecting the final implementation.

Vector sometimes loaded an older module snapshot immediately after replacement.
Version codes were bumped during development, and a subsequent YouTube restart
after package-update processing loaded the current code. Verification checks the
installed APK hash, actual visible entry/page and module process logs.

This is a development APK tested on one YouTube/framework/device combination.
The page target is verified for that version, not resolved by DexKit. Live ad
targets, authenticated feature inputs/actions, preferences and SponsorBlock
network/player binding remain separate implementation work. The standalone
manager requirement from earlier notes is superseded by the user's in-app-page
instruction. No release APK or upstream redistribution permission is claimed.
The preflight gate now labels its remaining requirements as production ad-host
requirements; it no longer reports that the proven page module is absent.
