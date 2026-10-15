# Proposed generic XAX host operations — NOT IMPLEMENTED

This is an interface-design register, not canonical XAX semantic state or a deployable implementation.

All capabilities are narrowly typed and bounded. In particular, do not expose an open-ended reflection or network operation to Brainfuck without strict allowlists, object-generation checks, byte limits and thread restrictions.

| Proposed capability | Boundary validation | Side effect |
| --- | --- | --- |
| `query_members(role, criteria)` | bounded query count, allowed target package, resolver generation | DexKit lookup (background) |
| `validate_member(handle, expected_shape)` | ClassLoader, signature, return/parameter type, package identity | none |
| `install_hook(descriptor)` | no duplicate, unique verified method, type safety | hook target process only |
| `read_component_descriptor(handle)` | immutable structural fields only; avoid raw object escape | none |
| `apply_action(action, handle, generation)` | Brainfuck decision plus validated type, thread, generation and reversible fallback | conditional host mutation |
| `seek_player(target_ms, video_generation)` | Brainfuck-supplied target, valid player state, current video, bounded seek | player seek |
| `fetch_segments(video_id,categories)` | URL allowlist, HTTPS, timeouts, rate-limits, privacy | async network/cache |
| `preferences_snapshot()` | schema, size, monotonic generation | none |
| `diagnostic(event)` | redacted fields; no raw video ID/history | bounded logging |

No capability has an XAX implementation, runtime signature, linker identity or device validation yet. All remain proposals. See `docs/BRAINFUCK_ABI.md` and `docs/LANGUAGE_BOUNDARY.md`.
