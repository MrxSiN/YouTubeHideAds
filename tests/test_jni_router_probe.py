"""Real JDK JNI -> Brainfuck JVM call, isolated to a NON-SHIPPED test probe."""
from __future__ import annotations

import importlib.util
import itertools
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

from toolchain.brainfuck.core import interpret, parse_source
from toolchain.brainfuck.host_abi import FEATURE_IDS, load_programs
from toolchain.brainfuck.router import build_router, selector_map, source_and_manifest
from toolchain.xax.router_call_plan import (
    RouterCallIdentity, make_xax_call_plan, ROUTER_SIGNATURE,
    ROUTER_CLASS_DESCRIPTOR,
)

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(sys.platform.startswith('linux') and shutil.which('gcc')
                     and shutil.which('javac') and shutil.which('java'),
                     'JNI desktop probe needs Linux, GCC and JDK; no Android claim')
class JniRouterProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory(prefix='bf-jni-probe-')
        cls.tmp = Path(cls.directory.name)
        java_home = Path(shutil.which('javac')).resolve().parent.parent
        native = cls.tmp / 'libbfr_jni_probe.so'
        command = [
            'gcc', '-std=c11', '-Wall', '-Wextra', '-Werror', '-fPIC', '-shared',
            '-I' + str(java_home / 'include'),
            '-I' + str(java_home / 'include/linux'),
            '-o', str(native), str(ROOT / 'tests/jni/jni_router_probe.c'),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode:
            raise RuntimeError(f'JNI probe build failed: {result.stderr}')
        result = subprocess.run(
            ['javac', '-d', str(cls.tmp), str(ROOT / 'tests/jni/JniRouterProbe.java')],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode:
            raise RuntimeError(f'JNI caller harness build failed: {result.stderr}')
        cls.jars = {}
        for optimized in (False, True):
            cls.jars[optimized] = build_router(cls.tmp / ('optimized' if optimized else 'baseline'), optimize=optimized)

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    @classmethod
    def invoke(cls, optimized: bool, samples: list[bytes | None], *, include_router: bool = True) -> list[str]:
        command = [
            'java', '-Djava.library.path=' + str(cls.tmp),
            '-cp', str(cls.tmp) + (os.pathsep + str(cls.jars[optimized]) if include_router else ''),
            'JniRouterProbe',
        ]
        result = subprocess.run(command,
            input='\n'.join('NULL' if data is None else data.hex() for data in samples) + '\nEND\n',
            text=True, capture_output=True, timeout=35,
        )
        if result.returncode:
            raise AssertionError(f'JNI JVM process failed: {result.stderr}')
        return result.stdout.splitlines()

    def test_real_native_jni_invokes_all_brainfuck_bodies_both_modes(self):
        programs = load_programs()
        selectors = selector_map()
        fixtures: list[bytes] = []
        for name, selector in selectors.items():
            if name == 'select_sponsor_category':
                for cat in range(8):
                    for toggled in (0, 1):
                        mask = bytes(value for i in range(8) for value in (toggled, int(i == cat)))
                        fixtures.append(bytes((selector,)) + mask)
            elif name == 'sponsor_time_window':
                for values in ((0,0,1),(10,11,15),(3,2,8)):
                    fixtures.append(bytes((selector,))+b''.join(v.to_bytes(8,'little') for v in values))
            elif name == 'sponsor_skip_pipeline':
                for cat in range(8):
                    for enabled in (0,1):
                        category=bytes(x for i in range(8) for x in (enabled,int(cat==i)))
                        fixtures.append(bytes((selector,))+category+bytes((1,)*5)+(100000+cat).to_bytes(8,'little'))
            elif name == 'authorize_seek':
                for bits in itertools.product((0, 1), repeat=6):
                    end = (1 << 50) + 77
                    fixtures.append(bytes((selector,)) + bytes(bits) + end.to_bytes(8, 'little'))
            else:
                count = programs[FEATURE_IDS[name]].code.count(',')
                for values in itertools.product((0, 1), repeat=count):
                    fixtures.append(bytes((selector,)) + bytes(values))
        expected_program = parse_source(source_and_manifest()[0])
        expected = ['OK ' + interpret(expected_program, data).hex() for data in fixtures]
        self.assertGreaterEqual(len(fixtures), 100)
        for optimized in (False, True):
            with self.subTest(optimized=optimized):
                self.assertEqual(self.invoke(optimized, fixtures), expected)

    def test_jni_binary_round_trip_and_invalid_selector(self):
        selector = selector_map()['authorize_seek']
        valid_seek = bytes((selector,)) + b'\x01' * 6 + (0x0102030405060708).to_bytes(8, 'little')
        invalid = bytes((255,)) + b'\xff' * 24
        samples = [valid_seek, invalid, valid_seek, invalid]
        oracle = parse_source(source_and_manifest()[0])
        expected = ['OK ' + interpret(oracle, item).hex() for item in samples]
        self.assertEqual(expected[1], 'OK ')  # rejected selector, never an action
        self.assertTrue(expected[0].startswith('OK 04'))
        for optimize in (False, True):
            self.assertEqual(self.invoke(optimize, samples), expected)

    def test_null_input_exception_survives_native_boundary(self):
        for optimize in (False, True):
            result = self.invoke(optimize, [None, bytes((255,)), None])
            self.assertEqual(result, [
                'ERR java.lang.IllegalArgumentException:NULL_BRAINFUCK_INPUT',
                'OK ',
                'ERR java.lang.IllegalArgumentException:NULL_BRAINFUCK_INPUT',
            ])

    def test_missing_router_class_propagates_resolution_failure(self):
        selector = selector_map()['suppress_feed_item']
        for optimize in (False, True):
            result = self.invoke(optimize, [bytes((selector, 1, 1, 1))], include_router=False)
            self.assertEqual(len(result), 1)
            self.assertTrue(result[0].startswith('ERR java.lang.NoClassDefFoundError:'), result[0])
            self.assertIn('org/youtubehideads/bf/dispatch_all', result[0])

    @classmethod
    def invoke_isolated(cls, optimized: bool, samples: list[str], *, router_jar: bool = True,
                        path_override: Path | None = None) -> list[str]:
        # Router must NOT appear on the system classpath. It is visible only
        # through the URLClassLoader passed as a JNI jobject argument.
        jar = path_override or (cls.jars[optimized] if router_jar else cls.tmp / 'nonexistent-router.jar')
        command = ['java', '-Djava.library.path=' + str(cls.tmp),
                   '-cp', str(cls.tmp), 'JniRouterProbe', str(jar)]
        result = subprocess.run(command, input='\n'.join(samples) + '\nEND\n',
                                capture_output=True, text=True, timeout=35)
        if result.returncode:
            raise AssertionError(f'isolated JNI JVM process failed: {result.stderr}')
        return result.stdout.splitlines()

    def test_module_classloader_isolation_for_both_compiler_modes(self):
        selectors = selector_map()
        feed = bytes((selectors['suppress_feed_item'], 1, 1, 1))
        seek = bytes((selectors['authorize_seek'],)) + b'\x01'*6 + (0x0102030405060708).to_bytes(8,'little')
        oracle = parse_source(source_and_manifest()[0])
        fixtures = [feed, seek, bytes((255,))]
        expected = ['VISIBLE false'] + ['OK ' + interpret(oracle, f).hex() for f in fixtures]
        for optimized in (False, True):
            with self.subTest(optimized=optimized):
                result = self.invoke_isolated(optimized, ['SYSTEM_CLASS_VISIBILITY'] +
                                              ['LOAD:' + f.hex() for f in fixtures])
                self.assertEqual(result, expected)

    def test_class_loader_negative_cases_do_not_fall_back(self):
        selector = selector_map()['suppress_feed_item']
        raw = bytes((selector, 1, 1, 1)).hex()
        for optimized in (False, True):
            with self.subTest(optimized=optimized):
                results = self.invoke_isolated(optimized, [
                    'SYSTEM_CLASS_VISIBILITY', raw, 'LOAD_NULL_LOADER:' + raw,
                    'LOAD:NULL', 'LOAD:' + raw,
                ], router_jar=False)
                self.assertEqual(results[0], 'VISIBLE false')
                self.assertTrue(results[1].startswith('ERR java.lang.NoClassDefFoundError:'), results[1])
                self.assertEqual(results[2], 'ERR java.lang.IllegalArgumentException:NULL_MODULE_CLASS_LOADER')
                self.assertEqual(results[3], 'ERR java.lang.IllegalArgumentException:NULL_BRAINFUCK_INPUT')
                self.assertTrue(results[4].startswith('ERR java.lang.ClassNotFoundException:'), results[4])
                self.assertIn('org.youtubehideads.bf.dispatch_all', results[4])

    def test_isolated_loader_delivers_full_binary_seek_with_extreme_bytes(self):
        selector = selector_map()['authorize_seek']
        samples = [bytes((selector,)) + bytes((1,1,1,1,1,1)) + n.to_bytes(8,'little')
                   for n in (0, 1, 255, 0xFFFFFFFFFFFFFFFF)]
        oracle = parse_source(source_and_manifest()[0])
        expected = ['OK ' + interpret(oracle, f).hex() for f in samples]
        self.assertEqual(len(expected), 4)
        for optimized in (False, True):
            self.assertEqual(self.invoke_isolated(optimized, ['LOAD:' + f.hex() for f in samples]), expected)

    def test_explicit_module_loader_invokes_all_ten_policies(self):
        programs = load_programs()
        samples = []
        for name, selector in selector_map().items():
            if name == 'sponsor_skip_pipeline':
                payload=bytes(x for i in range(8) for x in (1,int(i==5)))+bytes((1,)*5)+(10001).to_bytes(8,'little')
            elif name == 'select_sponsor_category':
                # Every category slot must preserve the exact input bytes.
                payload = bytes(value for i in range(8) for value in (1, int(i == 5)))
            elif name == 'sponsor_time_window':
                payload = b''.join(x.to_bytes(8,'little') for x in (0,10,20))
            elif name == 'authorize_seek':
                payload = bytes((1, 1, 1, 1, 1, 1)) + bytes.fromhex('002000ff81234567')
            else:
                payload = b'\x01' * programs[FEATURE_IDS[name]].code.count(',')
            samples.append(bytes((selector,)) + payload)
        oracle = parse_source(source_and_manifest()[0])
        expected = ['VISIBLE false'] + ['OK ' + interpret(oracle, item).hex() for item in samples]
        for optimized in (False, True):
            self.assertEqual(self.invoke_isolated(optimized,
                ['SYSTEM_CLASS_VISIBILITY'] + ['LOAD:' + item.hex() for item in samples]), expected)

    def test_loaded_class_with_wrong_signature_is_not_executed(self):
        # Temporary test fixture — deliberately wrong method signature;
        # no Java source is packaged in the actual application or JAR.
        fixture = self.tmp / 'wrong-signature'
        pkg = fixture / 'org/youtubehideads/bf'
        pkg.mkdir(parents=True, exist_ok=True)
        source = pkg / 'dispatch_all.java'
        source.write_text('package org.youtubehideads.bf; '
                          'public final class dispatch_all { '
                          'public static byte[] run(int ignored) { return new byte[]{1}; } }\n')
        compiled = subprocess.run(['javac', '-d', str(fixture), str(source)],
                                  capture_output=True, text=True, timeout=30)
        self.assertEqual(compiled.returncode, 0, compiled.stderr)
        sample = bytes((selector_map()['suppress_feed_item'], 1, 1, 1))
        for optimized in (False, True):
            result = self.invoke_isolated(optimized, ['SYSTEM_CLASS_VISIBILITY',
                'LOAD:' + sample.hex()], path_override=fixture)
            self.assertEqual(result[0], 'VISIBLE false')
            self.assertEqual(len(result), 2)
            self.assertTrue(result[1].startswith('ERR java.lang.NoSuchMethodError:'), result[1])
            self.assertIn('run', result[1])

    def test_parent_delegation_is_rejected_by_defining_loader_check(self):
        sample = bytes((selector_map()['suppress_feed_item'], 1, 1, 1))
        oracle = parse_source(source_and_manifest()[0])
        expected = 'OK ' + interpret(oracle, sample).hex()
        for optimized in (False, True):
            result = self.invoke_isolated(optimized, [
                'SYSTEM_CLASS_VISIBILITY', 'LOAD_UNCHECKED:' + sample.hex(),
                'LOAD_PARENT:' + sample.hex(), 'LOAD:' + sample.hex(),
            ])
            self.assertEqual(result, ['VISIBLE false', expected,
                'ERR java.lang.SecurityException:ROUTER_LOADER_PROVENANCE_MISMATCH', expected])

    def test_overridden_load_class_cannot_spoof_router_identity(self):
        raw = bytes((selector_map()['suppress_feed_item'], 1, 1, 1)).hex()
        for optimized in (False, True):
            results = self.invoke_isolated(optimized, [
                'LOAD_SPOOF:' + raw, 'LOAD:' + raw,
                'LOAD_SPOOF:' + raw, 'LOAD:' + raw,
            ])
            self.assertEqual(results[0], 'ERR java.lang.SecurityException:ROUTER_CLASS_NAME_MISMATCH')
            self.assertTrue(results[1].startswith('OK '))
            self.assertEqual(results[0], results[2])
            self.assertEqual(results[1], results[3])

    def test_native_local_reference_cleanup_across_repeated_failures(self):
        raw = bytes((selector_map()['suppress_feed_item'], 1, 1, 1)).hex()
        for optimized in (False, True):
            # A single JNI process exercises cleanup with alternating rejected
            # and accepted lookups; this is not an ART memory-leak proof.
            inputs = ['LOAD_PARENT:' + raw, 'LOAD_SPOOF:' + raw, 'LOAD:' + raw] * 80
            result = self.invoke_isolated(optimized, inputs)
            self.assertEqual(len(result), len(inputs))
            for index in range(0, len(result), 3):
                self.assertEqual(result[index],
                    'ERR java.lang.SecurityException:ROUTER_LOADER_PROVENANCE_MISMATCH')
                self.assertEqual(result[index + 1],
                    'ERR java.lang.SecurityException:ROUTER_CLASS_NAME_MISMATCH')
                self.assertTrue(result[index + 2].startswith('OK '))

    def test_probe_is_not_application_code_and_not_packaged_in_router(self):
        with zipfile.ZipFile(self.jars[False]) as archive:
            self.assertEqual(archive.namelist(), ['org/youtubehideads/bf/dispatch_all.class'])
            self.assertNotIn('JniRouterProbe.class', archive.namelist())
        for path in (ROOT/'tests/jni/JniRouterProbe.java', ROOT/'tests/jni/jni_router_probe.c'):
            self.assertTrue(path.is_file())
            self.assertTrue(path.relative_to(ROOT).parts[0] == 'tests')


class XaxJniCallPlanTests(unittest.TestCase):
    def test_exact_native_signature_is_frozen(self):
        self.assertEqual(ROUTER_CLASS_DESCRIPTOR, 'Lorg/youtubehideads/bf/dispatch_all;')
        self.assertEqual(ROUTER_SIGNATURE, '([B)[B')
        self.assertEqual(RouterCallIdentity().signature, ROUTER_SIGNATURE)
        with self.assertRaisesRegex(ValueError, 'ROUTER_JNI_ABI_FROZEN'):
            RouterCallIdentity(method='invoke')
        with self.assertRaisesRegex(ValueError, 'ROUTER_JNI_ABI_FROZEN'):
            RouterCallIdentity(module_loader=b'android.boot')

    def test_external_xax_plan_requires_imported_compiler(self):
        if importlib.util.find_spec('xax_jni') is None:
            with self.assertRaisesRegex(RuntimeError, 'PINNED_XAX_COMPILER_NOT_IMPORTED'):
                make_xax_call_plan()
        else:
            plan = make_xax_call_plan()
            self.assertEqual(plan['jni_operation'], 'CallStaticObjectMethodA')
            self.assertEqual(plan['jvalue_bytes'], 8)
            self.assertFalse(plan['xax_graph_built'])
            self.assertFalse(plan['android_executed'])


if __name__ == '__main__':
    unittest.main()
