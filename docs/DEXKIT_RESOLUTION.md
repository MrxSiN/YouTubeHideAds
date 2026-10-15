# DexKit dynamic resolution (design only)

Target library: `org.luckypray:dexkit`, evaluate version 2.3.0. DexKit's current documented API supports multi-condition class, method and field searches, plus batched string searches. Neither a dependency nor a XAX binding has been linked to this repository.

Candidate identity must include app version, base + split APK DEX content identities, module/resolver schema, and the digest of its owning `.bf` policy. Lookup order: valid cache -> bounded structural query -> candidate validation -> Brainfuck-owned scoring/rejection -> unique descriptor persistence -> typed Xposed hook installation. Do not use obfuscated method names as sole evidence; require unique structural signals. Ambiguous/missing candidates must disable the particular feature.

Examples for **research only**, not claimed live fingerprints: Morphe's `LoadVideoAdsFingerprint` uses two string literals; `GetPremiumViewFingerprint` has a named measurement method plus instruction pattern; `PlayerOverlayTimelyShelfFingerprint` combines a string and call structure. Pinned sources listed in `MORPHE_AD_PATCH_INVENTORY.md`. No YouTube DEX was supplied to test them, and no resolver targets were verified.
