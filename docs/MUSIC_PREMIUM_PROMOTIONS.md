# YouTube Music Premium promotions

Build 162 adds [separate download modes and export](DOWNLOADS.md). The promotion switch described
here still controls promotional UI; download modes have their own independent settings.

Development build 161 adds the native welcome-offer layout family to the same switch. It invokes
the matched view's native cancel action after attachment. The audio/video trial BottomSheet remains
outside this implementation. [Welcome contract](../contracts/music_welcome_inputs.json).

Development build 160 extends Music's existing **Premium promotions** switch to the Upgrade tab,
Get Music Premium account entry, membership upsell label and promotion mealbar. Existing component
and fullscreen promotion filtering remains in place. The switch is on by default and follows the
Music Hide ads master. Restart Music after changing it so native views are reconstructed.

## Shared architecture

Music uses the existing settings scaffold, package-local preference file, complete BF ad snapshot,
typed AND3 authorization, protective API 102 hook installer and startup DexKit session. No additional
preference or page is introduced. YouTube's feature startup remains separate. New host logic is
canonical XAX; the unchanged packaged Brainfuck AND3 policy authorizes every suppression.

The gate validates the complete nine-byte ad snapshot and reads effective Premium byte 7, already
computed by BF from the master and saved Premium preference. Inputs are effective enablement,
matched surface and validated context. Only status zero and exactly one byte `01` permit an effect.
See the [contract](../contracts/music_premium_inputs.json) and
[vectors](../testdata/music_premium_vectors.json).

## Structural discovery

- Account: unique no-argument void method referencing both public Music history and offline browse
  identifiers; its unique used instance field typed exactly View supplies the promotion container.
- Membership: unique CharSequence getter with the reference opcode sequence, correlated with a
  unique field used by that account method. Authorized results become null after the original call.
- Navigation: resolve the enum containing `TAB_MUSIC_PREMIUM`, its unique public static int converter,
  then its unique public final one-reference-argument void caller using visibility, findViewById and
  ArrayList construction. Used fields connect controller, model list, route-to-tab map, model payload
  and tab view. Only that enum value under a Material TabLayout is hidden.
- Mealbar: the public MusicActivity View getter must return the named `floating_layout`. A weakly
  held root and global-layout listener inspect its first child, require the named
  `mealbar_layout_root`, then the promotion profile (inner LinearLayout, first visible ImageView).
  Only that matched child is hidden; other floating UI is preserved.
- Native welcome offer: uniquely anchor the overlay controller by its parameter marker, shorty and
  opcode prefix; follow its unique invoked public final one-reference-argument void binding method.
  Its owner must have unique non-static View and int fields. That int must resolve to the named
  `interstitial_promo_view` or `onboarding_interstitial_promo_view` resource at runtime.

The welcome callback runs the original binding first and posts one Runnable against a weakly held
candidate. After attachment it requires the main thread, named `layout_container` root, a named
`interstitials_container` ancestor within six views, title/body/action/dismiss TextViews and a
ScrollView. The enabled cancel control must have a click listener. A fresh shared BF gate then
authorizes `dismiss.performClick()`. The purchase control is never invoked. Native cancellation
owns overlay cleanup; the module does not leave a hidden container or take over navigation.
The education interstitial layout is excluded. Role discovery bounds invoked methods and declared
fields at 64, and direct caller deoptimization at 128. Unexpected welcome failures clear only its
own readiness and leave existing Music startup intact.

Named view checks resolve resource IDs through Music's Resources and package, then compare IDs.
Unnamed/generated views are skipped without querying nonexistent resource names.

Discovery inspects at most 256 field references per role, deduplicates before uniqueness checks,
and bounds direct callers at 128. Navigation inspects at most 16 models and four ancestor views.
View changes require the main thread. A maximum of 64 weakly held views retains original visibility
for restoration on subsequent bindings. There is no strong Activity reference or polling worker.
The listener detaches from a previous live observer when its weak root changes.

Readiness remains false until self-checks, role correlation, deoptimization and all four protective
hooks complete. A synchronous completed-future guard isolates discovery and layout exceptions from
Music ads, background playback and settings startup. Unsupported or ambiguous roles preserve native
behavior. Missing view/model matches skip only that candidate. No numeric resource IDs, obfuscated
member names, localized labels or version offsets select production hooks.

## Reference and limits

The runtime adaptation follows Morphe commit
[`44031c5`](https://github.com/MorpheApp/morphe-patches/tree/44031c561ea048c8f196877f30a49c13bfd6afb6),
particularly [Music HideAdsPatch](https://github.com/MorpheApp/morphe-patches/blob/44031c561ea048c8f196877f30a49c13bfd6afb6/patches/src/main/kotlin/app/morphe/patches/music/ad/HideAdsPatch.kt)
and [navigation buttons](https://github.com/MorpheApp/morphe-patches/blob/44031c561ea048c8f196877f30a49c13bfd6afb6/patches/src/main/kotlin/app/morphe/patches/music/layout/buttons/navigation/NavigationBarPatch.kt).
No Morphe application implementation or APK patcher is bundled.

This hides recognized promotional surfaces; it does not provide a subscription or unlock paid
downloads, DRM content or other server entitlements. A separate audio/video-switch trial dialog
observed in Music 9.45.51 uses `upsell.eml` and Material BottomSheet rather than the reference
mealbar; it remains unsupported. Arbitrary future or server-selected purchase UI is not covered.
Build 160 observed a native full-page welcome offer ("Now with 100 million songs") and manually
dismissed it during acceptance. Build 161 adds its native promo layout family as described above.
Natural mealbar presentation depends on the account/server. Requirements and controlled fixtures
must not be reported as naturally observed device positives.

[Native transactions](../source/xax/transactions/music-premium-20261116/README.md) ·
[Build and device evidence](../evidence/music_premium_20261116/README.md)

[Welcome extension transactions](../source/xax/transactions/music-welcome-20261117/README.md) ·
[Welcome extension evidence](../evidence/music_welcome_20261117/README.md)
