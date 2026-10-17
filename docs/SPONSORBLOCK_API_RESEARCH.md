# SponsorBlock read API and implementation

Recorded behavior retained in build 77; the live seek evidence was collected on build 39.
This guide is an implementation record, not a fresh query of the upstream service.

Official contract: [SponsorBlock API docs](https://wiki.sponsor.ajay.app/w/API_Docs), consulted
2026-10-16. The shipped XAX client makes read-only requests to the fixed HTTPS endpoint
https://sponsor.ajay.app/api/skipSegments/{sha256HashPrefix}, using four hexadecimal digits and an
encoded categories array. It performs no submissions, votes or account operations.

The response is bounded to 256 KiB, 1,024 video records and 100 segments for the exact local ID.
The accepted VOD duration is at most seven days. Only exact local videoID matches are accepted.
Segments require two numeric seconds values, a supported category, actionType skip and a bounded
hex/hyphen UUID. Negative numbers are rejected before conversion. BigDecimal floors seconds to
integer milliseconds without floating-point multiplication. Missing duration is zero; nonzero
reported duration must match the current player within 1,000 ms.

Brainfuck owns category eligibility, start <= current < end, raw playback-type authorization and
duplicate/enablement gates. XAX validates transport, data provenance, types, current player and
generation, then invokes the resolved typed seek only for an exact BF endpoint reply.

Requests use one worker, CompletableFuture exception handling and connection cleanup. Connect/read
timeouts, byte/read-count/elapsed limits, disabled redirects and one attempt per generation bound
the work. Errors and absent data produce no synthetic segments or seeks. The first implementation
has no cross-video cache or retry; a later playback generation permits another request.

The Pixel retrieved real segments and accepted seeks to 68,509 ms (sponsor, JogMQGLmps8) and
76,737 ms (outro, M7FIvfx5J10). The latter category was initially off and enabled for testing.
The real four-digit bucket held 123 video records; a packaged regression prevents the former
64-record limit from returning empty data. Live playback type 9 was observed without a fetch/seek.

See [architecture](ARCHITECTURE_BRAINFUCK_XAX.md) and
evidence (`remaining_20261016`, removed before 1.0.0). Colored seekbar/overlay UI, submission controls,
channel whitelists and complete upstream SponsorBlock parity are not implemented.

[All setting defaults](README.md#settings-and-defaults): the ad master gates SponsorBlock effective
enablement; its own enable/sponsor/self-promotion defaults are on and other categories default off.
The original-audio feature does not spoof or refetch player responses and adds no SponsorBlock API
operation. AI list caching is independent; it does not imply a SponsorBlock cache.
