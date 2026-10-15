# Device acceptance protocol (not executed)

Preconditions: a build signed via verified XAX Android pipeline; stable user-configured Vector/modern libxposed installation; permission to install packages and inspect logs; a backup or test device. Do not assume a device is ready solely because `adb` is connected.

1. Record exact Android API level, ABI, rooted framework version, Vector state, YouTube package/version, base+split APK hashes, module APK digest, BF policy JAR and canonical XAX store digests.
2. Validate module manifest and modern libxposed `META-INF/xposed/java_init.list`, target scope only `com.google.android.youtube`. Confirm manager and framework identify the same module.
3. Launch YouTube with module disabled, capture baseline startup and playback. Enable and scope module; relaunch. Verify no other process is hooked and no crash/boot loop occurs.
4. Force a known synthetic host event into a test-only endpoint to verify Brainfuck output propagates to typed Xposed action. A genuine ad must be removed only after real structural evidence and hook end-to-end tracing.
5. Exercise pre-/mid-/postroll, ad pods, home/feed/search/Shorts/promotion/shopping. For each observation record method/renderer identity, event payload evidence, BF source SHA and output, action handle and UI/playback result.
6. Exercise disabled flags, ambiguous resolver candidates, split APK changes, stale cache, negative classes, rapid video switching, per-Short whitelist resets, and orphaned containers. No uncertain target may receive a destructive hook.
7. Exercise SponsorBlock network offline and online, overlapping segments, disabled category, manual/auto behavior, backwards seeking, livestream, aborted and stale responses. Verify that the BF program determines if and where to seek.
8. Verify preferences, process restart, module reload, hook cleanup, timestamp precision, memory, and per-hook timing. Capture failures and pass/fail artifacts for each test separately.

**Status: all steps NOT RUN.**
