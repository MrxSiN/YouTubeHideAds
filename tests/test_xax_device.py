"""Device-input integrity tests and opt-in checks against the real XAX compiler."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from scripts.probe_android_integration import XAX_COMMIT
from scripts.verify_xax_device import artifacts, corpus
from toolchain.brainfuck.router import ROUTER_CLASS
from toolchain.xax.link_d8 import merge_unsigned
from tests.test_dex_link import POLICY_CLASSES
from tests.test_xax_artifact import synthetic_apk, synthetic_header_dex, synthetic_method_dex


class XaxDeviceInputTests(unittest.TestCase):
    def test_corpus_pairs_standalone_and_real_bf_router_inputs(self):
        wire, count = corpus()
        self.assertEqual(count, 8926)
        lines = wire.decode().splitlines()
        for standalone, routed in zip(lines[::2], lines[1::2]):
            name, data, expected = standalone.split()
            router, routed_data, routed_expected = routed.split()
            self.assertNotEqual(name, router)
            self.assertEqual(router, 'dispatch_all')
            self.assertEqual(routed_data[2:], data)
            self.assertEqual(expected, routed_expected)

    def test_artifact_drift_is_rejected_before_device_access(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            policies = root / 'policies'
            transport = root / 'transport'
            policies.mkdir()
            transport.mkdir()
            for name in ('brainfuck-policies.jar', 'brainfuck-router.jar'):
                (policies / name).write_bytes(name.encode())
            dex = synthetic_method_dex(POLICY_CLASSES + ['L' + ROUTER_CLASS + ';'],
                                      extra_classes={'L' + ROUTER_CLASS + ';'})
            apk = root / 'linked.apk'
            apk.write_bytes(merge_unsigned(synthetic_apk(), [dex], with_router=True))
            paths = ((apk, 'apk_sha256'), (policies / 'brainfuck-policies.jar', 'bf_jar_sha256'),
                     (policies / 'brainfuck-router.jar', 'bf_router_jar_sha256'))
            apk.with_suffix('.evidence.json').write_text(json.dumps({
                key: hashlib.sha256(path.read_bytes()).hexdigest() for path, key in paths}))
            files = {'transport.xax-store': b'fixture store',
                     'classes.dex': synthetic_header_dex(['Lorg/youtubehideads/bridge/BinaryTransport;']),
                     'libxaxapp.so': b'fixture library'}
            for name, data in files.items():
                (transport / name).write_bytes(data)
            report = {'xax_commit': XAX_COMMIT, 'status': 'XAX_TRANSPORT_COMPILED',
                      'artifacts': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}
            (transport / 'evidence.json').write_text(json.dumps(report))
            harness = root / 'harness.dex'
            harness.write_bytes(synthetic_header_dex(['LXaxTransportProbe;']))
            native_probe = root / 'libxaxprobe.so'
            native_probe.write_bytes(b'fixture native test adapter')
            with patch('scripts.verify_xax_device.verify_jar'), patch('scripts.verify_xax_device.verify_router'):
                ready = artifacts(apk, policies, transport, harness, native_probe)
                self.assertEqual(ready['policies-0.dex'], dex)
                (transport / 'libxaxapp.so').write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError, 'transport hash mismatch'):
                    artifacts(apk, policies, transport, harness, native_probe)
                apk.write_bytes(apk.read_bytes() + b'changed')
                with self.assertRaisesRegex(ValueError, 'linked input hash mismatch'):
                    artifacts(apk, policies, transport, harness, native_probe)


@unittest.skipUnless(os.environ.get('XAX_SOURCE_DIR'), 'set XAX_SOURCE_DIR to run pinned external compiler')
class ExternalXaxBuildTests(unittest.TestCase):
    def test_separate_profiles_compile_with_real_pinned_xax(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for module, out in (('smoke_build', 'lifecycle'), ('transport_build', 'transport')):
                command = [sys.executable, '-B', '-m', 'toolchain.xax.' + module,
                           '--xax-source', os.environ['XAX_SOURCE_DIR'], '--out', str(root / out)]
                if module == 'smoke_build':
                    command.append('--local-research-only')
                result = subprocess.run(command, capture_output=True, text=True, timeout=120)
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads(result.stdout)
                if module == 'smoke_build':
                    self.assertEqual(report['apk_verifier']['mode'], 'smoke')
                    self.assertFalse(report['managed_transport_included'])
                else:
                    self.assertEqual(report['status'], 'XAX_TRANSPORT_COMPILED')
                    self.assertFalse(report['android_executed'])
                    self.assertTrue(report['router_requires_pre_resolved_class_and_method'])
                    self.assertEqual(report['router_exception_status'], 'CALLER_CHECKS_LIVE_JNI_STATE')
                    self.assertEqual(set(report['artifacts']), {'transport.xax-store', 'classes.dex', 'libxaxapp.so'})


if __name__ == '__main__':
    unittest.main()
