"""Timestamp correctness and compiled/JNI boundary checks; no Android seek."""
from __future__ import annotations

import hashlib
import random
import subprocess
import tempfile
import unittest
from pathlib import Path

from toolchain.brainfuck.build import build
from toolchain.brainfuck.core import BFError, interpret, load, parse_source, program_fuel
from toolchain.brainfuck.host_abi import (
    ABIError, FEATURE_IDS, Request, Reply, PASS, TIME_WINDOW_VALID,
    checked_reply, checked_sponsor_time_chain, validate_request, load_programs,
)
from toolchain.brainfuck.host_link import exercise_aot_frames
from toolchain.brainfuck.router import build_router, exercise_router_frames, selector_map

FID = FEATURE_IDS['sponsor_time_window']
SKIP = FEATURE_IDS['sponsor_skip_pipeline']
LIMIT = (1 << 63) - 1


def packet(start: int, current: int, end: int) -> bytes:
    return b''.join(n.to_bytes(8, 'little') for n in (start, current, end))


def sponsor_payload(window_gate: int, end: int, *, enabled: int = 0) -> bytes:
    flags = bytes(value for category in range(8) for value in (1, int(category == 3)))
    return flags + bytes((enabled, 1, window_gate, 1, 1)) + end.to_bytes(8, 'little')


class SponsorTimeWindowTests(unittest.TestCase):
    def test_boundaries_and_full_unsigned_63bit_domain(self):
        prog = load_programs()[FID]
        cases = ((0, 0, 1), (0, 1, 1), (5, 4, 6), (5, 5, 6), (5, 6, 6),
                 (10, 11, 12), (12, 11, 13), (0, 1 << 40, 1 << 42),
                 (LIMIT - 2, LIMIT - 1, LIMIT), (LIMIT, LIMIT, LIMIT),
                 (1, 0, LIMIT), (0, LIMIT, LIMIT), (0, 0, LIMIT),
                 (0xFF00FF00, 0xFF00FF01, 0xFF00FF02))
        for start, current, end in cases:
            with self.subTest(start=start, current=current, end=end):
                result = interpret(prog, packet(start, current, end))
                self.assertEqual(result, bytes((TIME_WINDOW_VALID if start <= current < end else PASS,)))

    def test_deterministic_randomized_64bit_comparisons(self):
        p = load_programs()[FID]
        rng = random.Random(0xBF14)
        for _ in range(35):
            values = [rng.randrange(LIMIT + 1) for _ in range(3)]
            start, current, end = values
            self.assertEqual(interpret(p, packet(*values)),
                bytes((TIME_WINDOW_VALID if start <= current < end else PASS,)))

    def test_explicit_per_feature_fuel_and_inert_metadata(self):
        p = load_programs()[FID]
        self.assertEqual(p.code.count(','), 24)
        self.assertEqual(program_fuel(p), 2_000_000)
        self.assertEqual(program_fuel(load_programs()[FEATURE_IDS['suppress_feed_item']]), 100_000)
        text = Path('source/brainfuck/sponsorblock/sponsor_time_window.bf').read_text()
        self.assertEqual(parse_source(text.replace('# @purpose', '# @note INERT\n# @purpose')).digest, p.digest)
        for fuel in ('0', '-1', '02000000', '99999999999999', 'NaN'):
            with self.subTest(fuel=fuel), self.assertRaisesRegex(BFError, 'INVALID_FUEL_LIMIT'):
                parse_source(text.replace('# @fuel 2000000', '# @fuel ' + fuel))
        with self.assertRaisesRegex(BFError, 'LATE_HEADER'):
            parse_source(text.replace('# @fuel 2000000\n', '') + '\n# @fuel 2000000')
        with self.assertRaisesRegex(BFError, 'FUEL_EXHAUSTED'):
            interpret(p, packet(LIMIT - 2, LIMIT - 1, LIMIT), max_steps=100000)

    def test_out_of_domain_timestamp_rejected_at_host_abi(self):
        prog=load_programs()[FID]
        for bad in ((1 << 63, 1, 2), (0, 1 << 63, LIMIT), (0, 1, 1 << 63)):
            with self.assertRaisesRegex(ABIError, 'TIMESTAMP_OUT_OF_RANGE'):
                validate_request(Request(FID, 4, packet(*bad)), {FID:prog})
        with self.assertRaisesRegex(ABIError, 'INPUT_LENGTH_MISMATCH'):
            validate_request(Request(FID, 4, bytes(23)), {FID:prog})

    def test_real_jvm_router_and_standalone_differential(self):
        cases=((0, 0, 1), (5, 4, 9), (8, 9, 10), (9, 9, 9),
               (LIMIT - 3, LIMIT - 2, LIMIT), (0, LIMIT, LIMIT))
        # A window-valid outcome is never a seek; action 6 is a local validation proof.
        frames=[Request(FID, 44, packet(*t)).pack() for t in cases]
        with tempfile.TemporaryDirectory() as tmp:
            for optimize in (False, True):
                out=Path(tmp)/str(optimize)
                jar=build(out,optimize=optimize)
                router=build_router(out,optimize=optimize)
                a=exercise_aot_frames(frames,jar=jar,manifest=out/'policies.json',
                                      optimized=optimize,active_generation=44)
                b=exercise_router_frames(frames,jar=router,manifest=out/'router.json',
                                         optimized=optimize,active_generation=44)
                self.assertEqual(a,b)
                self.assertEqual([Reply.unpack(x).action for x in a],
                                 [TIME_WINDOW_VALID if t[0]<=t[1]<t[2] else PASS for t in cases])

    def test_cross_policy_gate_generation_and_endpoint_tied(self):
        w=Request(FID, 12, packet(10, 11, 20))
        yes=Reply(FID, 12, TIME_WINDOW_VALID)
        skip=Request(SKIP, 12, sponsor_payload(1, 20, enabled=0))
        sk_reply=Reply(SKIP, 12, PASS)
        self.assertEqual(checked_sponsor_time_chain(w,yes,skip,sk_reply,active_generation=12),(yes,sk_reply))
        for bad,code in (
            (Request(SKIP, 12, sponsor_payload(0,20,enabled=0)), 'TIME_CHAIN_GATE_MISMATCH'),
            (Request(SKIP, 12, sponsor_payload(1,21,enabled=0)), 'TIME_CHAIN_ENDPOINT_MISMATCH'),
            (Request(SKIP, 13, sponsor_payload(1,20,enabled=0)), 'TIME_CHAIN_GENERATION_MISMATCH'),
        ):
            with self.subTest(code=code),self.assertRaisesRegex(ABIError,code):
                checked_sponsor_time_chain(w,yes,bad,sk_reply,active_generation=12)
        no=Reply(FID,12,PASS)
        with self.assertRaisesRegex(ABIError,'TIME_CHAIN_GATE_MISMATCH'):
            checked_sponsor_time_chain(w,no,skip,sk_reply,active_generation=12)
        # Even valid timestamps cannot result in a real seek without Android verification.
        active=Request(SKIP,12,sponsor_payload(1,20,enabled=1))
        with self.assertRaisesRegex(ABIError,'SEEK_NOT_DEPLOYABLE'):
            checked_sponsor_time_chain(w,yes,active,Reply(SKIP,12,4,(20).to_bytes(8,'little')),active_generation=12)


if __name__=='__main__':
    unittest.main()
