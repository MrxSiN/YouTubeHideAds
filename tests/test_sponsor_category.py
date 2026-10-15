"""Actual eight-command category decisions and offline JVM AOT chain tests.

No Android runtime, network, SponsorBlock lookup or player seek is simulated.
"""
from __future__ import annotations

import hashlib
import itertools
from pathlib import Path
import tempfile
import unittest

from toolchain.brainfuck.build import build
from toolchain.brainfuck.core import interpret, parse_source
from toolchain.brainfuck.host_abi import (
    ABIError, CATEGORY_AUTO_SKIP, FEATURE_IDS, PASS, Request, Reply,
    SPONSOR_CATEGORIES, checked_reply, checked_sponsor_chain, load_programs, validate_request,
)
from toolchain.brainfuck.host_link import exercise_aot_frames
from toolchain.brainfuck.jvm import compile_class

CATEGORY_ID = FEATURE_IDS['select_sponsor_category']
SEEK_ID = FEATURE_IDS['authorize_seek']


def category_request(mask: int, selected: int, generation: int = 117) -> Request:
    # Encoding fixture ONLY: each category has [configuration flag, selector flag].
    data = bytearray(16)
    for i in range(8):
        data[2*i] = (mask >> i) & 1
    data[2*selected+1] = 1
    return Request(CATEGORY_ID, generation, bytes(data))


