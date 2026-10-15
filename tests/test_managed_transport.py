"""Compile-independent structural transport tests; no claim of live XAX lowering."""
from __future__ import annotations
import unittest
from toolchain.xax.managed_transport import TransportIdentity, make_semantics, TRANSPORT_DESCRIPTOR
from toolchain.xax.verify_apk import ArtifactError, inspect_module_apk
from tests.test_xax_artifact import synthetic_apk, synthetic_header_dex, synthetic_method_dex


class ManagedTransportTests(unittest.TestCase):
    def test_contract_is_frozen_and_binary(self):
        spec = TransportIdentity()
        self.assertEqual(spec.owner, TRANSPORT_DESCRIPTOR)
        self.assertEqual(spec.descriptor, '([B)[B')
        self.assertNotEqual(spec.descriptor, '(Ljava/lang/String;)Ljava/lang/String;')
        with self.assertRaisesRegex(ValueError, 'TRANSPORT_ABI_IS_FROZEN'):
            TransportIdentity(descriptor='(I)I')
        with self.assertRaisesRegex(ValueError, 'TRANSPORT_ABI_IS_FROZEN'):
            TransportIdentity(owner='Landroid/app/Activity;')

    def test_canonical_builder_fails_without_pinned_compiler(self):
        # On this host no external XAX checkout is installed.
        # A genuine XAX installation may instead construct the semantic graph.
        try:
            import xax_android_managed  # noqa: F401
        except ImportError:
            with self.assertRaisesRegex(RuntimeError, 'PINNED_XAX_COMPILER_NOT_IMPORTED'):
                make_semantics()
        else:
            self.skipTest('Use real-XAX integration tests on this host')

    def test_transport_forwarder_structural_gate(self):
        report = inspect_module_apk(synthetic_apk(transport=True), mode='transport_smoke')
        self.assertEqual(report['linked_brainfuck_class_count'], 0)
        self.assertTrue(report['jni_transport_structurally_present'])
        self.assertFalse(report['jni_transport_runtime_tested'])
        self.assertFalse(report['module_runtime_verified'])
        with self.assertRaisesRegex(ArtifactError, 'XAX_TRANSPORT_CLASS_MISSING'):
            inspect_module_apk(synthetic_apk(), mode='transport_smoke')
        with self.assertRaisesRegex(ArtifactError, 'XAX_TRANSPORT_METHOD_TABLE_INVALID'):
            inspect_module_apk(synthetic_apk(transport=True, override={
                'classes.dex': synthetic_header_dex(['Lxax/generated/XaxModule;', TRANSPORT_DESCRIPTOR])
            }), mode='transport_smoke')

    def test_reject_wrong_transport_method_name(self):
        with self.assertRaisesRegex(ArtifactError, 'XAX_TRANSPORT_FORWARDER_MISSING'):
            inspect_module_apk(synthetic_apk(transport=True, override={
                'classes.dex': synthetic_method_dex(
                    ['Lxax/generated/XaxModule;', TRANSPORT_DESCRIPTOR],
                    method_name='run', extra_classes={TRANSPORT_DESCRIPTOR})
            }), mode='transport_smoke')

    def test_transport_probe_is_not_integrated_youtube_module(self):
        with self.assertRaises(ArtifactError):
            inspect_module_apk(synthetic_apk(transport=True), mode='integrated')
        with self.assertRaises(ArtifactError):
            inspect_module_apk(synthetic_apk(transport=True), mode='linked_smoke')


if __name__ == '__main__':
    unittest.main()
