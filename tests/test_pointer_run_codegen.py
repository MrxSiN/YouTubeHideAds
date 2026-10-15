"""Large pointer-run direct JVM compilation and precise failure precedence."""
from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path
from toolchain.brainfuck.core import parse_source, interpret, BFError
from toolchain.brainfuck.jvm import compile_class
from toolchain.brainfuck.build import ROOT


def policy(code):
    return parse_source('\n'.join((
        '# @feature pointer_run_fixture', '# @purpose Test-only pointer movement bounds.',
        '# @abi bf-host-v1', '# @inputs one binary byte', '# @outputs test byte',
        '# @cells position is the live Brainfuck pointer',
        '# @invariant pointer-run checks must preserve failure precedence',
        '# @safety build-only, never packaged in Android',
        '# @section fixture', code,
    )), require_feature=False)


class PointerRunCodegenTests(unittest.TestCase):
    def test_compacted_pointer_run_fuel_versus_bounds_ordering(self):
        # >2000 forces the long-code path. At tape_size=16, the first
        # invalid pointer step is the 16th; fuel=7 fails earlier.
        cases=(('>'*2000+',.',7,'FUEL_EXHAUSTED'),
               ('>'*2000+',.',20,'POINTER_BOUNDS'),
               ('<'+('>'*1600)+',.',2,'POINTER_BOUNDS'),
               ('>'+('<'*1800)+',.',8,'POINTER_BOUNDS'))
        with tempfile.TemporaryDirectory() as tmp:
            temp=Path(tmp)
            subprocess.run(['javac','-d',str(temp),str(ROOT/'tests/jvm/Runner.java')],
                           check=True,capture_output=True)
            for optimize in (False,True):
                jar=temp/f'pointer_{optimize}.jar'
                with zipfile.ZipFile(jar,'w') as archive:
                    for i,(source,fuel,expected) in enumerate(cases):
                        p=policy(source)
                        with self.assertRaises(BFError) as caught:
                            interpret(p,b'\x80',max_steps=fuel,tape_size=16)
                        self.assertEqual(caught.exception.code,expected)
                        archive.writestr(f'org/youtubehideads/bf/p{i}.class',
                          compile_class(p,f'org/youtubehideads/bf/p{i}',
                                        max_steps=fuel,tape_size=16,optimize=optimize))
                result=subprocess.run(['java','-cp',str(temp)+os.pathsep+str(jar),'Runner'],
                    input=''.join(f'p{i} 80\n' for i in range(len(cases)))+'END\n',
                    text=True,capture_output=True,check=True,timeout=30)
                self.assertEqual(result.stdout.splitlines(),
                    ['ERR '+expected for _src,_fuel,expected in cases])

    def test_pointer_run_in_bounds_and_fuel_exact_on_success(self):
        # Build enough commands for long-code mode, with zero-net pointer drift.
        program=policy(('>'*8+'<'*8)*110+',.')
        self.assertEqual(interpret(program,b'\x4a'),b'\x4a')
        with tempfile.TemporaryDirectory() as tmp:
            temp=Path(tmp)
            subprocess.run(['javac','-d',str(temp),str(ROOT/'tests/jvm/Runner.java')],
                           capture_output=True,check=True)
            for optimized in (False,True):
                jar=temp/f'valid{optimized}.jar'
                with zipfile.ZipFile(jar,'w') as archive:
                    archive.writestr('org/youtubehideads/bf/valid.class',
                        compile_class(program,'org/youtubehideads/bf/valid',optimize=optimized))
                result=subprocess.run(['java','-cp',str(temp)+os.pathsep+str(jar),'Runner'],
                    input='valid 4a\nEND\n',capture_output=True,text=True,check=True)
                self.assertEqual(result.stdout.strip(),'OK 4a')


if __name__=='__main__':
    unittest.main()
