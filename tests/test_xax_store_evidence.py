"""Unit tests for closure rejection, NOT a mock of canonical XAX verification."""
from __future__ import annotations
import unittest
from dataclasses import dataclass
from toolchain.xax.store_evidence import object_closure, GraphClosureError


@dataclass(frozen=True)
class LocalObject:
    cid: bytes
    references: tuple[bytes, ...] = ()
    body: bytes = b''


class XaxGraphStoreClosureTests(unittest.TestCase):
    def test_disconnected_or_missing_dependency_rejected(self):
        a, b = b'1' * 32, b'2' * 32
        with self.assertRaisesRegex(GraphClosureError, 'XAX_MISSING_REFERENCE_CIDS'):
            object_closure((LocalObject(a, (b,)),))
        self.assertEqual(object_closure((LocalObject(a, (b,)), LocalObject(b))),
                         (LocalObject(a, (b,)), LocalObject(b)))

    def test_duplicate_cid_semantically_conflicting_objects_rejected(self):
        cid = b'1' * 32
        with self.assertRaisesRegex(GraphClosureError, 'XAX_CID_OBJECT_CONFLICT'):
            object_closure((LocalObject(cid, body=b'a'), LocalObject(cid, body=b'b')))

    def test_deterministic_closure_and_deduplication(self):
        a = LocalObject(b'a' * 32)
        b = LocalObject(b'b' * 32, (a.cid,))
        self.assertEqual(object_closure((b, a, a, b)), (a, b))


if __name__ == '__main__':
    unittest.main()
