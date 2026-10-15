"""The managed XAX call must remain tied to current executable BF sources."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from toolchain.brainfuck.router import build_router


@unittest.skipUnless(os.environ.get('XAX_SOURCE_DIR'), 'set XAX_SOURCE_DIR to run pinned external compiler')
class ManagedDispatchBuildTests(unittest.TestCase):
    def test_real_compile_is_deterministic_and_rejects_tampered_bf(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            policies = root / 'policies'
            build_router(policies)
            command = [sys.executable, '-B', '-m', 'toolchain.xax.managed_dispatch',
                       '--xax-source', os.environ['XAX_SOURCE_DIR'], '--policies', str(policies),
                       '--out', str(root / 'dispatch')]
            reports = []
            for _ in range(2):
                result = subprocess.run(command, capture_output=True, text=True, timeout=120)
                self.assertEqual(result.returncode, 0, result.stderr)
                reports.append(json.loads(result.stdout))
            self.assertEqual(reports[0], reports[1])
            self.assertEqual(reports[0]['invocation'], 'JVM_INVOKESTATIC')
            self.assertFalse(reports[0]['jni_required'])
            (policies / 'brainfuck-router.jar').write_bytes(b'tampered')
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / 'dispatch/evidence.json').exists())


if __name__ == '__main__':
    unittest.main()