class SponsorCategoryTests(unittest.TestCase):
    def test_exact_sponsorblock_wire_order(self):
        self.assertEqual(SPONSOR_CATEGORIES, (
            'sponsor','selfpromo','interaction','intro',
            'outro','preview','filler','music_offtopic',
        ))

    def test_all_2048_category_setting_combinations(self):
        program = load_programs()[CATEGORY_ID]
        for mask, selected in itertools.product(range(256), range(8)):
            req = category_request(mask, selected)
            validate_request(req, {CATEGORY_ID: program})
            expected = CATEGORY_AUTO_SKIP if (mask & (1 << selected)) else PASS
            self.assertEqual(interpret(program,req.data),bytes([expected]),(mask,selected))

    def test_one_hot_and_boolean_encoding_fail_closed(self):
        programs = load_programs()
        valid = category_request(255, 3).data
        malformed = [
            (valid[:7] + b'\x00' + valid[8:], 'CATEGORY_NOT_ONE_HOT'),
            (valid[:3] + b'\x01' + valid[4:], 'CATEGORY_NOT_ONE_HOT'),
            (valid[:3] + b'\x02' + valid[4:], 'NON_BOOLEAN_INPUT'),
            (valid[:-1], 'INPUT_LENGTH_MISMATCH'),
            (b'', 'INPUT_LENGTH_MISMATCH'),
        ]
        for data, code in malformed:
            with self.subTest(code=code), self.assertRaises(ABIError) as cm:
                validate_request(Request(CATEGORY_ID,117,data),programs)
            self.assertEqual(cm.exception.code, code)

    def test_real_jvm_aot_all_category_positions_and_settings(self):
        frames = [category_request(mask, position).pack()
                  for mask in range(256) for position in range(8)]
        with tempfile.TemporaryDirectory() as directory:
            for optimized in (False, True):
                root=Path(directory)/str(optimized)
                jar=build(root,optimize=optimized)
                observed=exercise_aot_frames(frames,jar=jar,
                    manifest=root/'policies.json',optimized=optimized,
                    active_generation=117)
                self.assertEqual(len(observed),2048)
                for reqbytes,repbytes in zip(frames,observed):
                    req=Request.unpack(reqbytes)
                    rep=Reply.unpack(repbytes)
                    selected=next(i for i in range(8) if req.data[2*i+1])
                    self.assertEqual(rep.action,CATEGORY_AUTO_SKIP if req.data[2*selected] else PASS)
                    self.assertEqual(rep.feature_id,CATEGORY_ID)
                    self.assertEqual(rep.generation,117)

    def test_causal_chain_from_compiled_category_into_seek_gate(self):
        # The category gate is copied ONLY from the real BF policy's verified
        # response. Seek remains blocked until XAX/Android runtime checks exist.
        cases=[category_request(0,2),category_request(1<<2,2),category_request(1<<4,4)]
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            jar=build(root)
            responses=exercise_aot_frames([r.pack() for r in cases],jar=jar,
                manifest=root/'policies.json',active_generation=117)
            for req,raw_response in zip(cases,responses):
                decision=Reply.unpack(raw_response)
                category_gate=int(decision.action==CATEGORY_AUTO_SKIP)
                seek=Request(SEEK_ID,req.generation,bytes([1,category_gate,1,1,1,1])+
                             (500_001).to_bytes(8,'little'))
                if category_gate:
                    with self.assertRaises(ABIError) as cm:
                        exercise_aot_frames([seek.pack()],jar=jar,
                          manifest=root/'policies.json',active_generation=117)
                    self.assertEqual(cm.exception.code,'SEEK_NOT_DEPLOYABLE')
                else:
                    replies=exercise_aot_frames([seek.pack()],jar=jar,
                        manifest=root/'policies.json',active_generation=117)
                    self.assertEqual(Reply.unpack(replies[0]).action,PASS)

    def test_causal_guard_rejects_generation_and_category_spoofing(self):
        category=category_request(1 << 5,5)
        category_reply=Reply(CATEGORY_ID,117,CATEGORY_AUTO_SKIP)
        endpoint=(45678).to_bytes(8,'little')
        good_seek=Request(SEEK_ID,117,b'\x01'*6+endpoint)
        denied_seek=Request(SEEK_ID,117,b'\x01\x00\x01\x01\x01\x01'+endpoint)
        with self.assertRaises(ABIError) as cm:
            checked_sponsor_chain(category,category_reply,denied_seek,
                                  Reply(SEEK_ID,117,0),active_generation=117)
        self.assertEqual(cm.exception.code,'SPONSOR_CATEGORY_GATE_MISMATCH')
        stale_seek=Request(SEEK_ID,118,good_seek.data)
        with self.assertRaises(ABIError) as cm:
            checked_sponsor_chain(category,category_reply,stale_seek,
                                  Reply(SEEK_ID,118,0),active_generation=117)
        self.assertEqual(cm.exception.code,'SPONSOR_PIPELINE_STALE_CONTEXT')
        wrong_feature=Request(FEATURE_IDS['suppress_feed_item'],117,b'\x01'*3)
        with self.assertRaises(ABIError) as cm:
            checked_sponsor_chain(category,category_reply,wrong_feature,
                                  Reply(wrong_feature.feature_id,117,0),active_generation=117)
        self.assertEqual(cm.exception.code,'SPONSOR_PIPELINE_FEATURE_MISMATCH')
        # A positive category can be verified but cannot authorize an Android seek.
        with self.assertRaises(ABIError) as cm:
            checked_sponsor_chain(category,category_reply,good_seek,
                Reply(SEEK_ID,117,4,endpoint),active_generation=117)
        self.assertEqual(cm.exception.code,'SEEK_NOT_DEPLOYABLE')
        # A disabled category never approves a seek, including with stale state.
        disabled=category_request(0,5)
        deny=Reply(CATEGORY_ID,117,PASS)
        self.assertEqual(checked_sponsor_chain(disabled,deny,denied_seek,
            Reply(SEEK_ID,117,PASS),active_generation=117)[1].action,PASS)

    def test_authentic_source_bytecode_and_comment_invariance(self):
        path=Path('source/brainfuck/sponsorblock/select_sponsor_category.bf')
        src=path.read_text()
        p=parse_source(src)
        alternate=parse_source(src.replace('# @section emit_category_action',
                            '# none of ><+-.,[] in this comment are executable\n# @section emit_category_action'))
        # Changing only an annotation cannot affect the exact resulting AOT class.
        name='org/youtubehideads/bf/select_sponsor_category'
        self.assertEqual(compile_class(p,name),compile_class(alternate,name))
        mutated=parse_source(src.replace('[->+++++<]>.','[->++++<]>.'))
        self.assertNotEqual(hashlib.sha256(compile_class(p,name)).digest(),
                            hashlib.sha256(compile_class(mutated,name)).digest())
        self.assertEqual(interpret(p,category_request(255,4).data),b'\x05')
        self.assertEqual(interpret(mutated,category_request(255,4).data),b'\x04')
        # The host would reject action 4 for category, even when the source is mutated.
        with self.assertRaises(ABIError) as cm:
            checked_reply(category_request(255,4),Reply(CATEGORY_ID,117,4),active_generation=117)
        self.assertEqual(cm.exception.code,'ACTION_NOT_AUTHORIZED')

if __name__=='__main__':unittest.main()
