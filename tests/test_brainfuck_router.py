"""Real Brainfuck multi-policy router conformance; no Android runtime claim."""
from __future__ import annotations

import itertools
import json
import os
from pathlib import Path
import tempfile
import unittest
import zipfile

from toolchain.brainfuck.core import interpret, parse_source
from toolchain.brainfuck.host_abi import ABIError, FEATURE_IDS, Request, Reply, load_programs
from toolchain.brainfuck.router import (
    ROUTER_CLASS, ROUTER_ENTRY, build_router, exercise_router_frames,
    selector_map, source_and_manifest, verify_router, _pointer_proof,
)


class RouterTests(unittest.TestCase):
    def test_pointer_proof_rejects_escaping_feature_bodies(self):
        self.assertEqual(_pointer_proof('[>+<-]>>'),2)
        with self.assertRaisesRegex(ABIError,'ROUTER_BODY_POINTER_ESCAPE'):
            _pointer_proof('<,+.')
        with self.assertRaisesRegex(ABIError,'ROUTER_UNBALANCED_LOOP_POINTER'):
            _pointer_proof('[>+]')

    def test_branch_source_integrity_and_fixed_selectors(self):
        source, manifest = source_and_manifest()
        self.assertEqual(manifest['schema'], 'brainfuck-inline-router-v1')
        self.assertEqual(manifest['class'], ROUTER_CLASS)
        self.assertEqual(len(manifest['policies']), len(FEATURE_IDS))
        self.assertEqual(sorted(selector_map().values()), list(range(1, len(FEATURE_IDS)+1)))
        self.assertEqual(parse_source(source).digest, manifest['source_sha256'])
        for name, policy in manifest['policies'].items():
            self.assertEqual(policy['feature_id'], FEATURE_IDS[name])
            program = load_programs()[FEATURE_IDS[name]]
            self.assertIn(program.code, source)
            self.assertEqual(program.digest, policy['source_sha256'])

    def test_exhaustive_boolean_and_category_equivalence(self):
        router = parse_source(source_and_manifest()[0])
        programs = load_programs()
        count = 0
        for name, index in selector_map().items():
            policy = programs[FEATURE_IDS[name]]
            if name == 'select_sponsor_category':
                # All 256 setting masks, each of eight valid one-hot categories.
                samples = []
                for mask in range(256):
                    for selected in range(8):
                        samples.append(bytes(value for cat in range(8)
                                             for value in ((mask >> cat) & 1, int(cat == selected))))
            elif name == 'sponsor_time_window':
                samples = [b''.join(n.to_bytes(8,'little') for n in t) for t in ((0,0,1),(10,12,13),(10,9,13),(10,13,13))]
            elif name == 'sponsor_skip_pipeline':
                samples = []
                for mask in range(0, 256, 17):
                    for selected in range(8):
                        category=bytes(value for cat in range(8) for value in ((mask >> cat)&1, int(cat==selected)))
                        for enabled in (0,1):
                            samples.append(category + bytes((enabled,1,1,1,1)) + (0x0102030405).to_bytes(8,'little'))
            elif name == 'authorize_seek':
                samples = [bytes(bits) + endpoint.to_bytes(8, 'little')
                           for bits in itertools.product((0, 1), repeat=6)
                           for endpoint in (1, 0x0102030405060708, (1 << 63) - 1)]
            else:
                samples = [bytes(bits) for bits in itertools.product((0, 1), repeat=policy.code.count(','))]
            for data in samples:
                self.assertEqual(
                    interpret(router, bytes((index,))+data), interpret(policy, data),
                    f'{name}: {data.hex()}')
                count += 1
        self.assertGreaterEqual(count, 2300)
        # Unsupported selectors perform no action. The host MUST reject empty output.
        for invalid in (0, len(FEATURE_IDS)+1, 254, 255):
            self.assertEqual(interpret(router, bytes((invalid,)) + bytes([1]*32)), b'')

    def test_both_real_jvm_compiler_modes_and_framing(self):
        features = load_programs()
        selectors = selector_map()
        frames = []
        for name, index in selectors.items():
            program = features[FEATURE_IDS[name]]
            if name == 'select_sponsor_category':
                for selected in range(8):
                    for toggled in (0, 1):
                        data = bytes(x for cat in range(8) for x in (toggled, int(cat == selected)))
                        frames.append(Request(FEATURE_IDS[name], 29, data).pack())
            elif name == 'sponsor_time_window':
                for t in ((0,0,1),(10,9,13),(3,4,5)):
                    frames.append(Request(FEATURE_IDS[name],29,b''.join(n.to_bytes(8,'little') for n in t)).pack())
            elif name == 'sponsor_skip_pipeline':
                for selected in range(8):
                    for on in (0,):
                        category=bytes(x for cat in range(8) for x in (on,int(cat==selected)))
                        frames.append(Request(FEATURE_IDS[name],29,category+b'\x01'*5+(300).to_bytes(8,'little')).pack())
            elif name == 'authorize_seek':
                for enabled in (0,):
                    for end in (1, (1 << 40)+2):
                        frames.append(Request(FEATURE_IDS[name], 29, bytes((enabled,)*6)+end.to_bytes(8,'little')).pack())
            else:
                width=program.code.count(',')
                for bits in itertools.product((0, 1), repeat=width):
                    frames.append(Request(FEATURE_IDS[name], 29, bytes(bits)).pack())
        with tempfile.TemporaryDirectory() as tmp:
            all_replies = []
            for optimized in (False, True):
                out=Path(tmp) / str(optimized)
                jar=build_router(out, optimize=optimized)
                manifest=out/'router.json'
                verified=verify_router(jar,manifest,optimize=optimized)
                self.assertEqual(set(verified['policies']),set(FEATURE_IDS))
                self.assertEqual((out/'router.bf').read_text(), source_and_manifest()[0])
                with zipfile.ZipFile(jar) as archive:
                    self.assertEqual(archive.namelist(),[ROUTER_ENTRY])
                replies=exercise_router_frames(frames,jar=jar,manifest=manifest,
                                               optimized=optimized,active_generation=29)
                self.assertEqual(len(replies),len(frames))
                all_replies.append(replies)
            self.assertEqual(all_replies[0],all_replies[1])
            for request, response in zip(frames, all_replies[0]):
                self.assertEqual(Reply.unpack(response).feature_id,Request.unpack(request).feature_id)

    def test_positive_seek_is_real_bf_but_still_blocked_from_host_action(self):
        # The one-entrypoint router must execute the seek program exactly,
        # but the host-contract oracle is required to refuse device seeking.
        import subprocess
        from toolchain.brainfuck.core import interpret
        payload=bytes((1,)*6) + ((1 << 40)+123).to_bytes(8,'little')
        selector=selector_map()['authorize_seek']
        router=parse_source(source_and_manifest()[0])
        expected=interpret(router, bytes((selector,))+payload)
        self.assertEqual(expected,bytes((4,))+payload[6:])
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for optimized in (False, True):
                out=root/str(optimized)
                jar=build_router(out,optimize=optimized)
                compile_result=subprocess.run(['javac','-d',str(root),
                    str(Path(__file__).resolve().parent/'jvm/Runner.java')],
                    capture_output=True,text=True)
                self.assertEqual(compile_result.returncode,0,compile_result.stderr)
                result=subprocess.run(['java','-cp',str(root)+os.pathsep+str(jar),'Runner'],
                    input='dispatch_all '+(bytes((selector,))+payload).hex()+'\nEND\n',
                    capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertEqual(result.stdout.strip(),'OK '+expected.hex())
                frame=Request(FEATURE_IDS['authorize_seek'],73,payload).pack()
                with self.assertRaises(ABIError) as cm:
                    exercise_router_frames([frame],jar=jar,manifest=out/'router.json',
                                           optimized=optimized,active_generation=73)
                self.assertEqual(cm.exception.code,'SEEK_NOT_DEPLOYABLE')

    def test_manifest_and_class_tamper_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            jar=build_router(out)
            manifest=out/'router.json'
            original=manifest.read_text()
            source=source_and_manifest()[0]
            corrupt=json.loads(original)
            corrupt['policies']['suppress_video_slot']['selector']=10
            manifest.write_text(json.dumps(corrupt))
            with self.assertRaises(ABIError) as cm:
                verify_router(jar,manifest)
            self.assertEqual(cm.exception.code,'ROUTER_MANIFEST_MISMATCH')
            manifest.write_text(original)
            generated_source=out/'router.bf'
            generated_source.write_text(source+'# altered\n')
            with self.assertRaises(ABIError) as cm:
                verify_router(jar,manifest)
            self.assertEqual(cm.exception.code,'ROUTER_SOURCE_FILE_MISMATCH')
            generated_source.write_text(source, encoding='utf-8', newline='\n')
            with zipfile.ZipFile(jar) as z:
                data=z.read(ROUTER_ENTRY)
            with zipfile.ZipFile(jar,'w') as z:
                z.writestr(ROUTER_ENTRY, data[:-1]+bytes((data[-1]^1,)))
            with self.assertRaises(ABIError) as cm:
                verify_router(jar,manifest)
            self.assertEqual(cm.exception.code,'ROUTER_CLASS_TAMPERED')
            self.assertEqual(parse_source(source).name,'dispatch_all')

    def test_reject_stale_and_invalid_framed_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)
            jar=build_router(out)
            manifest=out/'router.json'
            sample=Request(FEATURE_IDS['suppress_feed_item'],33,b'\x01\x01\x01').pack()
            with self.assertRaises(ABIError) as cm:
                exercise_router_frames([sample],jar=jar,manifest=manifest,active_generation=34)
            self.assertEqual(cm.exception.code,'STALE_GENERATION')
            corrupted=Request(FEATURE_IDS['suppress_feed_item'],34,b'\x01\x02\x01').pack()
            with self.assertRaises(ABIError) as cm:
                exercise_router_frames([corrupted],jar=jar,manifest=manifest,active_generation=34)
            self.assertEqual(cm.exception.code,'NON_BOOLEAN_INPUT')


if __name__ == '__main__':
    unittest.main()
