"""Contract and fail-closed tests for uncompiled XAX loader-aware JNI graph."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from toolchain.xax.loader_resolution import (
    LoaderResolutionIdentity, CLASS_LOADER_OWNER,
    LOAD_CLASS_METHOD, LOAD_CLASS_DESCRIPTOR, ROUTER_BINARY_CLASS_NAME,
    make_xax_loader_call_plan, make_xax_bound_loader_call_graph,
)
from toolchain.xax.router_call_plan import (
    ROUTER_CLASS, BF_MODULE_LOADER, PRIMITIVE_ARRAY_LOADER,
)

ROOT = Path(__file__).resolve().parents[1]


class LoaderResolutionTests(unittest.TestCase):
    def test_contract_uses_correct_classloader_and_binary_class_name(self):
        identity = LoaderResolutionIdentity()
        self.assertEqual(identity.owner, 'java/lang/ClassLoader')
        self.assertEqual(identity.method, 'loadClass')
        self.assertEqual(identity.descriptor, '(Ljava/lang/String;)Ljava/lang/Class;')
        self.assertEqual(identity.class_name, ROUTER_CLASS.replace('/', '.'))
        self.assertEqual(identity.router_loader, BF_MODULE_LOADER)
        self.assertNotEqual(identity.boot_loader, identity.router_loader)
        self.assertEqual(PRIMITIVE_ARRAY_LOADER, identity.boot_loader)
        self.assertNotIn('/', identity.class_name)

    def test_contract_disallows_loader_and_method_substitutions(self):
        for mutation in (
            {'owner': 'java/lang/Object'},
            {'method': 'findClass'},
            {'descriptor': '(Ljava/lang/Object;)Ljava/lang/Class;'},
            {'class_name': 'org.youtubehideads.bf.SomeOtherClass'},
            {'boot_loader': BF_MODULE_LOADER},
            {'router_loader': b'android.boot'},
        ):
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(ValueError, 'XAX_LOADER_RESOLUTION_IDENTITY_FROZEN'):
                    LoaderResolutionIdentity(**mutation)

    def test_absent_xax_never_returns_a_claim_of_assembled_graph(self):
        if importlib.util.find_spec('xax_jni') is None:
            with self.assertRaisesRegex(RuntimeError, 'PINNED_XAX_COMPILER_NOT_IMPORTED'):
                make_xax_loader_call_plan()
            with self.assertRaises((ImportError, RuntimeError)):
                make_xax_bound_loader_call_graph()
        else:
            self.skipTest('Real pinned XAX compiler present; use external graph check')

    def test_external_graph_check_fails_closed_on_nonexistent_checkout(self):
        with tempfile.TemporaryDirectory(prefix='xax-check-missing-') as tmp:
            output = Path(tmp) / 'must-not-exist.json'
            command = [sys.executable, '-m', 'toolchain.xax.check_router_graph',
                       '--xax-source', str(Path(tmp) / 'no-xax'),
                       '--out', str(output)]
            r = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=20)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('XAX_ROUTER_GRAPH_BLOCKED:', r.stderr)
            self.assertFalse(output.exists())

    def test_xax_graph_source_explicitly_tracks_pending_exception_and_no_runtime(self):
        # This tests claims and wiring, not XAX type-checking without the compiler.
        xax = (ROOT / 'toolchain/xax/loader_resolution.py').read_text()
        dispatch = (ROOT / 'toolchain/xax/router_call_plan.py').read_text()
        for source in (xax, dispatch):
            self.assertIn('jni_exception_check_state_contract', source)
            self.assertIn("'android_execution_verified': False", source)
            self.assertIn('ExceptionCheck', source)
        self.assertIn('class_name_string_creation_implemented', xax)
        self.assertIn("'pending_exception_handled': False", dispatch)


if __name__ == '__main__':
    unittest.main()
