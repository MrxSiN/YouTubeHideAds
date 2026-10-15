# XAX source

`youtubehideads.xax` is the module's canonical XAX store: the whole Android side. It is binary on
purpose. XAX programs are semantic graphs, and the verified store is the source.

- 21 functions: the libxposed entry, the focus hook, the Settings row and page, the five ad hooks
  and their DexKit discovery, the preference snapshot, and `bf`, which calls one Brainfuck library.
- An `android-libxposed-jvm-module-v1` record: package `org.youtubehideads.module`, scope YouTube,
  versionCode 27, the signer's certificate SHA-256, and the BLAKE3 of every DEX and `.so` packaged.
- libxposed API 102 metadata.

Read it with XAX-MCP (`xax_workspace open`, `xax_query`). Build and change it as in
[`docs/BUILD.md`](../../docs/BUILD.md).
