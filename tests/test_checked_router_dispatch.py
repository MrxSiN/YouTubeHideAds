"""Offline XAX call-chain intent tests; no mock of XAX compiler/device."""
from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
from types import SimpleNamespace
import unittest

from toolchain.xax.checked_router_dispatch import (
    EXTERNAL_PROOFS, reference_invocation_gate,
    make_xax_checked_router_dispatch_graph,
)
from toolchain.xax.dispatch_guard import CONDITIONS, reference_dispatch_gate
from toolchain.xax.store_evidence import GraphClosureError, verify_canonical_graph_store, require_composed_edges

ROOT = Path(__file__).resolve().parents[1]


class ComposedDispatchTests(unittest.TestCase):
    def test_jni_exception_status_is_derived_and_denies_nonzero(self):
        self.assertEqual(EXTERNAL_PROOFS, CONDITIONS[1:])
        for exc, *flags in product((0, 1, 2, 255), repeat=5):
            with self.subTest(exc=exc, flags=flags):
                self.assertEqual(
                    reference_invocation_gate(exc, tuple(flags)),
                    reference_dispatch_gate((int(exc == 0), *flags)),
                )
        self.assertEqual(reference_invocation_gate(0, (1, 1, 1, 1)), 1)
        for exc in (1, 2, 255):
            self.assertEqual(reference_invocation_gate(exc, (1, 1, 1, 1)), 0)

    def test_invalid_input_does_not_authorize(self):
        for args in ((None, (1,) * 4), (True, (1,) * 4),
                     (-1, (1,) * 4), (256, (1,) * 4),
                     (0, (1,) * 3), (0, (1,) * 5),
                     (0, [1] * 4), (0, (1, True, 1, 1)),
                     (0, (1, -1, 1, 1)), (0, (1, 256, 1, 1))):
            with self.subTest(args=args), self.assertRaisesRegex(ValueError, 'XAX_INVOCATION_GATE_INVALID_INPUT'):
                reference_invocation_gate(*args)

    def test_composer_uses_real_call_edges_and_threads_resources(self):
        source = (ROOT / 'toolchain/xax/checked_router_dispatch.py').read_text()
        self.assertIn('Operation.CALL_DIRECT', source)
        self.assertIn('returned[3]', source)
        self.assertIn('IntCompare.EQ', source)
        self.assertIn('Operation.INT_ZERO_EXTEND', source)
        self.assertIn("entity=router['function']", source)
        self.assertIn("entity=guard['function']", source)
        self.assertIn('returned[4], returned[5]', source)
        self.assertIn("'android_execution_verified': False", source)
        self.assertNotIn('class TrueRouter', source)

    def test_composer_requires_external_xax_not_stub_runtime(self):
        if importlib.util.find_spec('xax_compiler') is None:
            with self.assertRaises(ModuleNotFoundError):
                make_xax_checked_router_dispatch_graph({}, {})
        else:
            self.skipTest('Real XAX checkout needs external opt-in structural verification')

    def test_graph_store_requires_five_reports(self):
        with self.assertRaisesRegex(ValueError, 'XAX_FIVE_GRAPHS_REQUIRED'):
            verify_canonical_graph_store({}, {}, {}, {})
        # Missing XAX dependency may precede store-specific failure for five
        # reports, so this test only asserts the cardinality invariant.

    def test_missing_direct_call_edge_rejected_without_compiler(self):
        router = {'function': SimpleNamespace(cid=b'r' * 32)}
        guard = {'function': SimpleNamespace(cid=b'g' * 32)}
        composed = {'graph': SimpleNamespace(references=(b'r' * 32,))}
        with self.assertRaisesRegex(GraphClosureError, 'XAX_COMPOSED_DISPATCH_CALL_EDGES_MISSING'):
            require_composed_edges(router, guard, composed)
        composed['graph'] = SimpleNamespace(references=(b'g' * 32, b'r' * 32))
        require_composed_edges(router, guard, composed)

    def test_identical_call_targets_are_not_two_independent_guards(self):
        fn = SimpleNamespace(cid=b'r' * 32)
        reports = ({'function': fn}, {'function': fn})
        with self.assertRaisesRegex(GraphClosureError, 'XAX_COMPOSED_DISPATCH_CALL_EDGES_MISSING'):
            require_composed_edges(*reports, {'graph': SimpleNamespace(references=(fn.cid,))})

    def test_external_probe_checks_composed_output(self):
        code = (ROOT / 'toolchain/xax/check_router_graph.py').read_text()
        self.assertIn('make_xax_checked_router_dispatch_graph(graph, guard)', code)
        self.assertIn('verify_canonical_graph_store(loader, method, graph, guard, composed)', code)
        self.assertIn("'composed_other_proofs_bound_to_runtime': False", code)
        workflow = (ROOT / '.github/workflows/xax-transport-research.yml').read_text()
        self.assertIn("assert result['exception_clear_derived_from_router_call']", workflow)


if __name__ == '__main__':
    unittest.main()
