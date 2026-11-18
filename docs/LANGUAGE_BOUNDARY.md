# Language boundary

Build 161's welcome discovery, queued callback and typed cancel effect are native XAX graph edits;
the existing BF gate authorizes the action. Its controlled host-view harness is a separate native
test graph, with controlled click listeners, and is excluded from final APKs. External drivers only
transport native edits, package inputs, operate ADB and collect evidence.

Build 160's Music promotion controls extend the canonical graph through native XAX batches and
reuse the unchanged Brainfuck AND3 gate and BF ad snapshot. New JSON contracts, static XML text
and packaging metadata are data. [Design and bounds](MUSIC_PREMIUM_PROMOTIONS.md).

Build 159's Music background feature is authored as native XAX transactions and reuses the unchanged
Brainfuck AND3 policy. Its declarations, exact-root batches, metadata and branding inputs are checked
in for review and replay; native edit and mandatory verification produce canonical source. External
SDK use is read-only inspection and declaration/metadata serialization, never application lowering
or an implementation in another language. [Design](MUSIC_BACKGROUND_PLAYBACK.md).

Build 158's Music hooks and settings are native XAX semantic edits; ad authorization reuses the
unchanged AND3 and fullscreen BF policies. Static XML labels and JSON contracts/vectors are data.
Checked-in native batches are exact-root mutation transport for the canonical store, not a separate
source language. Native verification precedes publication, and the compiler builds the APK natively.
The external SDK only inspects/serializes declarations and packaging/edit carriers; no application
implementation in another language is added. [Music design](MUSIC_ADS.md).

Background playback remains in the canonical XAX store and the existing authored AND3 BF policy.
New contracts, fixtures and packaged attribution are data. Its typed graph transport, BBC/compiler
invocations and device test drivers were kept outside this repository. Native/JNI/third-party DEX
inputs are unchanged. [Design](BACKGROUND_PLAYBACK.md).

All application implementation is **Brainfuck and XAX**. The source tree contains nine BF files,
one canonical XAX store, and static XML resources. JSON contracts/fixtures and prose are data.
No Java, Kotlin, C, Python or shell application source is tracked; `Release CI` fails if one appears.
The two GitHub Actions workflows only check the repository and verify and mirror the published APK;
they build nothing and take no part in the module. External tool sources used for build 153 (the
JNI bridge rebuild and carrier-edit transport) are kept outside Git in the ignored `build/` folder,
recorded by hash in the [build 153 record](../evidence/device_perf_20261028/build.json). Earlier
conventional-language implementations remain in Git history.

| Responsibility | Owner |
| --- | --- |
| Native removal/gesture/selection authorization, ad/SponsorBlock snapshots, category/window rules | Authored BF policies |
| Hook lifecycle, structural discovery, fact extraction, typed Android effects, preferences, bounded HTTPS/JSON and caches | Canonical XAX store |
| Title, description, adaptive/monochrome icon, slider and menu shapes/layout, translated strings and manifest resources | Static XML in source/branding |
| Byte contracts and expected vectors | contracts/ and testdata/ |
| BF compilation, JNI transport, third-party libraries, APK lowering/signing | External tools and pinned prebuilt inputs |

XAX validates shape, identity, scope, thread and freshness, derives bounded structural/membership
facts and calls the appropriate BF library. Only status zero and an exact expected reply authorize
an effect. Failure preserves content or declines a seek/gesture/selection. This is a validation
boundary, not a claim that string parsing or structural classification happens inside BF.

Ad and SponsorBlock defaults and master gating are computed by BF snapshots. Independent Playables,
feed, AI and player preferences use XAX/Android defaults; final authorization remains in BF.
[All defaults and master dependencies](README.md#settings-and-defaults).

## External contributions

- BBC (formerly BrainfuckCC) compiled BF into the shipped AArch64 bfc_call_v1 libraries. Its external generic C JNI bridge loads
  a library, moves byte buffers and calls the policy; it contains no YouTube feature classification.
- XAX emits application JVM/DEX and the libxposed lifecycle/native declarations and state holders.
  The branding-v2 profile packages a digest-pinned resource archive, metadata and native inputs and
  signs the APK. No app Java/Kotlin source is generated into this repo.
- DexKit, flatbuffers and Kotlin runtime are prebuilt third-party dependencies, not application
  implementation source. The APK's native bridge and DexKit are external binary dependencies.
- AAPT2 compiles static XML branding only. D8 was used once for third-party DEX, not XAX app code.

The external profile adds no YouTube policy. Its two local compiler modifications and snapshot
requirement are recorded in [BUILD.md](BUILD.md) and [toolchain evidence](../evidence/ai_audio_branding_20261018/toolchain.json).
A clean base compiler checkout cannot rebuild the branded store by itself.

## State and constraints

Generated AdBindings, PlayerBindings, SponsorBindings, ShortsBindings, PlayablesBindings,
SwipeBindings, FeedBindings, ExtraBindings and SponsorUiBindings hold the typed host state. They do not replace the
BF authorization checks. The parser/dialog share component fact extraction; panels use a typed ID
helper. AI reads only the candidate's own bounded payload; audio uses validated current bindings.

The pinned lowering cannot bind a boolean callback parameter, so switches use View.OnClickListener
and isChecked(). Its ldc text is ASCII-only; non-ASCII values use constructed code points/decoded
UTF-8 data. Policy libraries are loaded at startup; per-call bridge loading retains references.
[Native byte ABI](BRAINFUCK_ABI.md) and [source conventions](BRAINFUCK_SOURCE_STYLE.md) describe
current behavior.
