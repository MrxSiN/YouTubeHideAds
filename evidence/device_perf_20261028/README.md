# Device performance pass — 2026-10-28

Pixel 8 Pro, Android 17 (CP3A.261005.005), Vector, stock YouTube 21.42.243.
Development build **code 135**, built from the installed code-132 store, then **code 143** (DexKit
threads), **code 152** (DexKit result cache) and **code 153** (background playback from links). [Build identity](build.json).

## Diagnosis

Logs from a cold start showed no module errors: all 11 startup self-checks passed and every hook
installed. A 40 s system-wide `simpleperf` profile (cold start, feed scroll, video, Shorts) showed
the cost was in the Brainfuck transport, not the policies:

- `Bfp1Bridge.run` ran `dlopen`/`dlsym`/`dlclose` on every policy call. Opening a
  `base.apk!/lib/...` path makes the linker reopen and parse the module APK each time. The bridge
  and its callers were **22.7 %** of all YouTube-process CPU; `dlopen` was 76 % of the bridge.
- After that, each call still allocated a fresh 4 KiB tape plus two path strings. Fresh tapes kept
  faulting in new TLAB pages: allocation was about 40 % of the call wrapper.
- The background playback flag hook read the preference and called the AND3 policy for every flag
  lookup YouTube made, although only one flag id can ever be overridden.

## Changes

| Change | Effect on behaviour |
| --- | --- |
| Bridge resolves each library's `bfc_call_v1` once and keeps it | None: same JNI signature, checks, status codes and release modes. Libraries were already held open by `System.load`. |
| A path without `/` is a policy name, resolved to `lib<name>.so` beside the bridge; the wrapper passes the interned name | None: that is the directory the old path string named. |
| Bridge runs each call on a zeroed native tape of the Java tape's length; the wrapper passes one shared tape | None: every call still starts on a fresh zero tape, and nothing read the tape afterwards. |
| `bg_authorize` returns false before the preference read and policy call when the flag fact or context input is false | None: AND3 replies 01 only when all three inputs are 1, and all 8 inputs are still checked at startup. |

## Results (same 40 s scripted session)

| Measure | Build 132 | Build 135 |
| --- | --- | --- |
| `Bfp1Bridge.run` incl. callees, share of YouTube CPU | 22.7 % | 0.05 % |
| XAX hook `intercept` incl. callees | 13.3 % | 1.1 % |
| Vector `Vector_.m` hook dispatch incl. callees | 21.9 % | 0.5 % |
| Startup self-checks | 11 pass | 11 pass |

Ads, Shorts ad removal (4 entries before the pager in every run), SponsorBlock lookups and cache,
original audio and background playback (audio kept playing from the launcher) behaved the same in
builds 133, 134 and 135.

## DexKit threads (build 143)

The main-thread discovery bridge ran DexKit with 2 worker threads on a 9-core phone while YouTube's
main thread waited. Build 143 uses 8; the background-playback pass, which does not block the UI,
keeps 2. A/B with alternating installs (each install verified), 4 cold starts per batch:

| Threads | Module load to last hook, main thread (median per batch) | Time to first screen |
| --- | --- | --- |
| 2 | 754, 761, 792 ms | 1272, 1293, 1322 ms |
| 8 | 470, 479 ms | 1018, 1024 ms |

Hook resolution, candidate counts and self-check lines in the log are identical to build 135. An
earlier ordered (non-interleaved) run was discarded: downgrade installs had failed silently.

## DexKit result cache (build 152)

Discovery still runs every site, check, log line and diagnostic record exactly as before; only the
DexKit answers come from a file. All 21 discovery functions reach DexKit through 38 `dk_*` functions:

- A result is its DexKit descriptor. Everything `MethodData`/`FieldData` derives from a descriptor
  (names, types, reflection through DexKit's own `DexMethod`/`DexField`/`DexClass`) is computed the
  same way DexKit computes it. Access flags, modifiers, encode id and `MethodData.toString()` are
  recorded from the live object on a miss, so the background candidate log text is unchanged.
- A query's key is the exact byte string DexKit sends to native code (`serializedBytes`). A
  different query can never reuse another's answer; a site that runs a new query simply misses.
- The file `code_cache/youtubehideads-dexkit.bin` in YouTube's data directory carries a header of
  YouTube's base.apk path, size and modification time and the module APK path. Any mismatch, a
  missing file or an unreadable one is an empty cache. The DexKit bridge is only created on a miss.

| Start | DexKit bridges | Hook, candidate and self-check log lines |
| --- | --- | --- |
| First after module install (old file rejected) | 2 | identical to build 143 |
| Cached, repeated | 0 | identical |
| File overwritten with garbage | 2, file rebuilt | identical, no crash |

A/B with alternating installs, 4 cold starts per batch after one discarded start:

| Build | Main-thread discovery | Time to first screen | Background-thread discovery |
| --- | --- | --- | --- |
| No cache | 464, 452 ms | 1014, 986 ms | 538, 523 ms |
| Cache | 84, 80 ms | 646, 627 ms | 8, 8 ms |

The first development cache build did not store the header on its first run, so the second start
rejected the file once; build 152 stores it whenever it is set. The in-memory cache (about 320
entries) stays for the process because changing the background switch reruns that discovery.

## Background playback from a link (build 153)

Starting a regular 3:33 video from a link, then pressing Home, stopped audio in builds 132 (rebuilt
from its exact source and bridge), 143 and 152 alike. YouTube logged
`blockingStopVideo(), STOPPAGE_PLAYBACK_SUSPENDED`; only the foreground-resume override fired.

Cause: the background hooks are resolved on a worker that starts at the first window-focus refresh.
A video opened from a link creates its player and reports its state before that, so the player
observer never saw a state, the regular-player context stayed unknown and the eligibility and kids
overrides correctly refused. The same link opened after the hooks were in place kept playing.

Fix: startup discovery installs only the player observer, right after `BackgroundBindings` is
created and before any Activity exists. It runs the worker's two exact queries (unique enum
initializer, unique updater on the public player View), so the worker hits the cache afterwards and
skips its own observer install. The observer records state and authorizes nothing; every override
still needs the worker's complete validation, the switch, the AND3 reply and the regular-player checks.

| Case | Build 152 | Build 153 |
| --- | --- | --- |
| Link, Home | stopped (3 of 3 with 132/143/152) | kept playing, 3 of 3 |
| Feed regular video, Home | kept playing | kept playing |
| Link, screen off | not run | kept playing |
| Switch off, link, Home | not run | stopped (native) |

Shorts are excluded by design and were not counted. Cached cold start is unchanged (80 ms main-thread
discovery, 644 ms to first screen). The startup log adds one line,
`Background playback player observer installed at startup`; all other hook lines match build 143.
