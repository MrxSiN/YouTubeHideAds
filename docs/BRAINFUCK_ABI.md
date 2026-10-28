# Brainfuck runtime ABI

Current release 1.0.0 packages 9 policy libraries plus the JNI bridge and DexKit. The seven AND3 rows below all call `liband3.so` ([and3.bf](../source/brainfuck/and3.bf)); their names are semantic call sites, not separate libraries. This is the shipped
runtime contract. [Build identity](../evidence/ai_audio_branding_20261018/build.json).

The shipped XAX host calls external Bfp1Bridge.run(libraryPath,input,output,tape,budget,used).
Each library exports bfc_call_v1. A call uses a fresh 4,096-byte tape, a 64-byte output buffer
and a 2,000,000-loop budget. Since build 135 the host passes the policy name (`and3`), which the
bridge resolves to `lib<name>.so` in its own directory and caches; the bridge zeroes a native tape
of the Java tape's length per call, so the host shares one tape array. [Details](../evidence/device_perf_20261028/README.md). Only status zero and an exact expected reply authorize an action.
Cells wrap modulo 256. Whole-line annotations are stripped before compilation.

| Policy | Input | Reply |
| --- | --- | --- |
| settings_snapshot | Five (present,value) Boolean pairs | Five raw switches, then four master-gated switches |
| ad_component | 54 bytes, ordered by contracts/ad_component_inputs.json | 01 suppress or 00 pass |
| ad_panel | Popup enabled, Premium enabled, PAproduct fact, jumpahead fact | 01 suppress or 00 pass |
| ad_fullscreen | Popup enabled, _interstitial marker, already-gated component decision | 01 iff (popup AND marker) OR component decision; otherwise 00 |
| suppress_video_slot | Enabled, structural ad fact, safe transition, whitelist | 01 suppress or 00 pass |
| suppress_shorts_slot | Effective video-ad gate, native Shorts ad evidence, current context valid | 01 suppress or 00 pass |
| suppress_premium_upsell | Enabled, marketing fact, not subscription management | 01 suppress or 00 pass |
| sponsor_settings | Master, nine (present,value) pairs | Nine raw switches, then master AND SponsorBlock enabled |
| sponsor_time_window | Three little-endian u64 values: start/current/end milliseconds | 06 iff start <= current < end; otherwise 00 |
| sponsor_skip_pipeline | 16 category bytes, five context bytes, eight endpoint bytes | 04 plus the original endpoint, or 00 |
| suppress_playables | Own preference, games fact, validated component | 01 remove or 00 pass |
| authorize_player_swipe | Own preference, fullscreen state, validated vertical intent | 01 handle or 00 pass |
| suppress_feed_section | Own preference, section fact, validated feed context | 01 remove or 00 pass |
| filter_ai_channel | Selected list enabled, whole-handle membership, validated own card | 01 remove or 00 pass |
| select_original_audio | Enabled, unique original, current audio context | 01 select or 00 pass |
| authorize_background_playback | Own switch, validated restriction gate, validated playback/settings/experiment context | 01 permits only the scoped capability override; otherwise native behavior |

Sponsor category order is sponsor, selfpromo, interaction, intro, outro, preview, filler,
music_offtopic. The 16 bytes interleave configured category and one-hot category selector.
The five context bytes are enabled, matching generation, BF window accepted, **raw playback type**,
and not previously skipped. Only playback type 01, calibrated against ordinary VOD on the Pixel,
passes. Other byte values reject. This extends the former Boolean non-live input without changing
its behavior for 00/01.

The host accepts nonnegative signed-long-compatible timestamps, validates the API schema, floors
decimal seconds to milliseconds, checks the reported duration against the player within 1,000 ms,
and bounds the endpoint by the player duration. The window reply must be exactly 06; the pipeline
reply must be exactly 04 plus the same eight endpoint bytes. Immediately before invoking the typed
seek method, the host rechecks the active video ID and playback generation on the main thread.
UUIDs are marked skipped only after the player accepts the seek.

The Shorts policy also authorizes feed-entry removal. XAX obtains native video/image ad facts
from typed endpoint helpers before pager insertion. It copies endpoint and tracking lists together,
or filters whole response records before those lists are derived. Brainfuck receives a validated
feed context; removal does not require a loaded next item or move the pager.

## Playables and fullscreen swipe gates

Both call the shared `liband3.so`; no interpreter or extra native dependency ships.

| Policy | Input | Reply |
| --- | --- | --- |
| suppress_playables | Own enabled preference, structural games fact, validated component context | 01 remove or 00 pass |
| authorize_player_swipe | Own enabled preference, WATCH_WHILE_FULLSCREEN, validated vertical intent | 01 handle or 00 pass |

Both features default on and are independent of the ad master. XAX derives layout facts and
performs Android effects. The native reply must be exactly one byte, 01. Fixture data is in
[testdata/playables_vectors.json](../testdata/playables_vectors.json) and
[testdata/player_swipe_vectors.json](../testdata/player_swipe_vectors.json).

## Feed section gate

suppress_feed_section takes three Boolean bytes: own enabled preference, structural section fact,
and validated feed context. Exactly 01 removes the component; all other replies preserve it. The
annotated program reuses the existing compiled AND3 command stream and has its own library path.
Four independent settings use the existing preference/reset helpers; defaults and identifiers are
specified in [feed_section_inputs.json](../contracts/feed_section_inputs.json). All eight native
gate combinations and 64 host classifier/default/scope/decision cases run at startup; the fixture
is [feed_section_vectors.json](../testdata/feed_section_vectors.json).

## AI channel and original-audio gates

Both new libraries reuse the identical compiled AND3 instruction stream after checking authored
commands and all eight Boolean inputs for each. Each has a separate semantic path and requires an
exact one-byte 01 reply. Inputs are Boolean bytes; host facts are validated before invoking them.

| Policy | Inputs | Effect |
| --- | --- | --- |
| filter_ai_channel | selected list enabled, whole handle membership, validated own video card | Typed EmptyComponent replacement |
| select_original_audio | enabled, unique non-dubbed original track, valid current audio context | Typed original-ID setter |

Contracts: [AI](../contracts/ai_channel_inputs.json), [audio](../contracts/original_audio_inputs.json).
Fixtures: [60 AI/audio startup cases](../testdata/ai_audio_vectors.json). Defaults are AI false/false,
original audio true, independent of the ad master. Cache/selection state belongs to XAX; neither BF
program knows Android, networking, strings or YouTube class names.

## Source and input inventory

Background playback also uses the unchanged `liband3.so` command stream and existing 4,096-cell
JNI ABI. Its 28 packaged checks cover all eight native Boolean inputs and host context/flag cases.
The [contract](../contracts/background_playback_inputs.json) defines its independent default and
validated effects. Current BBC shared libraries require 65,536 cells and ignore the loop budget;
they must not replace this pinned JNI input without a separate ABI migration.

All 9 libraries above are listed by digest in the canonical store; this is not an on-device BF
interpreter. There is one authored BF file per library. Unshipped feed/search/shopping, resolver,
cleanup and older SponsorBlock building blocks were removed; Git history keeps them.
Settings/defaults and master dependencies are listed in the [documentation index](README.md#settings-and-defaults).
