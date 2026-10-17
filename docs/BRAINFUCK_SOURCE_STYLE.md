# Brainfuck source conventions

Current source is annotated eight-command BF. Metadata describes the program; it does not execute
or grant host authorization. The external build uses --annotated to strip whole-line comments.
There is no repository parser/test harness implementing the older strict metadata API.

## Executable commands

- A full line beginning with # after optional spaces/tabs is ignored entirely, including any BF
  punctuation inside the comment. This includes shortcut: notes and section descriptions.
- Other lines contain only ><+-.,[] and ASCII whitespace. No inline #, macros, labels or extended opcodes.
- Normalize by removing whole-line comments and whitespace. Compare the remaining command stream
  when reusing a compiled native policy. A comment-only edit leaves that stream unchanged.
- UTF-8 text is allowed in whole-line comments, not executable lines.

## Annotation convention

Headers document @feature, @purpose, @abi, @inputs, @outputs, @cells, @invariant and @safety.
@section may repeat for non-obvious data flow. @note, @status and historical @fuel annotations provide
context; they do not change the native call's runtime budget. Existing files are not evidence that
all metadata is checked by the external annotated compiler. Validate the actual commands and ABI.
A known limit should use a whole-line `# shortcut: <limit>; <when to upgrade>` comment.

## Runtime semantics

The shipped native ABI uses wrapping byte cells, a fresh 4,096-byte tape, a 64-byte output buffer
and a 2,000,000-loop budget supplied by XAX. Only exact successful replies authorize actions.
Input Boolean/length validation belongs to the host contract.

After executable edits, compare reference and compiled behavior on meaningful cases, including
invalid-context/disabled paths. AND3 aliases require command-stream equality and all eight Boolean
inputs through the packaged JNI boundary. Keep fixtures as data and use external test tooling;
do not restore the removed Python/JVM harness into this repository.

[Native ABI](BRAINFUCK_ABI.md) · [Testing and fixtures](TESTING.md)
