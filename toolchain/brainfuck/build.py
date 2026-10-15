"""Deterministically build JVM classes and a JAR from annotated feature files."""
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
from .core import load, program_fuel
from .jvm import compile_class
ROOT=Path(__file__).resolve().parents[2]
FEATURES=ROOT/'source/brainfuck'

def build(out:Path, optimize:bool=False):
    out.mkdir(parents=True,exist_ok=True)
    registry={}
    jar=out/'brainfuck-policies.jar'
    with zipfile.ZipFile(jar,'w') as z:
        for path in sorted(FEATURES.rglob('*.bf')):
            p=load(path)
            if p.name in registry:raise ValueError(f'duplicate feature id {p.name}')
            cls=f'org/youtubehideads/bf/{p.name}'
            data=compile_class(p,cls,optimize=optimize)
            entry=cls+'.class'
            meta=zipfile.ZipInfo(entry,(1980,1,1,0,0,0))
            meta.compress_type=zipfile.ZIP_DEFLATED
            meta.external_attr=0o644<<16
            z.writestr(meta,data)
            registry[p.name]={'source':str(path.relative_to(ROOT)),'sha256':p.digest,
                              'class':cls,'method':'run([B)[B','commands':len(p.code),
                              'fuel_limit':program_fuel(p)}
    (out/'policies.json').write_text(json.dumps(registry,indent=2,sort_keys=True)+'\n')
    print(f'{len(registry)} Brainfuck policies -> {jar} sha256={hashlib.sha256(jar.read_bytes()).hexdigest()}')
    return jar
if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=ROOT/'generated');a.add_argument('--optimize',action='store_true')
    args=a.parse_args();build(args.out,args.optimize)
