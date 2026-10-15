"""Strict annotated Brainfuck source reader and reference semantics.

This Python code is OFF-DEVICE COMPILER INFRASTRUCTURE, not application logic.
The 8-command stream is the sole authority for all feature decisions.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

OPS = frozenset('><+-.,[]')
REQUIRED = frozenset({'feature','purpose','abi','inputs','outputs','cells','invariant','safety'})
ALLOWED = REQUIRED | {'section','note','status','fuel'}
TAPE_SIZE = 4096
MAX_STEPS = 100_000
MAX_OUTPUT = 64

class BFError(ValueError):
    def __init__(self, code: str, line: int | None = None):
        self.code = code
        self.line = line
        super().__init__(f'{code}' + (f' at line {line}' if line else ''))

@dataclass(frozen=True)
class Program:
    name: str
    code: str
    source_map: tuple[int, ...]
    jumps: dict[int, int]
    metadata: dict[str, str]

    @property
    def digest(self) -> str:
        return sha256(self.code.encode('ascii')).hexdigest()


def parse_source(source: str, *, require_feature: bool = True) -> Program:
    annotations: dict[str,str] = {}
    result: list[str] = []
    loc: list[int] = []
    seen_exec = False
    for number, line in enumerate(source.splitlines(),1):
        stripped = line.lstrip(' \t')
        if stripped.startswith('#'):
            body = stripped[1:].strip()
            if body.startswith('@'):
                fields = body[1:].split(None,1)
                key = fields[0] if fields else ''
                if key not in ALLOWED or len(fields)<2 or not fields[1].strip():
                    raise BFError('BAD_ANNOTATION',number)
                if key in annotations and key not in {'section','invariant','note'}:
                    raise BFError('DUPLICATE_ANNOTATION',number)
                if key != 'section' and key != 'note':
                    if seen_exec and (key == 'fuel' or (key in REQUIRED and (key != 'invariant' or key not in annotations))):
                        raise BFError('LATE_HEADER',number)
                    annotations.setdefault(key,fields[1].strip())
            continue
        for ch in line:
            if ch in ' \t\r':
                continue
            if ch not in OPS:
                raise BFError('INVALID_TOKEN',number)
            result.append(ch)
            loc.append(number)
            seen_exec = True
    if not REQUIRED.issubset(annotations):
        raise BFError('MISSING_METADATA')
    if annotations['abi'] != 'bf-host-v1':
        raise BFError('UNKNOWN_ABI')
    if 'fuel' in annotations:
        fuel = annotations['fuel']
        if not fuel.isascii() or not fuel.isdecimal() or str(int(fuel)) != fuel or not 1 <= int(fuel) <= 2**31-1:
            raise BFError('INVALID_FUEL_LIMIT')
    code=''.join(result)
    if not code or (require_feature and not all(op in code for op in (',','.','[',']'))):
        raise BFError('NONEXECUTABLE_FEATURE')
    stack: list[int] = []
    jumps: dict[int,int] = {}
    for index,command in enumerate(code):
        if command=='[':
            stack.append(index)
        elif command==']':
            if not stack:
                raise BFError('UNMATCHED_CLOSE',loc[index])
            start=stack.pop()
            jumps[start]=index
            jumps[index]=start
    if stack:
        raise BFError('UNMATCHED_OPEN',loc[stack[-1]])
    return Program(annotations['feature'],code,tuple(loc),jumps,annotations)


def load(path: Path) -> Program:
    return parse_source(path.read_text(encoding='utf-8'))


def program_fuel(program: Program) -> int:
    return int(program.metadata.get('fuel', MAX_STEPS))

def interpret(program: Program, data: bytes = b'', *, tape_size: int = TAPE_SIZE,
              max_steps: int | None = None, max_output: int = MAX_OUTPUT) -> bytes:
    max_steps = program_fuel(program) if max_steps is None else max_steps
    tape=bytearray(tape_size)
    pc=ptr=ip=steps=0
    output=bytearray()
    code=program.code
    while pc < len(code):
        steps+=1
        if steps > max_steps:
            raise BFError('FUEL_EXHAUSTED',program.source_map[pc])
        op=code[pc]
        if op=='>':
            ptr+=1
            if ptr>=tape_size:
                raise BFError('POINTER_BOUNDS',program.source_map[pc])
        elif op=='<':
            ptr-=1
            if ptr<0:
                raise BFError('POINTER_BOUNDS',program.source_map[pc])
        elif op=='+':
            tape[ptr]=(tape[ptr]+1)&255
        elif op=='-':
            tape[ptr]=(tape[ptr]-1)&255
        elif op==',':
            tape[ptr]=data[ip] if ip<len(data) else 0
            if ip<len(data):
                ip+=1
        elif op=='.':
            if len(output)>=max_output:
                raise BFError('OUTPUT_LIMIT',program.source_map[pc])
            output.append(tape[ptr])
        elif op=='[' and not tape[ptr]:
            pc=program.jumps[pc]
        elif op==']' and tape[ptr]:
            pc=program.jumps[pc]
        pc+=1
    return bytes(output)
