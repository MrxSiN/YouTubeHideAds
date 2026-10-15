"""End-to-end BF source/JVM 64-bit seek authorization tests (no Android seek)."""
from __future__ import annotations
import itertools
import random
import tempfile
import unittest
from pathlib import Path

from toolchain.brainfuck.build import build
from toolchain.brainfuck.core import interpret
from toolchain.brainfuck.host_abi import (
    ABIError, FEATURE_IDS, Request, Reply, checked_reply, load_programs, validate_request,
)
from toolchain.brainfuck.host_link import exercise_aot_frames

FID = FEATURE_IDS['authorize_seek']

class SponsorSeekTests(unittest.TestCase):
    def test_full_boolean_cube_and_endpoints(self):
        prog = load_programs()[FID]
        samples = [1, 255, 256, 1024, 1234567890, 2**32+1, 2**63-1]
        for endpoint in samples:
            stamp=endpoint.to_bytes(8,'little')
            for flags in itertools.product((0,1),repeat=6):
                data=bytes(flags)+stamp
                req=Request(FID, 234, data)
                validate_request(req,{FID:prog})
                expected=(b'\x04'+stamp if all(flags) else b'\x00')
                self.assertEqual(interpret(prog,data),expected,(flags,endpoint))

    def test_bitwise_destination_is_not_constant_or_host_reconstructed(self):
        prog=load_programs()[FID]
        for target in [b'\x00\xff\x12\x34\x56\x00\x78\x01', b'\x01'+b'\x00'*7,
                       b'\xff'*7+b'\x7f']:
            self.assertEqual(interpret(prog, b'\x01'*6 + target), b'\x04'+target)

    def test_jvm_equivalence_both_modes(self):
        rng=random.Random(0x51A0B)
        frames=[]
        for _ in range(70):
            flags=bytes(rng.randrange(2) for _ in range(6))
            end=rng.randrange(1,2**63).to_bytes(8,'little')
            if all(flags):flags=b'\x00'+flags[1:] # usable host frames, no actual seek
            frames.append(Request(FID, 76, flags+end).pack())
        with tempfile.TemporaryDirectory() as tmp:
            for optimize in (False,True):
                root=Path(tmp)/str(optimize)
                jar=build(root,optimize=optimize)
                outputs=exercise_aot_frames(frames,jar=jar,manifest=root/'policies.json',
                                             optimized=optimize,active_generation=76)
                self.assertEqual(len(outputs),len(frames))
                for frame, reply in zip(frames,outputs):
                    req=Request.unpack(frame)
                    self.assertEqual(Reply.unpack(reply).action,0)
                    self.assertEqual(Reply.unpack(reply).data,b'')
                eligible=Request(FID,76,b'\x01'*6 +(991225777).to_bytes(8,'little')).pack()
                with self.assertRaises(ABIError) as cm:
                    exercise_aot_frames([eligible],jar=jar,manifest=root/'policies.json',
                                        optimized=optimize,active_generation=76)
                self.assertEqual(cm.exception.code,'SEEK_NOT_DEPLOYABLE')

    def test_malformed_destinations_and_flags(self):
        p=load_programs()
        good=b'\x01'*6+(200).to_bytes(8,'little')
        for data,code in [
            (good[:-1],'INPUT_LENGTH_MISMATCH'),
            (b'\x02'+good[1:],'NON_BOOLEAN_INPUT'),
            (b'\x01'*6+b'\0'*8,'SEEK_TARGET_OUT_OF_RANGE'),
            (b'\x01'*6+b'\xff'*8,'SEEK_TARGET_OUT_OF_RANGE'),
        ]:
            with self.subTest(data=data.hex()),self.assertRaises(ABIError) as cm:
                validate_request(Request(FID,7,data),p)
            self.assertEqual(cm.exception.code,code)

    def test_anti_spoofing_generation_and_payload_match(self):
        req=Request(FID,20,b'\x01'*6+(50000).to_bytes(8,'little'))
        valid=Reply(FID,20,4,req.data[6:])
        bad=[
            (Reply(FID,21,4,req.data[6:]),'STALE_GENERATION'),
            (Reply(FID,20,4,(49999).to_bytes(8,'little')),'SEEK_DESTINATION_MISMATCH'),
            (Reply(FID,20,4,req.data[6:-1]),'SEEK_TARGET_REQUIRED'),
            (Reply(FID,20,4,b'\0'*8),'SEEK_DESTINATION_MISMATCH'),
        ]
        for response,code in bad:
            with self.subTest(code=code),self.assertRaises(ABIError) as cm:
                checked_reply(req,response,active_generation=20,allow_seek=True)
            self.assertEqual(cm.exception.code,code)
        with self.assertRaises(ABIError) as cm:
            checked_reply(req,valid,active_generation=20,allow_seek=True)
        self.assertEqual(cm.exception.code,'SEEK_RUNTIME_HOST_ABSENT')

if __name__=='__main__':unittest.main()
