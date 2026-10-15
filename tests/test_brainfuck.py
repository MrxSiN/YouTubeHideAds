"""Validation, conformance, purity, and real JVM-class differential tests."""
from __future__ import annotations
import hashlib,itertools,os,random,subprocess,tempfile,unittest
from pathlib import Path
from toolchain.brainfuck.core import BFError,load,parse_source,interpret,TAPE_SIZE
from toolchain.brainfuck.build import ROOT, FEATURES,build
from toolchain.brainfuck.jvm import compile_class


def specimen(code, feature='test_policy'):
    return '\n'.join([
        '# @feature '+feature,'# @purpose Structural conformance fixture.',
        '# @abi bf-host-v1','# @inputs one binary byte',
        '# @outputs zero or more binary bytes','# @cells 0=counter 1=scratch',
        '# @invariant pointer starts at 0', '# @safety controlled fixture',
        '# @section fixture', code])

class ParseTests(unittest.TestCase):
    def test_comments_and_whitespace_invariant(self):
        base=specimen(',[->+<]>.')
        annotated=base.replace('# @section fixture', '# <[>+-.,] are documentation, not machine instructions\n# @section fixture')
        annotated=annotated.replace(',[->+<]>.', ' , [ - > + < ] > . \n ')
        self.assertEqual(parse_source(base).digest,parse_source(annotated).digest)
        self.assertEqual(interpret(parse_source(base),b'\x81'),b'\x81')
    def test_noncomment_invalid(self):
        for token in ['x', ';', '# foo','🚫','／', '->\nnot brainfuck']:
            with self.subTest(token=token),self.assertRaises(BFError):
                parse_source(specimen(',.'+token))
    def test_bad_annotation(self):
        for replacement in ['# @never abc', '# @abi ', '# @feature bad\n# @feature again']:
            s=specimen(',[->+<]>.')
            if replacement.startswith('# @feature'):s=s.replace('# @feature test_policy',replacement)
            else:s=s.replace('# @abi bf-host-v1',replacement)
            with self.subTest(replacement=replacement),self.assertRaises(BFError):parse_source(s)
    def test_late_header(self):
        src=specimen(',[->+<]>.')
        src=src.replace('# @invariant pointer starts at 0\n','')+'\n# @invariant after source is too late'
        with self.assertRaises(BFError) as cm:parse_source(src)
        self.assertEqual(cm.exception.code,'LATE_HEADER')
    def test_brackets_and_nonexecuting(self):
        for code in ['[,.',',.]',',.', '', '+.']:
            with self.subTest(code=code),self.assertRaises(BFError):parse_source(specimen(code))
    def test_binary_semantics(self):
        self.assertEqual(interpret(parse_source(specimen(',[->+<]>.')),b'\xff'),b'\xff')
        self.assertEqual(interpret(parse_source(specimen(',-[->+<]>.')),b'\x00'),b'\xff')
        self.assertEqual(interpret(parse_source(specimen(',.'),require_feature=False),b''),b'\x00')
        self.assertEqual(interpret(parse_source(specimen('++[-],.'),require_feature=False),b'\x07'),b'\x07')
        self.assertEqual(interpret(parse_source(specimen('+[>+[>+<-]<-]>>.'),require_feature=False),b''),b'\x01')
    def test_bounds_fuel_output(self):
        for code,kw,expected in [('<<,.',{},'POINTER_BOUNDS'),
                                  ('>,.',{'tape_size':2},None),
                                  ('+[+],.',{'max_steps':40},'FUEL_EXHAUSTED'),
                                  (',..',{'max_output':1},'OUTPUT_LIMIT')]:
            p=parse_source(specimen(code),require_feature=False)
            if expected is None:
                self.assertEqual(interpret(p,b'\x12',**kw),b'\x12')
            else:
                with self.subTest(code=code),self.assertRaises(BFError) as cm:
                    interpret(p,b'\x12',**kw)
                self.assertEqual(cm.exception.code,expected)

