"""The module has no standalone UI and its real XAX callbacks must compile."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from toolchain.brainfuck.build import ROOT


class ModuleManifestTests(unittest.TestCase):
    def test_no_standalone_components(self):
        root = ET.parse(ROOT / 'app/AndroidManifest.xml').getroot()
        self.assertEqual(root.get('package'), 'org.youtubehideads.module')
        application = root.find('application')
        self.assertIsNotNone(application)
        self.assertEqual(list(application), [])


@unittest.skipUnless(os.environ.get('XAX_SOURCE_DIR'), 'set XAX_SOURCE_DIR for the real compiler')
class ModuleGraphTests(unittest.TestCase):
    def test_wrong_api_aar_rejected_without_stale_success_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            aar = root / 'wrong.aar'
            aar.write_bytes(b'not the pinned API')
            output = root / 'out'
            output.mkdir()
            (output / 'build-result.json').write_text('{"status":"old success"}')
            result = subprocess.run([sys.executable, '-B', '-m', 'toolchain.xax.module_build',
                '--xax-source', os.environ['XAX_SOURCE_DIR'], '--java-home', str(root),
                '--sdk', str(root), '--api-aar', str(aar), '--out', str(output)],
                capture_output=True, text=True, timeout=60)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('libxposed AAR does not match', result.stderr)
            self.assertFalse((output / 'build-result.json').exists())

    def test_real_store_and_callback_interfaces_compile(self):
        script = '''
import json, sys
from pathlib import Path
from toolchain.xax.smoke_build import require_pinned_checkout
p = require_pinned_checkout(Path(sys.argv[1]))
sys.path.insert(0, str(p / 'compiler/src'))
from toolchain.xax.module_graph import make_module_graph
from xax_compiler import jvm_classfile_general_target
from xax_graph_builder import program_store
from xax_jvm import compile_jvm_bound_target
from xax_android_sdk import parse_classfile
g = make_module_graph()
t = jvm_classfile_general_target()
r = program_store(g['function'], t, g['objects'])
image = compile_jvm_bound_target(r, g['function'].cid, t)
c = parse_classfile(image.class_bytes)
print(json.dumps({'interfaces': c.interfaces, 'methods': [(m.name, m.descriptor) for m in c.methods]}))
'''
        result = subprocess.run([sys.executable, '-B', '-c', script, os.environ['XAX_SOURCE_DIR']],
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(set(report['interfaces']), {
            'android/view/View$OnClickListener', 'io/github/libxposed/api/XposedInterface$Hooker'})
        self.assertIn(['onClick', '(Landroid/view/View;)V'], report['methods'])
        self.assertIn(['intercept', '(Lio/github/libxposed/api/XposedInterface$Chain;)Ljava/lang/Object;'], report['methods'])


if __name__ == '__main__':
    unittest.main()
