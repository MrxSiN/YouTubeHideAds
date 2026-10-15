# Brainfuck source conventions — normative locally

- A full line beginning with `#` after optional spaces/tabs is ignored entirely; `><+-.,[]` inside a comment does not execute.
- Remaining non-comment lines allow only `><+-.,[]` and ASCII spaces, tabs, CR/LF. Inline `#` is invalid. No executable macros, labels, extended opcodes or comment semantics.
- Required header keys before execution: `@feature`, `@purpose`, `@abi`, `@inputs`, `@outputs`, `@cells`, `@invariant`, `@safety`. `@section` can be repeated. `@note` and `@status` also allowed. Repeated single-use keys fail validation. An optional **header-only** `@fuel N` sets a canonical positive bounded decimal instruction limit (max signed 32-bit).
- UTF-8 text is allowed in whole-line comments, never in executable lines.
- The parser records the original 1-based source line for every Brainfuck instruction; normalization removes all commentary and whitespace.
- Compiler digests are SHA-256 of **only** the normalized 8-op byte stream. An executable change changes the digest, but a comment/layout change does not.
- Semantics: unsigned byte cells wrap modulo 256; tape 4096 bytes initially zero, pointer initially zero, moving beyond either end traps, binary I/O, input EOF writes 0, 100,000 executed ops by default (the timestamp validator declares 2,000,000 explicitly) and 64 output bytes maximum.
- Checked-in feature sources must use real input and output and contain conditional behavior; truth-table checks reject programs whose decisions never depend on validated inputs.
- Each section should describe non-obvious data flow and tape invariants. The public MrxSiN profile served only as a tonal reference, not as a normative grammar.

The test harness may use `parse_source(...,require_feature=False)` for instruction conformance fixtures; the regular `load`/build always uses strict feature validation.
