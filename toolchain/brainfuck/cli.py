"""Command-line compiler and runtime verification (offline build infrastructure)."""
import argparse
from pathlib import Path
from .core import load, interpret
from .jvm import compile_class


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('command',choices=['validate','interpret','compile'])
    ap.add_argument('source',type=Path)
    ap.add_argument('--input-hex',default='')
    ap.add_argument('--out',type=Path)
    ap.add_argument('--class-name',default='youtubehideads/bf/Policy')
    ap.add_argument('--optimize',action='store_true')
    a=ap.parse_args()
    p=load(a.source)
    if a.command=='validate':print(f'{p.name} {len(p.code)} ops sha256={p.digest}')
    elif a.command=='interpret':print(interpret(p,bytes.fromhex(a.input_hex)).hex())
    else:
        if a.out is None:ap.error('--out required for compile')
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_bytes(compile_class(p,a.class_name,optimize=a.optimize))
        print(f'wrote {a.out}; source sha256={p.digest}')
if __name__=='__main__':main()
