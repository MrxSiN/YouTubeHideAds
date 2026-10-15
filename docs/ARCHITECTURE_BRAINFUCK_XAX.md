# Architecture — implementation and planned boundaries

```
annotated .bf -> strict source parser -> 8-op stream -> JVM bytecode AOT -> policy JAR (TESTED)
                                                            |
                                                            v
                                   XAX graph host / DEX / APK / Xposed (NOT IMPLEMENTED)
                                                         + DexKit (NOT IMPLEMENTED)
                                                         + SponsorBlock HTTPS (NOT IMPLEMENTED)
```

The JVM class emitter compiles each opcode into explicit bytecode instructions, not an on-device Brainfuck interpreter. For each program, the generated class exposes `public static byte[] run(byte[] input)`. It internally creates a fresh 4096-byte tape, pointer, input cursor, output stream and a finite instruction budget. The compiled class has Java-5 classfile format, verified on this host's Java-21 runtime; D8 compatibility is **unverified**.

`--optimize` coalesces runs of `+` and `-` while preserving 8-bit wrap and the original command fuel count. Large programs also compact same-direction pointer runs with a resource guard that preserves the original **fuel-versus-pointer-bounds** error precedence; this compilation-preserving size reduction is mandatory even in baseline mode when a large method requires it. Bracket targets are lowered to JVM conditional branches. Use the interpreter as an independent behavior oracle.

The host architecture is a **design**, not an existing XAX graph. It must receive raw, validated low-level facts, invoke the Brainfuck-generated policy and validate return actions. It must not embed independently authored ad-identification predicates. The current `.bf` files are small building blocks, not claims of comprehensive player/feed/SponsorBlock policy coverage. Future evidence matching must be sent to Brainfuck in feature-neutral fields, rather than passing the result of a host-side ad classifier.

Each binary policy class is named `org.youtubehideads.bf.<feature>` and supports the same method signature, but Android integration requires proof of class linkage from XAX-generated DEX. No JNI, hook, or network client is currently shipped.
