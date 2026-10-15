"""Offline conformance/reference codec for the bf-host-v1 XAX boundary.

OFF-DEVICE TOOLCHAIN ONLY. This is not an Android host implementation, not XAX
source, and never decides whether a YouTube object is an advertisement. The
only feature decisions remain the compiled genuine Brainfuck instructions.
"""
from __future__ import annotations

from dataclasses import dataclass
import struct

from .build import FEATURES
from .core import Program, load, interpret

# Stable ABI IDs, not classifier data or a feature policy table. Never renumber.
FEATURE_IDS = {
    'suppress_video_slot': 0x0101,
    'suppress_feed_item': 0x0102,
    'suppress_search_result': 0x0103,
    'suppress_shorts_slot': 0x0104,
    'suppress_premium_upsell': 0x0105,
    'suppress_paid_shelf': 0x0106,
    'collapse_filtered_container': 0x0201,
    'reject_ambiguous': 0x0301,
    'authorize_seek': 0x0401,
    'select_sponsor_category': 0x0402,
    'sponsor_skip_pipeline': 0x0403,
    'sponsor_time_window': 0x0404,
}

# Wire layouts: all multibyte integers are little-endian and unsigned.
REQ = struct.Struct('<4sBBHIH')  # BFH1, major, minor, feature ID, generation, length
REP = struct.Struct('<4sBBHIBH') # BFR1, major, minor, feature ID, generation, action, length
MAX_PAYLOAD = 256
MAJOR = 1
MINOR = 0
PASS = 0
SUPPRESS_COMPONENT = 1
COLLAPSE_CONTAINER = 2
REJECT_RESOLUTION = 3
SEEK_PLAYER = 4
CATEGORY_AUTO_SKIP = 5
TIME_WINDOW_VALID = 6

# Wire slots, not human-facing labels. Preserve numeric positions across builds.
SPONSOR_CATEGORIES = (
    'sponsor', 'selfpromo', 'interaction', 'intro',
    'outro', 'preview', 'filler', 'music_offtopic',
)

class ABIError(ValueError):
    """Boundary failure: always leave target behavior unchanged."""
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _u32(n: int) -> bool:
    return type(n) is int and 0 <= n <= 0xFFFFFFFF


def _u16(n: int) -> bool:
    return type(n) is int and 0 <= n <= 0xFFFF


def _bytes(data: bytes) -> bytes:
    if type(data) is not bytes:
        raise ABIError('NON_BINARY_PAYLOAD')
    if len(data) > MAX_PAYLOAD:
        raise ABIError('PAYLOAD_LIMIT')
    return data


@dataclass(frozen=True)
class Request:
    feature_id: int
    generation: int
    data: bytes

    def pack(self) -> bytes:
        if not _u16(self.feature_id) or self.feature_id not in FEATURE_IDS.values():
            raise ABIError('UNKNOWN_FEATURE')
        if not _u32(self.generation):
            raise ABIError('INVALID_GENERATION')
        data = _bytes(self.data)
        return REQ.pack(b'BFH1', MAJOR, MINOR, self.feature_id, self.generation, len(data)) + data

    @classmethod
    def unpack(cls, packet: bytes) -> Request:
        packet = _bytes_outer(packet)
        if len(packet) < REQ.size:
            raise ABIError('TRUNCATED_REQUEST')
        magic, major, minor, fid, gen, size = REQ.unpack_from(packet)
        if magic != b'BFH1':
            raise ABIError('BAD_MAGIC')
        if major != MAJOR or minor != MINOR:
            raise ABIError('BAD_VERSION')
        if fid not in FEATURE_IDS.values():
            raise ABIError('UNKNOWN_FEATURE')
        if size > MAX_PAYLOAD:
            raise ABIError('PAYLOAD_LIMIT')
        if len(packet) != REQ.size + size:
            raise ABIError('LENGTH_MISMATCH')
        return cls(fid, gen, packet[REQ.size:])


@dataclass(frozen=True)
class Reply:
    feature_id: int
    generation: int
    action: int
    data: bytes = b''

    def pack(self) -> bytes:
        if not _u16(self.feature_id) or self.feature_id not in FEATURE_IDS.values():
            raise ABIError('UNKNOWN_FEATURE')
        if not _u32(self.generation):
            raise ABIError('INVALID_GENERATION')
        data = _bytes(self.data)
        if type(self.action) is not int or self.action not in (PASS, SUPPRESS_COMPONENT, COLLAPSE_CONTAINER, REJECT_RESOLUTION, SEEK_PLAYER, CATEGORY_AUTO_SKIP, TIME_WINDOW_VALID):
            raise ABIError('INVALID_ACTION')
        return REP.pack(b'BFR1', MAJOR, MINOR, self.feature_id, self.generation, self.action, len(data)) + data

    @classmethod
    def unpack(cls, packet: bytes) -> Reply:
        packet = _bytes_outer(packet)
        if len(packet) < REP.size:
            raise ABIError('TRUNCATED_REPLY')
        magic, major, minor, fid, gen, action, size = REP.unpack_from(packet)
        if magic != b'BFR1':
            raise ABIError('BAD_MAGIC')
        if major != MAJOR or minor != MINOR:
            raise ABIError('BAD_VERSION')
        if fid not in FEATURE_IDS.values():
            raise ABIError('UNKNOWN_FEATURE')
        if size > MAX_PAYLOAD:
            raise ABIError('PAYLOAD_LIMIT')
        if len(packet) != REP.size + size:
            raise ABIError('LENGTH_MISMATCH')
        return cls(fid, gen, action, packet[REP.size:])


