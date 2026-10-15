# Brainfuck ABI and host framing

The inner, tested ahead-of-time JVM interface is `public static byte[] run(byte[] input)`; the output is executable Brainfuck computation, not XAX policy code. Cells wrap modulo 256 with explicit tape and fuel budgets.

**Iteration 2 adds an executable, versioned offline binary ABI conformance harness.** The complete normative framing, field offsets, stable feature IDs, generation guards, authorization rules and error cases are in [`contracts/bf_host_v1.md`](../contracts/bf_host_v1.md). Its Python codec and JVM linkage checker are compiler/test tooling **not an Android implementation**. The future XAX semantic host must reimplement these checks, and actual Android/Vector device tests remain undone.

- Request: 14-byte packed header `BFH1`, major/minor, u16 ID, u32 generation, u16 length; followed by <=256 bytes.
- Reply: 15-byte packed header `BFR1`, major/minor, u16 ID, u32 generation, u8 action, u16 length; followed by <=256 bytes.
- The input byte count is **derived from executable comma count**, not annotated metadata. Nine policies consume Boolean-only bytes (including the new category classifier, which consumes 16 interleaved Boolean bytes with a one-hot selector). The other SponsorBlock seek policy consumes six Boolean bytes followed by one binary u64 in little-endian order; comments cannot influence either program.
- The host must reject invalid lengths, non-Boolean gate fields, out-of-range timestamps, stale generations, forged action codes and object mismatches without mutating YouTube.
- `SEEK_PLAYER` now has a Brainfuck-emitted, source-attested 64-bit end-position payload (`authorize_seek.bf`: 6 Boolean gate bytes + 8 endpoint bytes in; 1 or 9 bytes out). Positive seeks are **still not deployable**: the offline boundary rejects actual invocation until a verified XAX player host exists.

Conformance source: [`testdata/bf_abi_v1_vectors.json`](../testdata/bf_abi_v1_vectors.json); real compiled-JVM exercise: `tests/test_host_link.py`. A generated JAR that no longer exactly matches its `.bf` source is rejected before it can serve the bridge.

## Iteration 6: Brainfuck-owned category selection and causal handoff

`0x0402 select_sponsor_category`: 16 Boolean input bytes: for each of `sponsor`, `selfpromo`, `interaction`, `intro`, `outro`, `preview`, `filler`, `music_offtopic`, supply `[auto_skip_enabled, category_selected]`. Exactly one of the eight selector bytes must equal `01`; the ABI validator checks shape only. The Brainfuck instructions emit `PASS=0` or `CATEGORY_AUTO_SKIP=5` from the selected category's setting. All 2,048 valid combinations pass reference and compiled-JVM differential tests in both modes.

The category action is the *only authorized source* for the subsequent `authorize_seek` category Boolean (input byte 1). `checked_sponsor_chain` verifies paired feature IDs, generation, valid input shapes, action boundaries and matching category result. It is a testing oracle and **does not execute Android seeks**. The actual Android semantic bridge is still unimplemented.

## Iteration 13 one-call SponsorBlock feature (`0x0403`)

Eleven features now exist. `sponsor_skip_pipeline.bf` takes 29 bytes: 16 interleaved category Booleans, five runtime evidence Booleans, and eight endpoint bytes. Category eligibility and seek conjunction occur in the same Brainfuck stream. The separate `0x0401`/`0x0402` pathway remains supported for backwards-compatible off-device tests, not preferred for future runtime routing. `SEEK_PLAYER` is still rejected by the offline host, and raw time-window computation is still missing.
