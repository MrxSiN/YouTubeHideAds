"""XAX-facing binary protocol conformance oracles (no platform hooks)."""
from __future__ import annotations
import itertools
from dataclasses import replace
import random
import unittest

from toolchain.brainfuck.host_abi import (
    ABIError, FEATURE_IDS, MAJOR, MAX_PAYLOAD, REQ, REP,
    Request, Reply, checked_reply, reference_dispatch, load_programs, validate_request,
)
from toolchain.brainfuck.core import interpret

class HostAbiTests(unittest.TestCase):
    def test_exact_layout_and_round_trip(self):
        req = Request(FEATURE_IDS['suppress_feed_item'], 0x12345678, b'\x00\x01\x01')
        frame = req.pack()
        self.assertEqual(frame, b'BFH1\x01\x00\x02\x01\x78\x56\x34\x12\x03\x00\x00\x01\x01')
        self.assertEqual(Request.unpack(frame), req)
        rep = Reply(req.feature_id, req.generation, 1)
        self.assertEqual(rep.pack(), b'BFR1\x01\x00\x02\x01\x78\x56\x34\x12\x01\x00\x00')
        self.assertEqual(Reply.unpack(rep.pack()), rep)
        self.assertEqual(REQ.size, 14)
        self.assertEqual(REP.size, 15)

    def test_all_feature_frames_and_generation(self):
        programs = load_programs()
        for fid, program in programs.items():
            if fid == 0x0403:
                variants=[]
                for index in range(8):
                    for toggled in (0,1):
                        category=bytes(x for j in range(8) for x in (toggled,int(index==j)))
                        variants.append(category+b'\x01'*5+(1234567890123).to_bytes(8,'little'))
            elif fid == 0x0404:
                variants=(b''.join(n.to_bytes(8,'little') for n in t) for t in ((0,0,1),(5,4,6),(1,2,2),(100,101,102)))
            elif fid == 0x0402:
                variants=[]
                for index in range(8):
                    for mask in (0, 1, 85, 170, 255):
                        data=bytearray(16)
                        for j in range(8):data[2*j]=(mask>>j)&1
                        data[2*index+1]=1
                        variants.append(bytes(data))
            else:
                n = 6 if fid == 0x0401 else program.code.count(',')
                variants = (bytes(bits) + ((1234567890123).to_bytes(8,'little') if fid == 0x0401 else b'')
                            for bits in itertools.product((0, 1), repeat=n))
            for inp in variants:
                req = Request(fid, 7, inp)
                validate_request(req, programs)
                expected = interpret(program, req.data)[0]
                if expected == 4:
                    with self.assertRaises(ABIError) as blocked:
                        reference_dispatch(req.pack(), active_generation=7)
                    self.assertEqual(blocked.exception.code, 'SEEK_NOT_DEPLOYABLE')
                else:
                    native = reference_dispatch(req.pack(), active_generation=7)
                    rep = Reply.unpack(native)
                    self.assertEqual(rep.action, expected)
                    self.assertEqual(rep.generation, 7)
                    self.assertEqual(rep.feature_id, fid)
                with self.assertRaises(ABIError) as stale:
                    reference_dispatch(req.pack(), active_generation=8)
                self.assertEqual(stale.exception.code, 'STALE_GENERATION')

    def test_mutated_frames_fail_closed(self):
        req = Request(0x0102, 1, b'\x01\x00\x01').pack()
        rep = Reply(0x0102, 1, 1).pack()
        changes = [req[:i] for i in range(14)] + [req+b'\0', b'NOPE'+req[4:], req[:4]+b'\x02'+req[5:], req[:5]+b'\x01'+req[6:], req[:6]+b'\xff\xff'+req[8:], req[:12]+b'\xff\xff'+req[14:]]
        for frame in changes:
            with self.subTest(frame=frame.hex()), self.assertRaises(ABIError):
                Request.unpack(frame)
        changes = [rep[:i] for i in range(15)] + [rep+b'\0', b'NOPE'+rep[4:], rep[:4]+b'\x02'+rep[5:], rep[:6]+b'\xff\xff'+rep[8:], rep[:13]+b'\xff\xff'+rep[15:]]
        for frame in changes:
            with self.subTest(frame=frame.hex()), self.assertRaises(ABIError):
                Reply.unpack(frame)
        for frame in (b'', b'BFH1', b'BFR1', b'\xff'*1000):
            with self.assertRaises(ABIError):Request.unpack(frame)

    def test_invalid_inputs_and_bad_types(self):
        programs = load_programs()
        for input in [b'', b'\x01\x01', b'\x01\x01\x01\x01', b'\x01\x02\x01']:
            with self.subTest(input=input.hex()), self.assertRaises(ABIError):
                validate_request(Request(0x0102, 1, input), programs)
        for payload in [bytearray(b'\x01'), 'x', None, b'\0'*(MAX_PAYLOAD+1)]:
            with self.subTest(payload=type(payload)),self.assertRaises(ABIError):
                Request(0x0102, 1, payload).pack()
        for generation in [-1, 0x1_0000_0000, True]:
            with self.assertRaises(ABIError):Request(0x0102, generation, b'\x01\x01\x01').pack()

    def test_action_domain_and_stale_context(self):
        req = Request(0x0101, 54, b'\x01\x01\x01\x00')
        for reply, expected in [
            (Reply(0x0102, 54, 1), 'FEATURE_MISMATCH'),
            (Reply(0x0101, 55, 1), 'STALE_GENERATION'),
            (Reply(0x0101, 54, 2), 'ACTION_NOT_AUTHORIZED'),
            (Reply(0x0101, 54, 1, b'anything'), 'UNEXPECTED_ACTION_PAYLOAD'),
        ]:
            with self.assertRaises(ABIError) as cm:
                checked_reply(req, reply, active_generation=54)
            self.assertEqual(cm.exception.code, expected)
        for action in [-1, 7, 255]:
            with self.assertRaises(ABIError):Reply(0x0101, 54, action).pack()

    def test_seek_is_non_deployable(self):
        req=Request(0x0401, 12, b'\x01'*6 + (1234567).to_bytes(8,'little'))
        # The AOT program now emits a typed destination; Android seek is still disabled.
        with self.assertRaises(ABIError) as cm:
            reference_dispatch(req.pack(), active_generation=12)
        self.assertEqual(cm.exception.code, 'SEEK_NOT_DEPLOYABLE')
        with self.assertRaises(ABIError) as cm:
            checked_reply(req, Reply(0x0401,12,4), active_generation=12, allow_seek=True)
        self.assertEqual(cm.exception.code,'SEEK_TARGET_REQUIRED')
        with self.assertRaises(ABIError) as cm:
            checked_reply(req, Reply(0x0401,12,4,b'\x00'*8), active_generation=12, allow_seek=True)
        self.assertEqual(cm.exception.code,'SEEK_DESTINATION_MISMATCH')
        with self.assertRaises(ABIError) as cm:
            checked_reply(req, Reply(0x0401,12,4,req.data[6:]), active_generation=12, allow_seek=True)
        self.assertEqual(cm.exception.code,'SEEK_RUNTIME_HOST_ABSENT')

    def test_annotation_edits_do_not_change_abi_arity(self):
        programs=load_programs()
        p=programs[0x0102]
        changed=replace(p,metadata={**p.metadata, 'inputs':'Only an editorial comment, no executable meaning.'})
        original=Request(0x0102,5,b'\x01\x01\x00')
        self.assertEqual(validate_request(original,{0x0102:p}).digest,
                         validate_request(original,{0x0102:changed}).digest)
        with self.assertRaises(ABIError) as cm:
            validate_request(Request(0x0102,5,b'\x01'),{0x0102:changed})
        self.assertEqual(cm.exception.code,'INPUT_LENGTH_MISMATCH')

    def test_random_framing_roundtrips(self):
        rng=random.Random(1122)
        ids=list(FEATURE_IDS.values())
        for _ in range(500):
            req=Request(rng.choice(ids),rng.randrange(1<<32),rng.randbytes(rng.randrange(0,257)))
            self.assertEqual(Request.unpack(req.pack()),req)
            rep=Reply(req.feature_id,req.generation,rng.randrange(5),rng.randbytes(rng.randrange(0,257)))
            self.assertEqual(Reply.unpack(rep.pack()),rep)

if __name__=='__main__': unittest.main()