def _bytes_outer(packet: bytes) -> bytes:
    if type(packet) is not bytes:
        raise ABIError('NON_BINARY_PACKET')
    return packet


def checked_reply(request: Request, reply: Reply, *, active_generation: int, allow_seek: bool = False) -> Reply:
    """Verify frame/action safety; this off-device verifier executes no host operation.

    Even a complete, source-verified seek remains blocked from Android execution
    until a canonical XAX host verifies its playback context at seek time.
    """
    if not _u32(active_generation):
        raise ABIError('INVALID_GENERATION')
    if request.generation != active_generation or reply.generation != request.generation:
        raise ABIError('STALE_GENERATION')
    if reply.feature_id != request.feature_id:
        raise ABIError('FEATURE_MISMATCH')
    expected = {
        0x0101: SUPPRESS_COMPONENT, 0x0102: SUPPRESS_COMPONENT,
        0x0103: SUPPRESS_COMPONENT, 0x0104: SUPPRESS_COMPONENT,
        0x0105: SUPPRESS_COMPONENT, 0x0106: SUPPRESS_COMPONENT,
        0x0201: COLLAPSE_CONTAINER, 0x0301: REJECT_RESOLUTION,
        0x0401: SEEK_PLAYER,
        0x0402: CATEGORY_AUTO_SKIP,
        0x0403: SEEK_PLAYER,
        0x0404: TIME_WINDOW_VALID,
    }[request.feature_id]
    if reply.action not in (PASS, expected):
        raise ABIError('ACTION_NOT_AUTHORIZED')
    if reply.action == SEEK_PLAYER:
        if not allow_seek:
            raise ABIError('SEEK_NOT_DEPLOYABLE')
        if len(reply.data) != 8:
            raise ABIError('SEEK_TARGET_REQUIRED')
        offset = 21 if request.feature_id == FEATURE_IDS['sponsor_skip_pipeline'] else 6
        if len(request.data) != offset + 8 or reply.data != request.data[offset:offset + 8]:
            raise ABIError('SEEK_DESTINATION_MISMATCH')
        if int.from_bytes(reply.data, 'little') == 0 or int.from_bytes(reply.data, 'little') > 0x7FFFFFFFFFFFFFFF:
            raise ABIError('SEEK_TARGET_OUT_OF_RANGE')
        # The typed time is necessary, not sufficient: Android runtime validation
        # of player context, segment end, current position and live status is absent.
        raise ABIError('SEEK_RUNTIME_HOST_ABSENT')
    if reply.data:
        raise ABIError('UNEXPECTED_ACTION_PAYLOAD')
    return reply



def checked_sponsor_chain(category_request: Request, category_reply: Reply,
                          seek_request: Request, seek_reply: Reply,
                          *, active_generation: int) -> tuple[Reply, Reply]:
    """OFF-DEVICE binary causality guard for two independently executed BF policies.

    Does not determine category eligibility; only compares the source-produced
    category action with the next request's category gate. The caller must first
    execute both checked-in BF classes and attest their source/JAR identity.
    This is not an Android dispatcher and never executes a playback seek.
    """
    if category_request.feature_id != FEATURE_IDS['select_sponsor_category'] or \
       seek_request.feature_id != FEATURE_IDS['authorize_seek']:
        raise ABIError('SPONSOR_PIPELINE_FEATURE_MISMATCH')
    if category_request.generation != seek_request.generation:
        raise ABIError('SPONSOR_PIPELINE_STALE_CONTEXT')
    validate_request(category_request, load_programs())
    validate_request(seek_request, load_programs())
    checked_reply(category_request, category_reply, active_generation=active_generation)
    should_seek = 1 if category_reply.action == CATEGORY_AUTO_SKIP else 0
    if seek_request.data[1] != should_seek:
        raise ABIError('SPONSOR_CATEGORY_GATE_MISMATCH')
    checked_reply(seek_request, seek_reply, active_generation=active_generation)
    return category_reply, seek_reply



