# YouTube Premium promotion coverage

Development build 162 extends the existing default-on **Premium promotions** switch. It removes
the Premium action in the You-page header while retaining ordinary Subscribe and other actions.
It also recognizes a promotion by its own typed thumbnail payload, Premium leaf marker and
YouTube promotion image origin. Hide ads remains the master gate. This changes promotional UI;
it does not grant account entitlements or remove every server-generated purchase surface.

The shared component callback uses a fresh Brainfuck ad snapshot. The header decoder is discovered
through the host's buffer-reflection and serialization relationship. It rewrites only the immediate
matched action wrapper, preserving the rest of the header. A malformed, duplicate, ambiguous or
over-budget payload returns unchanged. Bounds are one MiB at the root, 64 KiB per button,
256 bytes per leaf, depth 12, 8,192 parser steps, and a breadth-first limit of 512 nodes/four MiB.
The [contract](../contracts/youtube_premium_inputs.json) records field numbers and exclusions.

The behavior reference is Morphe's AdsFilter/LayoutComponentsFilter at
[`31234a8465683a389bcfba25ad636fd1cd38fd02`](https://github.com/MorpheApp/morphe-patches/tree/31234a8465683a389bcfba25ad636fd1cd38fd02).
Implementation is native XAX with existing BF authorization and the established guarded startup,
typed payload and EmptyComponent architecture. Music's native welcome/account/navigation controls
remain described in [Music Premium promotions](MUSIC_PREMIUM_PROMOTIONS.md).
