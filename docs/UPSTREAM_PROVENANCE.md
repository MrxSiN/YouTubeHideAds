# Provenance and licenses

- BrainfuckC: external local checkout `D:\GitHub\brainfuckC`, used on
  2026-10-16 through `bootstrap.run_policy_native.PolicyCompiler`. Its inspected
  `LICENSE` is MIT, copyright 2026 brainfuck-native contributors. No upstream
  compiler source or seed binary was copied into this project or modified.
  The compiler manifest records SHA-256 hashes for its adapter and BF stage
  sources; this local snapshot has no verified Git revision. The selected
  Windows path executes upstream BF stages using upstream `seed.exe`.
  Generated native instruction templates originate in that compiler. A copy
  of its license accompanies the build/evidence; this is not the newer dynamic
  DSO backend. See `docs/BUILD.md` for scope and limits.

- XAX: [MrxSiN/XAX](https://github.com/MrxSiN/XAX), research read at SHA `9e44eedfc241d25bb5062b38af105f75234000e2`. Its normative no-text-syntax spec and compiler source were inspected remotely. **No XAX source/assets/runtime were copied.** No root `LICENSE` was found via GitHub contents at this SHA: do not assume redistribution permission.
- Morphe: [MorpheApp/morphe-patches](https://github.com/MorpheApp/morphe-patches), code inspected at `e5464395441e916b643af4e2175c4e253e6df487`. The `HideAdsPatch`, `AdsFilter`, SponsorBlock, fingerprints, and ChannelWhitelist sources were read as behavior references. Morphe is GPL-3.0 and its NOTICE includes GPL section-7 notices. **No implementation source was copied** into this independent repository; those notices must accompany any future actual adaptations under their terms.
- DexKit: [LuckyPray/DexKit](https://github.com/LuckyPray/DexKit); upstream README describes C++ DEX resolver, LGPL-3.0 and Maven `org.luckypray:dexkit`. Research only; not bundled.
- libxposed/Vector: specific integration assertions above come from the pinned XAX `xax_libxposed.py` and Android integration documentation, not from a local framework test.
- SponsorBlock: mentioned by user specification; no client code copied, no API calls verified.

The new project's Brainfuck programs, standalone direct bytecode emitter, test infrastructure and docs were authored independently for this greenfield project. GPL-3.0-or-later governs newly authored material here. License compatibility and notices must be re-audited before integrating binary or adapted third-party components.

## Iteration 2 (2026-10-15) — XAX licensing and runtime verification gate

Queried the GitHub REST repository metadata and pinned revision file listing for `MrxSiN/XAX`: the repository metadata returns `license: null` and a `LICENSE` lookup returned 404. Neither observation grants redistribution or adaptation permission. XAX sources were **not** copied, vendored, redistributed, or treated as an implicit new project license. Any future use must distinguish use of an externally provisioned permitted compiler from redistribution of compiler/runtime pieces. The pinned candidate remains `9e44eedfc241d25bb5062b38af105f75234000e2` until a licensed, locally testable build is available.

The new v1 host framing is independent work: no Morphe or XAX runtime code has been copied into its codec, JVM linkage test, or golden fixtures.
