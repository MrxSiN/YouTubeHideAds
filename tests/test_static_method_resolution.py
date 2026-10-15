"""Static-method lookup source contract, not an Android or XAX build oracle."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import unittest
from toolchain.xax.static_method_resolution import (
    StaticMethodIdentity, make_xax_static_method_resolution_plan,
    make_xax_bound_static_method_resolution_graph)
from toolchain.xax.router_call_plan import RouterCallIdentity

ROOT = Path(__file__).resolve().parents[1]


class StaticMethodResolutionTests(unittest.TestCase):
    def test_exact_router_identity_and_loader_are_frozen(self):
        item = StaticMethodIdentity()
        router = RouterCallIdentity()
        self.assertEqual((item.owner, item.name, item.descriptor),
            (router.owner, router.method, router.signature))
        self.assertEqual(item.defining_loader, router.module_loader)
        self.assertEqual(item.descriptor, '([B)[B')
        self.assertEqual(item.owner, 'org/youtubehideads/bf/dispatch_all')

    def test_no_substituted_method_class_or_loader(self):
        for change in ({'owner': 'java/lang/Object'}, {'name': 'runUnsafe'},
                       {'descriptor': '([B)Z'}, {'defining_loader': b'android.boot'}):
            with self.subTest(change=change):
                with self.assertRaisesRegex(ValueError, 'XAX_STATIC_METHOD_IDENTITY_FROZEN'):
                    StaticMethodIdentity(**change)

    def test_external_pinned_xax_required(self):
        if importlib.util.find_spec('xax_jni') is None:
            with self.assertRaisesRegex(RuntimeError, 'PINNED_XAX_COMPILER_NOT_IMPORTED'):
                make_xax_static_method_resolution_plan()
            with self.assertRaises((ImportError, RuntimeError)):
                make_xax_bound_static_method_resolution_graph()
        else:
            self.skipTest('Use the pinned external XAX conformance command')

    def test_method_graph_contains_checked_jni_call_without_false_success(self):
        s = (ROOT / 'toolchain/xax/static_method_resolution.py').read_text()
        self.assertIn("'GetStaticMethodID'", s)
        self.assertIn('jni_get_static_method_id_contract', s)
        self.assertIn('jni_exception_check_contract', s)
        self.assertIn("'method_id_nonnull_verified': False", s)
        self.assertIn("'exception_branch_implemented': False", s)
        s = (ROOT / 'toolchain/xax/check_router_graph.py').read_text()
        self.assertIn('make_xax_bound_static_method_resolution_graph', s)
        self.assertIn('verified_defining_loader_required', s)


if __name__ == '__main__':
    unittest.main()
