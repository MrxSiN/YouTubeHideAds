"""One-call Brainfuck SponsorBlock policy: no host-provided category decision.

Every expected action is compared with existing executable Brainfuck oracles.
Tests cannot authorize a device seek. Java is test-harness-only.
"""
from __future__ import annotations

import itertools
import random
import tempfile
import unittest
from pathlib import Path

from toolchain.brainfuck.build import build
from toolchain.brainfuck.core import interpret, load
from toolchain.brainfuck.host_abi import (
    ABIError, FEATURE_IDS, Request, Reply, checked_reply,
    load_programs, validate_request,
)
from toolchain.brainfuck.host_link import exercise_aot_frames
from toolchain.brainfuck.router import (
    build_router, exercise_router_frames, selector_map, source_and_manifest,
)

FID=FEATURE_IDS['sponsor_skip_pipeline']
CAT=FEATURE_IDS['select_sponsor_category']
SEEK=FEATURE_IDS['authorize_seek']


def make_payload(mask: int, selected: int, flags: tuple[int, ...], endpoint: int = 1234567) -> bytes:
    return (bytes(v for i in range(8) for v in ((mask >> i) & 1, int(i == selected)))
            + bytes(flags) + endpoint.to_bytes(8, 'little'))


class SponsorPipelineTests(unittest.TestCase):
    def test_all_category_masks_against_existing_bf_policies(self):
        programs=load_programs()
        combined=programs[FID]
        for mask in range(256):
            for category in range(8):
                payload=make_payload(mask,category,(1,1,1,1,1))
                category_action=interpret(programs[CAT],payload[:16])[0]
                legacy=b'\x01' + bytes((category_action == 5,)) + payload[17:21] + payload[21:29]
                expected=interpret(programs[SEEK],legacy)
                self.assertEqual(interpret(combined,payload),expected,(mask,category))

    def test_five_runtime_gates_and_binary_endpoint(self):
        program=load_programs()[FID]
        rng=random.Random(0xB13)
        for flags in itertools.product((0,1),repeat=5):
            for category in range(8):
                endpoint=rng.randint(1,(1<<63)-1)
                payload=make_payload(255,category,flags,endpoint)
                expected=b'\x04'+endpoint.to_bytes(8,'little') if all(flags) else b'\x00'
                self.assertEqual(interpret(program,payload),expected)

    def test_last_disabled_category_scratch_is_cleared(self):
        program=load_programs()[FID]
        data=make_payload(0,7,(1,1,1,1,1))
        self.assertEqual(interpret(program,data),b'\x00')
        # An unauthorized seventh/index-7 category must never inherit cell2.
        for mask in range(0,128):
            self.assertEqual(interpret(program,make_payload(mask,7,(1,1,1,1,1))),b'\x00')
        source=Path('source/brainfuck/sponsorblock/sponsor_skip_pipeline.bf').read_text()
        self.assertIn('>[-]>[-]<<',source)

    def test_input_integrity_and_runtime_seeks_blocked(self):
        program=load_programs()[FID]
        payload=make_payload(255,3,(1,1,1,1,1))
        for wrong, code in (
            (payload[:-1], 'INPUT_LENGTH_MISMATCH'),
            (b'\x02'+payload[1:], 'NON_BOOLEAN_INPUT'),
            (payload[:16]+b'\x02'+payload[17:], 'NON_BOOLEAN_INPUT'),
            (bytes(16)+payload[16:], 'CATEGORY_NOT_ONE_HOT'),
            (payload[:1]+b'\x01'+payload[2:3]+b'\x01'+payload[4:], 'CATEGORY_NOT_ONE_HOT'),
            (payload[:21]+bytes(8), 'SEEK_TARGET_OUT_OF_RANGE'),
            (payload[:21]+bytes((255,))*8, 'SEEK_TARGET_OUT_OF_RANGE'),
        ):
            with self.subTest(code=code,packet=wrong.hex()), self.assertRaises(ABIError) as caught:
                validate_request(Request(FID,4,wrong),{FID:program})
            self.assertEqual(caught.exception.code,code)
        req=Request(FID,4,payload)
        self.assertEqual(interpret(program,payload),b'\x04'+payload[21:])
        with self.assertRaisesRegex(ABIError,'SEEK_NOT_DEPLOYABLE'):
            checked_reply(req,Reply(FID,4,4,payload[21:]),active_generation=4)
        disabled=Request(FID,4,make_payload(0,3,(1,1,1,1,1)))
        self.assertEqual(checked_reply(disabled,Reply(FID,4,0),active_generation=4).action,0)

    def test_real_compiled_jvm_and_router_match_both_modes(self):
        masks=(0,1,85,128,255)
        samples=[Request(FID,94,make_payload(mask,category,flags,0x0203040506070809))
                 for mask in masks for category in range(8)
                 for flags in ((0,1,1,1,1),(1,0,1,1,1),(1,1,1,1,1))
                 if not ((mask>>category)&1 and all(flags))]
        with tempfile.TemporaryDirectory() as temp:
            for opt in (False,True):
                out=Path(temp)/str(opt)
                jar=build(out,optimize=opt)
                router=build_router(out,optimize=opt)
                frames=[r.pack() for r in samples]
                expected=exercise_aot_frames(frames,jar=jar,manifest=out/'policies.json',optimized=opt,active_generation=94)
                actual=exercise_router_frames(frames,jar=router,manifest=out/'router.json',optimized=opt,active_generation=94)
                self.assertEqual(actual,expected)
                positive=Request(FID,94,make_payload(255,7,(1,1,1,1,1)))
                for call in (
                    lambda:exercise_aot_frames([positive.pack()],jar=jar,manifest=out/'policies.json',optimized=opt,active_generation=94),
                    lambda:exercise_router_frames([positive.pack()],jar=router,manifest=out/'router.json',optimized=opt,active_generation=94),
                ):
                    with self.assertRaisesRegex(ABIError,'SEEK_NOT_DEPLOYABLE'):
                        call()

    def test_policy_is_sole_executable_category_and_seek_decider(self):
        program=load(Path('source/brainfuck/sponsorblock/sponsor_skip_pipeline.bf'))
        self.assertEqual(program.code.count(','),29)
        self.assertEqual(len(program.code),370)
        src,manifest=source_and_manifest()
        self.assertEqual(len(manifest['policies']),12)
        self.assertIn(program.code,src)
        self.assertEqual(manifest['policies']['sponsor_skip_pipeline']['feature_id'],FID)
        self.assertEqual(selector_map()['sponsor_skip_pipeline'],11)


if __name__ == '__main__':
    unittest.main()
