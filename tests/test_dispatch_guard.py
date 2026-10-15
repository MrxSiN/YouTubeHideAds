"""Build-time XAX graph intent tests; runtime graph conformance requires XAX."""
from __future__ import annotations

import importlib.util
from itertools import product
import unittest

from toolchain.xax.dispatch_guard import (
    CONDITIONS, reference_dispatch_gate, make_xax_dispatch_guard_graph,
)
from toolchain.xax.store_evidence import GraphClosureError, root_reachable_closure
from dataclasses import dataclass

@dataclass(frozen=True)
class LocalObject:
    cid: bytes
    references: tuple[bytes, ...] = ()
    body: bytes = b''


class DispatchGuardTests(unittest.TestCase):
    def test_gate_truth_table_includes_nonboolean_flags(self):
        self.assertEqual(CONDITIONS, (
            'jni_exception_clear', 'class_binary_name_verified',
            'defining_loader_verified', 'method_id_nonnull_verified',
            'result_frame_verified'))
        for flags in product((0, 1, 2, 255), repeat=5):
            with self.subTest(flags=flags):
                self.assertEqual(reference_dispatch_gate(flags), int(flags == (1,) * 5))

    def test_gate_rejects_invalid_input(self):
        for flags in ((), (1,) * 4, (1,) * 6, (1, 1, -1, 1, 1),
                      (1, 1, 256, 1, 1), (1, True, 1, 1, 1),
                      (1, 1, '1', 1, 1)):
            with self.subTest(flags=flags):
                with self.assertRaisesRegex(ValueError, 'DISPATCH_GUARD_INVALID_INPUT'):
                    reference_dispatch_gate(flags)

    def test_real_xax_required_to_construct_graph(self):
        if importlib.util.find_spec('xax_compiler') is None:
            with self.assertRaises(ModuleNotFoundError):
                make_xax_dispatch_guard_graph()
        else:
            self.skipTest('Pinned XAX needs a dedicated canonical-store check')


class ReachabilityTests(unittest.TestCase):
    def test_prunes_unreachable_construction_helpers(self):
        root = LocalObject(b'a'*32, (b'b'*32,))
        child = LocalObject(b'b'*32)
        irrelevant = LocalObject(b'z'*32, (b'q'*32,))
        self.assertEqual(root_reachable_closure(root, (irrelevant, child, root)), (root, child))
        self.assertEqual(root_reachable_closure(root, (root, child, child)), (root, child))

    def test_reachable_missing_reference_rejected(self):
        root = LocalObject(b'r'*32, (b'x'*32,))
        with self.assertRaisesRegex(GraphClosureError, 'XAX_MISSING_REACHABLE_REFERENCE'):
            root_reachable_closure(root, (root,))

    def test_rejects_substituted_root_and_cid_conflicts(self):
        root = LocalObject(b'r'*32)
        with self.assertRaisesRegex(GraphClosureError, 'XAX_ROOT_NOT_PRESENT'):
            root_reachable_closure(root, ())
        with self.assertRaisesRegex(GraphClosureError, 'XAX_ROOT_NOT_PRESENT'):
            root_reachable_closure(root, (LocalObject(b'r'*32, body=b'alt'),))
        with self.assertRaisesRegex(GraphClosureError, 'XAX_CID_OBJECT_CONFLICT'):
            root_reachable_closure(root, (root, LocalObject(b'r'*32, body=b'alt')))


if __name__ == '__main__':
    unittest.main()
