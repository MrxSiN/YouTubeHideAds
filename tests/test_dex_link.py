"""Offline-only D8/DEX linkage tests; test fixtures are NOT executable APKs."""
from __future__ import annotations
import io
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from tests.test_xax_artifact import synthetic_apk,synthetic_method_dex,synthetic_header_dex
from toolchain.brainfuck.host_abi import FEATURE_IDS
from toolchain.xax.link_d8 import (LinkError, build_linked_apk, collect_d8_outputs,
                                   merge_unsigned, source_archive,validate_policy_dex)
from toolchain.xax.verify_apk import ArtifactError, inspect_module_apk
from toolchain.brainfuck.build import build
from toolchain.brainfuck.router import build_router, ROUTER_CLASS


POLICY_CLASSES=[f'Lorg/youtubehideads/bf/{name};' for name in FEATURE_IDS]


def fake_d8_tool(root, source):
    tool = root / 'fake-d8.py'
    tool.write_text(source)
    tool.chmod(0o755)
    if os.name == 'nt':
        launcher = root / 'fake-d8.cmd'
        launcher.write_text(f'@"{sys.executable}" "{tool}" %*\n')
        return launcher
    return tool


class OfflineDexLinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake_policy_dex=synthetic_method_dex(POLICY_CLASSES)

    def test_all_policy_run_descriptors_and_code_items(self):
        result=validate_policy_dex([self.fake_policy_dex])
        self.assertEqual(result['policy_class_count'],len(FEATURE_IDS))
        self.assertTrue(result['all_run_methods_have_code'])
        self.assertFalse(result['dex_execution_verified'])

    def test_deterministic_structural_multidex_merger(self):
        a=merge_unsigned(synthetic_apk(),[self.fake_policy_dex])
        b=merge_unsigned(synthetic_apk(),[self.fake_policy_dex])
        self.assertEqual(a,b)
        outcome=inspect_module_apk(a,mode='linked_smoke')
        self.assertEqual(outcome['linked_brainfuck_class_count'],len(FEATURE_IDS))
        self.assertEqual(outcome['dex_files'],['classes.dex','classes2.dex'])
        self.assertFalse(outcome['dex_method_bodies_verified'])
        self.assertFalse(outcome['youtube_functionality_verified'])
        with self.assertRaises(ArtifactError):inspect_module_apk(a,mode='integrated')

    def test_structural_fake_dex_without_methods_fails(self):
        fake=synthetic_header_dex(POLICY_CLASSES)
        with self.assertRaisesRegex(LinkError,'INVALID_D8_DEX'):
            validate_policy_dex([fake])
        with self.assertRaisesRegex(LinkError,'INVALID_D8_DEX'):
            merge_unsigned(synthetic_apk(),[fake])

    def test_missing_or_duplicate_policy_class_rejected(self):
        with self.assertRaisesRegex(LinkError,'INCOMPLETE_D8_BRAINFUCK_CLASSES'):
            validate_policy_dex([synthetic_method_dex(POLICY_CLASSES[:-1])])
        with self.assertRaisesRegex(LinkError,'DUPLICATE_BF_CLASS'):
            validate_policy_dex([self.fake_policy_dex,self.fake_policy_dex])

    def test_dex_expected_contiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaisesRegex(LinkError,'D8_EXPECTED_CONTIGUOUS_DEX_OUTPUT'):
                collect_d8_outputs(root)
            (root/'classes.dex').write_bytes(self.fake_policy_dex)
            self.assertEqual(collect_d8_outputs(root),[self.fake_policy_dex])
            (root/'classes3.dex').write_bytes(self.fake_policy_dex)
            with self.assertRaisesRegex(LinkError,'D8_EXPECTED_CONTIGUOUS_DEX_OUTPUT'):
                collect_d8_outputs(root)

    def test_prevent_modifying_signed_apk(self):
        with zipfile.ZipFile(io.BytesIO(synthetic_apk())) as z:
            mapping={name:z.read(name) for name in z.namelist()}
        mapping['META-INF/CERT.RSA']=b'not-a-real-signature'
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,'w') as z:
            for name,data in mapping.items():z.writestr(name,data)
        with self.assertRaisesRegex(LinkError,'SIGNED_APK_MODIFICATION_FORBIDDEN'):
            merge_unsigned(buf.getvalue(),[self.fake_policy_dex])

    def test_fail_closed_d8_and_source_jar(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            jar=build(root/'gen')
            manifest=root/'gen/policies.json'
            self.assertEqual(len(source_archive(jar,manifest,False)),len(FEATURE_IDS))
            base=root/'smoke.apk';base.write_bytes(synthetic_apk())
            with self.assertRaisesRegex(LinkError,'D8_MISSING'):
                build_linked_apk(base=base,jar=jar,manifest=manifest,
                                 d8='a-definitely-missing-d8-tool',out=root/'result.apk')
            self.assertFalse((root/'result.apk').exists())
            jar.write_bytes(b'not a jar')
            with self.assertRaisesRegex(LinkError,'BF_SOURCE_JAR_VERIFICATION_FAILED'):
                build_linked_apk(base=base,jar=jar,manifest=manifest,
                                 d8='a-definitely-missing-d8-tool',out=root/'result.apk')

    def test_reject_unexpected_d8_class_and_v2_signature_marker(self):
        unexpected=synthetic_method_dex(POLICY_CLASSES + ['Lcom/example/Foreign;'])
        with self.assertRaisesRegex(LinkError,'UNEXPECTED_D8_COMPILED_CLASS'):
            validate_policy_dex([unexpected])
        # This marker by itself does not make the ZIP signed; it is a
        # conservative false-positive fail-closed test for an APK v2/v3 block.
        with self.assertRaisesRegex(LinkError,'APK_SIGNING_BLOCK_MODIFICATION_FORBIDDEN'):
            merge_unsigned(synthetic_apk() + b'APK Sig Block 42',[self.fake_policy_dex])

    def test_full_build_adapter_with_fake_d8_not_real_android(self):
        # Integration of CLI, subprocess, manifest and ZIP; deliberately NOT
        # evidence of real D8 output, libxposed execution or BF semantics.
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            jar=build(root/'gen')
            manifest=root/'gen/policies.json'
            base=root/'base.apk';base.write_bytes(synthetic_apk())
            source=root/'structural-fixture.dex';source.write_bytes(self.fake_policy_dex)
            d8=fake_d8_tool(root, '#!/usr/bin/env python3\n'
                          'import pathlib,shutil,sys\n'
                          'dest=pathlib.Path(sys.argv[sys.argv.index("--output")+1])\n'
                          f'shutil.copyfile({str(source)!r},dest/"classes.dex")\n')
            out=root/'linked.apk'
            record=build_linked_apk(base=base,jar=jar,manifest=manifest,
                                    d8=str(d8),out=out)
            self.assertTrue(out.is_file())
            self.assertTrue(out.with_suffix('.evidence.json').is_file())
            self.assertEqual(record['policy_dex']['policy_class_count'],len(FEATURE_IDS))
            self.assertFalse(record['xax_call_graph_reaches_bf'])
            self.assertFalse(record['android_runtime_tested'])
            self.assertFalse(record['signed'])
            self.assertEqual(record['apk']['mode'],'linked_smoke')

    def test_router_dex_code_and_complete_method_link(self):
        with_router=POLICY_CLASSES+['L'+ROUTER_CLASS+';']
        blob=synthetic_method_dex(with_router,extra_classes={'L'+ROUTER_CLASS+';'})
        record=validate_policy_dex([blob],with_router=True)
        self.assertEqual(record['policy_class_count'],len(FEATURE_IDS))
        self.assertEqual(record['router_class_count'],1)
        apk=merge_unsigned(synthetic_apk(),[blob],with_router=True)
        verified=inspect_module_apk(apk,mode='linked_router_smoke')
        self.assertTrue(verified['brainfuck_router_run_present'])
        self.assertFalse(verified['module_runtime_verified'])
        with self.assertRaisesRegex(LinkError,'INCOMPLETE_D8_BRAINFUCK_CLASSES'):
            validate_policy_dex([self.fake_policy_dex],with_router=True)
        with self.assertRaisesRegex(ArtifactError,'BF_ROUTER_CLASS_MISSING_OR_AMBIGUOUS'):
            inspect_module_apk(merge_unsigned(synthetic_apk(),[self.fake_policy_dex]),
                               mode='linked_router_smoke')

    def test_router_d8_adapter_typed_input_and_tamper_rejection(self):
        # Fake D8 only: inspect input JAR arguments and emit structural fixtures.
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            jar=build(root/'gen')
            router=build_router(root/'gen')
            manifest=root/'gen/policies.json'
            rmanifest=root/'gen/router.json'
            base=root/'base.apk';base.write_bytes(synthetic_apk())
            fixture=root/'router-fixture.dex'
            fixture.write_bytes(synthetic_method_dex(POLICY_CLASSES+['L'+ROUTER_CLASS+';'],extra_classes={'L'+ROUTER_CLASS+';'}))
            tool=fake_d8_tool(root, '#!/usr/bin/env python3\n'
                            'import pathlib,shutil,sys\n'
                            'dest=pathlib.Path(sys.argv[sys.argv.index("--output")+1])\n'
                            'assert len([x for x in sys.argv if x.endswith(".jar")])==2\n'
                            f'shutil.copyfile({str(fixture)!r},dest/"classes.dex")\n')
            target=root/'linked-with-router.apk'
            result=build_linked_apk(base=base,jar=jar,manifest=manifest,
                 d8=str(tool),out=target,router_jar=router,router_manifest=rmanifest)
            self.assertEqual(result['apk']['mode'],'linked_router_smoke')
            self.assertTrue(result['apk']['brainfuck_router_run_present'])
            self.assertFalse(result['xax_call_graph_reaches_bf'])
            self.assertTrue(target.is_file())
            with self.assertRaisesRegex(LinkError,'ROUTER_JAR_AND_MANIFEST_REQUIRED_TOGETHER'):
                build_linked_apk(base=base,jar=jar,manifest=manifest,d8=str(tool),
                                 out=root/'bad.apk',router_jar=router)
            # Reject a changed byte in executable router code before invoking D8.
            import zipfile
            with zipfile.ZipFile(router) as z:
                payload=z.read(ROUTER_CLASS+'.class')
            with zipfile.ZipFile(router,'w') as z:
                z.writestr(ROUTER_CLASS+'.class',payload[:-1]+bytes((payload[-1]^1,)))
            with self.assertRaisesRegex(LinkError,'BF_ROUTER_JAR_VERIFICATION_FAILED'):
                build_linked_apk(base=base,jar=jar,manifest=manifest,d8=str(tool),
                      out=root/'tampered.apk',router_jar=router,router_manifest=rmanifest)

    def test_missing_host_apk_dex_fails(self):
        with self.assertRaisesRegex(LinkError,'XAX_APK_HAS_NO_DEX'):
            with zipfile.ZipFile(io.BytesIO(synthetic_apk())) as z:
                items={n:z.read(n) for n in z.namelist() if n != 'classes.dex'}
            b=io.BytesIO()
            with zipfile.ZipFile(b,'w') as z:
                for n,v in items.items():z.writestr(n,v)
            merge_unsigned(b.getvalue(),[self.fake_policy_dex])

if __name__=='__main__':unittest.main()
