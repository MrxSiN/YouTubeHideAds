# Language boundary

The repository is Brainfuck and XAX. Nothing else is authored here: no Java, Kotlin, C, Python, shell
or CI script. The Python-era toolchain and its reports are in [`history/`](history/) and git history.

| What | Language | Where |
|---|---|---|
| Ad decisions, component classification, settings defaults and the master gate, SponsorBlock rules | Brainfuck | `source/brainfuck/`, `source/brainfuck-runtime/` |
| Hooks, DexKit queries, reflection, preferences, the Settings row and page, calling Brainfuck | XAX | `source/xax/youtubehideads.xax` |
| Byte layouts between them | prose contracts | `contracts/`, each `.bf` header |

## What the toolchains contribute

The compilers are other repositories and may use any language; they contribute no feature behaviour.

- **brainfuckC** compiles each policy. Its native code, ELF headers and relocations come from
  Brainfuck stages; its Python only moves bytes. Its `Bfp1Bridge` JNI bridge is C: it `dlopen`s a
  policy, calls `bfc_call_v1`, and copies buffers. It never reads policy bytes.
- **XAX** turns the store into an APK: JVM class files, its own JVM→DEX lowering, the `Module`
  forwarder (`onPackageReady` → the XAX entry, nothing else), a `Bfp1Bridge` class with one
  `static native` method, an `AdBindings` class with one `static volatile Object[]` field, the
  manifest, libxposed metadata and the v2 signature.
- **DexKit** is a third-party library packaged as prebuilt DEX and `.so`.

## Rules the store follows

- XAX never decides whether something is an ad. It reads facts, sends bytes to Brainfuck, and acts
  only on an exact authorized reply. Any other reply, including the empty reply of a failed call, is a
  pass.
- XAX never supplies a default. It sends each stored preference as `(present, value)`;
  `settings_snapshot.bf` decides.
- Presentation strings (titles, summaries) live in the store as text and encode no behaviour.

## Known constraints

- The pinned JVM lowering cannot bind a `boolean` callback parameter, so switches use
  `View.OnClickListener` and read `isChecked()`.
- `ldc` constants are ASCII-only, so the middle dot in summaries is built from code point `0xB7`.
- The bridge `dlopen`s per call; the module `System.load`s every policy at start so that is a
  reference count, not a load.