class FeatureTests(unittest.TestCase):
    def test_deterministic_builds(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)
            first=hashlib.sha256(build(out).read_bytes()).hexdigest()
            second=hashlib.sha256(build(out).read_bytes()).hexdigest()
            self.assertEqual(first,second)

    def test_truth_tables_and_actual_input_dependence(self):
        for path in sorted(FEATURES.rglob('*.bf')):
            p=load(path)
            if p.name in {'authorize_seek','select_sponsor_category','sponsor_skip_pipeline','sponsor_time_window'}:
                continue  # typed 64-bit SponsorBlock policy has its own differential suite
            n=p.metadata['inputs'].count(' (0 or 1)')
            for bits in itertools.product((0,1),repeat=n):
                expect=(1 if all(bits) else 0)
                if p.name=='suppress_video_slot':expect=(1 if all(bits[:-1]) and bits[-1]==0 else 0)
                action={'collapse_filtered_container':2,'reject_ambiguous':3,'authorize_seek':4}.get(p.name,1)
                result=interpret(p,bytes(bits))
                self.assertEqual(result,bytes((action if expect else 0,)),f'{path.name}: {bits}')
            self.assertGreater(n,2)
    def test_jvm_provenance_comment_and_mutation(self):
        import zipfile
        src=next(FEATURES.rglob('suppress_feed_item.bf')).read_text()
        a=parse_source(src)
        b=parse_source(src.replace('# @purpose','# This comment contains illegal-as-code operators ><+-.,[]\n# @purpose'))
        c=parse_source(src.replace('[->>+<<]','[->>++<<]'))
        original_name='org/youtubehideads/bf/feed_original'
        mutated_name='org/youtubehideads/bf/feed_mutated'
        self.assertEqual(compile_class(a,original_name),compile_class(b,original_name))
        self.assertNotEqual(compile_class(a,original_name),compile_class(c,original_name))
        with tempfile.TemporaryDirectory() as directory:
            tmp=Path(directory)
            subprocess.run(['javac','-d',str(tmp/'runner'),str(ROOT/'tests/jvm/Runner.java')],check=True,capture_output=True)
            jar=tmp/'mutant.jar'
            with zipfile.ZipFile(jar,'w') as z:
                z.writestr(original_name+'.class',compile_class(a,original_name))
                z.writestr(mutated_name+'.class',compile_class(c,mutated_name))
            r=subprocess.run(['java','-cp',str(tmp/'runner')+os.pathsep+str(jar),'Runner'],
                     input='feed_original 010101\nfeed_mutated 010101\nEND\n',text=True,capture_output=True,check=True)
            self.assertEqual(r.stdout.splitlines(),['OK 01','OK 02'])

    def test_executable_mutation(self):
        p=next(FEATURES.rglob('suppress_feed_item.bf'))
        src=p.read_text()
        original=parse_source(src)
        mutated=parse_source(src.replace('[->>+<<]','[->>++<<]')) if '[->>+<<]' in src else parse_source(src.replace('[->>+<<','[->>++<<'))
        # Mutation of the emitted Brainfuck action is authoritative, not a comment edit.
        self.assertNotEqual(original.digest,mutated.digest)
        self.assertNotEqual(interpret(original,b'\x01\x01\x01'),interpret(mutated,b'\x01\x01\x01'))

class JVMSafetyTests(unittest.TestCase):
    def test_opcode_families_and_failure_modes(self):
        import zipfile
        from toolchain.brainfuck.jvm import compile_class
        examples=[
            (',[->+<]>.',b'\xff','OK ff'),
            (',-[->+<]>.',b'\x00','OK ff'),
            ('[-],.',b'\x81','OK 81'),
            ('++[-],.',b'\x07','OK 07'),
            (',.',b'','OK 00'),
            (',.',b'\x80','OK 80'),
            ('<<,.',b'','ERR POINTER_BOUNDS'),
            ('+[]',b'','ERR FUEL_EXHAUSTED'),
            (',..',b'\x11','ERR OUTPUT_LIMIT'),
            ('+[>+[>+<-]<-]>>.',b'','OK 01'),
        ]
        with tempfile.TemporaryDirectory() as directory:
            tmp=Path(directory)
            subprocess.run(['javac','-d',str(tmp/'runner'),str(ROOT/'tests/jvm/Runner.java')],check=True,capture_output=True)
            for optimized in (False,True):
                zipname=tmp/f'cases_{optimized}.jar'
                with zipfile.ZipFile(zipname,'w') as jar:
                    for i,(src,data,expected) in enumerate(examples):
                        p=parse_source(specimen(src),require_feature=False)
                        jar.writestr(f'org/youtubehideads/bf/case{i}.class',compile_class(p,f'org/youtubehideads/bf/case{i}',optimize=optimized,max_steps=10000,max_output=1))
                payload=''.join(f'case{i} {data.hex()}\n' for i,(_,data,_) in enumerate(examples))+'END\n'
                result=subprocess.run(['java','-cp',str(tmp/'runner')+os.pathsep+str(zipname),'Runner'],input=payload,text=True,capture_output=True,check=True)
                self.assertEqual(result.stdout.splitlines(),[x[2] for x in examples])

    def test_compact_jvm_error_paths_preserve_all_guards(self):
        """Force region-shared exception paths and execute each real JVM guard."""
        import zipfile
        codes = (
            (',' + '+'*1550 + '.', b'\x01', 'ERR FUEL_EXHAUSTED'),
            ('<' + '+'*1550 + ',.', b'\x01', 'ERR POINTER_BOUNDS'),
            (',..' + '+'*1550, b'\x01', 'ERR OUTPUT_LIMIT'),
        )
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            subprocess.run(['javac','-d',str(root),str(ROOT/'tests/jvm/Runner.java')],check=True,capture_output=True)
            for optimized in (False,True):
                jar=root/f'compact_{optimized}.jar'
                with zipfile.ZipFile(jar,'w') as z:
                    for i,(code,_data,_expected) in enumerate(codes):
                        prog=parse_source(specimen(code),require_feature=False)
                        z.writestr(f'org/youtubehideads/bf/guard{i}.class',
                            compile_class(prog,f'org/youtubehideads/bf/guard{i}',
                                          optimize=optimized,max_steps=100,max_output=1))
                content=''.join(f'guard{i} {data.hex()}\n' for i,(_code,data,_expected) in enumerate(codes))+'END\n'
                result=subprocess.run(['java','-cp',str(root)+os.pathsep+str(jar),'Runner'],input=content,
                                      text=True,capture_output=True,check=True)
                self.assertEqual(result.stdout.splitlines(),[x[2] for x in codes])