def checked_sponsor_time_chain(window_request: Request, window_reply: Reply,
                               skip_request: Request, skip_reply: Reply,
                               *, active_generation: int) -> tuple[Reply, Reply]:
    """OFF-DEVICE causality check: authentic BF window result -> seek gate.

    Each reply MUST originate from source-verified executable BF. This helper
    cannot attest live Android playback state or authorize a seek. The timeline
    bytes and generation are bound across both policy invocations.
    """
    if window_request.feature_id != FEATURE_IDS['sponsor_time_window'] or \
       skip_request.feature_id != FEATURE_IDS['sponsor_skip_pipeline']:
        raise ABIError('TIME_CHAIN_FEATURE_MISMATCH')
    if window_request.generation != skip_request.generation:
        raise ABIError('TIME_CHAIN_GENERATION_MISMATCH')
    programs = load_programs()
    validate_request(window_request, programs)
    validate_request(skip_request, programs)
    checked_reply(window_request, window_reply, active_generation=active_generation)
    if window_request.data[16:24] != skip_request.data[21:29]:
        raise ABIError('TIME_CHAIN_ENDPOINT_MISMATCH')
    expected_gate = int(window_reply.action == TIME_WINDOW_VALID)
    if skip_request.data[18] != expected_gate:
        raise ABIError('TIME_CHAIN_GATE_MISMATCH')
    checked_reply(skip_request, skip_reply, active_generation=active_generation)
    return window_reply, skip_reply


def load_programs() -> dict[int, Program]:
    programs = {FEATURE_IDS[p.name]: p for path in sorted(FEATURES.rglob('*.bf')) for p in [load(path)] if p.name in FEATURE_IDS}
    # Never silently ignore a newly added program or bind a duplicate ID.
    named = [load(path).name for path in sorted(FEATURES.rglob('*.bf'))]
    if len(named) != len(set(named)) or set(named) != set(FEATURE_IDS) or len(programs) != len(FEATURE_IDS):
        raise ABIError('REGISTRY_MISMATCH')
    return programs


def validate_request(request: Request, programs: dict[int, Program]) -> Program:
    """Check source-backed length, Boolean decision bits and binary timestamp."""
    program = programs.get(request.feature_id)
    if program is None:
        raise ABIError('UNKNOWN_FEATURE')
    # Derive input arity ONLY from executable commas: annotations are inert.
    # The v1 policies execute every comma once (no branch-dependent input).
    expected_length = program.code.count(',')
    if not 1 <= expected_length <= MAX_PAYLOAD:
        raise ABIError('INPUT_SCHEMA_UNSUPPORTED')
    if len(request.data) != expected_length:
        raise ABIError('INPUT_LENGTH_MISMATCH')
    if request.feature_id == FEATURE_IDS['authorize_seek']:
        bit_length = 6
    elif request.feature_id == FEATURE_IDS['sponsor_skip_pipeline']:
        bit_length = 21
    elif request.feature_id == FEATURE_IDS['sponsor_time_window']:
        bit_length = 0
    else:
        bit_length = expected_length
    if any(value not in (0, 1) for value in request.data[:bit_length]):
        raise ABIError('NON_BOOLEAN_INPUT')
    if request.feature_id in (FEATURE_IDS['select_sponsor_category'], FEATURE_IDS['sponsor_skip_pipeline']):
        # A semantic one-hot category is data integrity, not a category policy.
        if sum(request.data[1:16:2]) != 1:
            raise ABIError('CATEGORY_NOT_ONE_HOT')
    if request.feature_id == FEATURE_IDS['sponsor_time_window']:
        for position in (0, 8, 16):
            timestamp = int.from_bytes(request.data[position:position + 8], 'little')
            if timestamp > 0x7FFFFFFFFFFFFFFF:
                raise ABIError('TIMESTAMP_OUT_OF_RANGE')
    if request.feature_id in (FEATURE_IDS['authorize_seek'], FEATURE_IDS['sponsor_skip_pipeline']):
        # An Android player seek position uses a signed long. Zero is not a valid
        # skip destination, even for a disabled synthetic request.
        offset = 21 if request.feature_id == FEATURE_IDS['sponsor_skip_pipeline'] else 6
        end = int.from_bytes(request.data[offset:offset + 8], 'little')
        if end == 0 or end > 0x7FFFFFFFFFFFFFFF:
            raise ABIError('SEEK_TARGET_OUT_OF_RANGE')
    return program


def reference_dispatch(packet: bytes, *, active_generation: int) -> bytes:
    """Test oracle ONLY: BF interpreter execution, not the XAX Android host."""
    request = Request.unpack(packet)
    program = validate_request(request, load_programs())
    result = interpret(program, request.data)
    if not result or len(result) != (9 if result[0] == SEEK_PLAYER else 1):
        raise ABIError('BAD_BF_RESULT_LENGTH')
    reply = Reply(request.feature_id, request.generation, result[0], result[1:])
    checked_reply(request, reply, active_generation=active_generation)
    return reply.pack()
