# Controlled welcome host-layout fixture

These optional native test transactions start from the final production store in the parent
[manifest](../manifest.json). They do not modify the canonical source or final APKs.
Their [manifest](manifest.json) records exact roots and hashes.

Apply `fixture.batch` and verify, then apply `fields.edit` and verify. Independent native replay
must reproduce the recorded fixture source. The fixture adds an Instrumentation resume hook and
four test fields. Every production function except the startup wrapper and its content-addressed
ancestors retains its exact CID; production scheduling and cancellation functions remain unchanged.

An external ADB driver sets the temporary Global setting `youtubehideads_welcome_fixture_kind`
to `promo`, `onboarding`, `education` or `ordinary` before a cold Music launch. The fixture inflates
Music's corresponding real resource layout and attaches it under the native interstitial container.
Its cancel listener removes the controlled view and restores the container visibility. Its action
listener records a test failure; it has no purchase endpoint. `ordinary` supplies an unmatched
layout identity to the production scheduler. With no mode key, the fixture adds no view.

This proves the production queued cancellation and gates on real Android host layouts; it does
not prove naturally served offers, native controller binding execution or server dismissal state.
The driver's seven cases distinguish automatic cancellation from subsequent manual fixture cleanup.

After testing, delete the temporary mode key, reinstall the ordinary development APK, force-stop
Music and verify final startup contains no fixture hook. Final APK payload checks also require
the fixture class, mode key and controlled-view labels to be absent from generated DEX.