class JVMTests(unittest.TestCase):
    def test_aot_differential_real_jvm(self):
        rng=random.Random(35075)
        with tempfile.TemporaryDirectory() as directory:
            td=Path(directory)
            subprocess.run(['javac','-d',str(td/'runner'),str(ROOT/'tests/jvm/Runner.java')],check=True,capture_output=True)
            samples=[]
            for pth in sorted(FEATURES.rglob('*.bf')):
                program=load(pth)
                count=6 if program.name=='authorize_seek' else program.code.count(',')
                if program.name=='select_sponsor_category':
                    choices=[]
                    for idx in range(8):
                        for enabled_mask in range(0,256,17):
                            payload=bytearray(16)
                            for j in range(8):
                                payload[2*j]=(enabled_mask>>j)&1
                            payload[2*idx+1]=1
                            choices.append(bytes(payload))
                elif program.name=='sponsor_time_window':
                    choices=[b''.join(t.to_bytes(8,'little') for t in times) for times in ((0,0,1),(10,9,20),(3,4,5),(1,2,2))]
                elif program.name=='sponsor_skip_pipeline':
                    choices=[]
                    for index in range(8):
                        for enabled in (0,1):
                            category=bytes(val for cat in range(8) for val in (enabled, int(cat==index)))
                            choices.append(category + bytes((1,)*5) + rng.randrange(1,2**63).to_bytes(8,'little'))
                else:
                    choices=(bytes(bits) for bits in itertools.product((0,1),repeat=count if count<=6 else 6))
                for data in choices:
                    bits=data

                    if program.name=='authorize_seek':
                        data+=rng.randrange(1,2**63).to_bytes(8,'little')
                    samples.append((program,data,interpret(program,data)))
                for _ in range(12):
                    if program.name=='sponsor_time_window':
                        times=sorted(rng.randrange(0,1 << 36) for _ in range(3))
                        data=b''.join(t.to_bytes(8,'little') for t in (times if rng.randrange(2) else times[::-1]))
                    elif program.name in ('select_sponsor_category', 'sponsor_skip_pipeline'):
                        idx=rng.randrange(8)
                        data=bytearray(16)
                        for j in range(8): data[2*j]=rng.randrange(2)
                        data[2*idx+1]=1
                        data=bytes(data)
                        if program.name=='sponsor_skip_pipeline':
                            data+=bytes(rng.randrange(2) for _ in range(5)) + rng.randrange(1,2**63).to_bytes(8,'little')
                    else:
                        data=bytes(rng.randrange(2) for _ in range(count))
                    if program.name=='authorize_seek':
                        data+=rng.randrange(1,2**63).to_bytes(8,'little')
                    samples.append((program,data,interpret(program,data)))
            for optimize in (False,True):
                target=td/('opt' if optimize else 'plain')
                jar=build(target,optimize)
                payload=''.join(f'{p.name} {data.hex()}\n' for p,data,_ in samples)+'END\n'
                cp=str(td/'runner')+os.pathsep+str(jar)
                res=subprocess.run(['java','-cp',cp,'Runner'],input=payload,text=True,capture_output=True,check=True)
                lines=res.stdout.splitlines()
                self.assertEqual(len(lines),len(samples),res.stderr)
                for line,(p,inp,expected) in zip(lines,samples):
                    self.assertEqual(line,f'OK {expected.hex()}',f'{p.name} {inp.hex()} optimized={optimize}')

if __name__=='__main__':unittest.main()
