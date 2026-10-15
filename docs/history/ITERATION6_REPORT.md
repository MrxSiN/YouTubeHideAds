# YouTubeHideAds — Iteration 6 evidence

## Scope and measured result

On 2026-10-15 the repository was continued from Iteration 5 (`0bd892f`). This iteration adds **one more genuine source-owned Brainfuck policy**, `source/brainfuck/sponsorblock/select_sponsor_category.bf`, bringing the inventory to **ten** policies. It compiles into `public static byte[] run(byte[])` bytecode just like the existing programs and emits its decisions from eight-command Brainfuck alone.

Command: `./scripts/build_fresh.sh` on Linux x86_64, Python 3.13 and local Java/Javac. Exit status **0**. `python3 -m unittest discover -s tests` reports **54 tests passed**. Both optimized and non-optimized JARs rebuild reproducibly and pass the full policy-source/JVM class identity verifier. This is an offline compiler/conformance milestone, **not** an Android runtime milestone.

Generated original JAR SHA-256: `30cf5ed83ff0c340b82cd0b743405d7815219c36d623b78f16d786445f732ab8`.
Generated optimized JAR SHA-256: `be5809c8fd4800aab0b267a9edc5abcafcdc10481b7086f47b953b6c2b9d9ad4`.
Evidence: `YouTubeHideAds_iteration6_full_build.log` alongside the packaged project, `testdata/bf_abi_v1_vectors.json`, `generated/policies.json`, `generated-optimized/policies.json`, and `generated/language_audit.json`.

## What changed

- New **Brainfuck-owned SponsorBlock category selection** using eight stable wire-category slots (`sponsor`, `selfpromo`, `interaction`, `intro`, `outro`, `preview`, `filler`, `music_offtopic`). One-hot selection is an ABI *shape* constraint; all category allowance decisions come from the actual `.bf` instructions, not a Python/XAX category table.
- Introduced the stable feature ID `0x0402` and the result code `CATEGORY_AUTO_SKIP=5` without renumbering existing actions or changing the outer v1 request/reply framing.
- Added offline `checked_sponsor_chain` to require both feature IDs, matching generation, valid one-hot/category inputs, and an `authorize_seek` category gate matching the preceding BF category decision. The checker cannot execute a seek or attest runtime XAX invocation.
- Verified **all 2,048 valid category/setting combinations** through the reference interpreter and through both directly compiled JVM variants. Added invalid length/Boolean/one-hot, forged category, stale generation, forbidden-action, comment-invariance and executable-mutation tests.
- Updated source digest/golden ABI vectors, auto-discovered ten-class D8/DEX expectations, CI-compatible tests, documentation, and language-boundary report.

## Blockers and nonclaims

- **Not executed:** pinned XAX compiler build, canonical XAX Android host graph, actual D8, Android SDK tools, ADB, Android/ART/Vector, libxposed lifecycle in an Android process, DexKit, YouTube ad suppression, SponsorBlock HTTP and seeking.
- The local prerequisite probe reports XAX/D8/SDK/ADB absent. The upstream XAX redistribution license remains unresolved; no upstream XAX source or binary was bundled.
- Although category eligibility is now source-owned, `authorize_seek` still consumes a prevalidated temporal-window Boolean rather than comparing raw video position/start/end itself. No claim of complete SponsorBlock functionality or YouTube compatibility is made.
- `tests/test_dex_link.py` uses deliberately **noninstallable synthetic DEX fixtures** and a fake D8 command. Passing these tests does not prove that a real Android APK can run or that an XAX caller invokes any of the ten BF classes.

## Next critical work

With a legally usable pinned XAX checkout and Android build tools, exercise `./scripts/link_xax_smoke.sh` to build an actual canonical semantic store and unsigned DEX artifact, inspect complete method definitions, then author an XAX semantic platform dispatcher that invokes source-attested BF `run([B)[B`, applies generic framing and action checks and proves the category-to-seek handoff. After that, a controlled libxposed device/Vector test and dynamic DexKit YouTube discovery are required. No hardcoded obfuscated YouTube endpoint is acceptable as a substitute.
