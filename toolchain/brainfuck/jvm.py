"""Direct Java 5 JVM class-file emission from validated Brainfuck streams.

No generated Java/Kotlin source, bytecode interpreter or feature policy templates.
The emitted method is a sequence of JVM ops specific to each Brainfuck command.
"""
from __future__ import annotations
import struct
from pathlib import Path
from .core import Program, MAX_STEPS, MAX_OUTPUT, TAPE_SIZE, program_fuel


def u1(x): return struct.pack('>B',x)
def u2(x): return struct.pack('>H',x)
def u4(x): return struct.pack('>I',x)

class Pool:
    def __init__(self):
        self.entries=[]
        self.index={}
    def put(self, typ, payload):
        key=(typ,payload)
        if key not in self.index:
            self.index[key]=len(self.entries)+1
            self.entries.append(u1(typ)+payload)
        return self.index[key]
    def utf(self,s):
        b=s.encode('utf-8')
        return self.put(1,u2(len(b))+b)
    def cls(self,s): return self.put(7,u2(self.utf(s)))
    def string(self,s): return self.put(8,u2(self.utf(s)))
    def integer(self,n): return self.put(3,struct.pack('>i',n))
    def nat(self,n,d): return self.put(12,u2(self.utf(n))+u2(self.utf(d)))
    def method(self,c,n,d): return self.put(10,u2(self.cls(c))+u2(self.nat(n,d)))

class Emitter:
    def __init__(self):
        self.code=bytearray()
        self.labels={}
        self.reloc=[]
    def mark(self,label):
        if label in self.labels: raise ValueError('duplicate label')
        self.labels[label]=len(self.code)
    def op(self,*data): self.code.extend(data)
    def branch(self,opcode,label):
        at=len(self.code)
        self.code.extend((opcode,0,0))
        self.reloc.append((at,label))
    def finalize(self):
        for at,label in self.reloc:
            if label not in self.labels: raise ValueError('missing label '+str(label))
            delta=self.labels[label]-at
            if not -32768<=delta<=32767: raise ValueError('BRANCH_TOO_FAR')
            self.code[at+1:at+3]=struct.pack('>h',delta)
        if len(self.code)>65535: raise ValueError('METHOD_TOO_LARGE')
        return bytes(self.code)


def compile_class(program: Program, class_name: str, *, tape_size:int=TAPE_SIZE,
                  max_steps:int|None=None,max_output:int=MAX_OUTPUT,
                  optimize:bool=False)->bytes:
    max_steps = program_fuel(program) if max_steps is None else max_steps
    if not (2<=tape_size<=32767 and 1<=max_steps<=2**31-1 and 1<=max_output<=32767):
        raise ValueError('invalid resource budget')
    if not class_name or not all(x.isidentifier() for x in class_name.split('/')):
        raise ValueError('invalid class name')
    cp=Pool(); e=Emitter()
    # The JVM limits each method Code array to 65,535 bytes. Very large
    # authentic Brainfuck streams share error paths per bounded region; the
    # policy and all fuel/pointer/output checks are otherwise unchanged.
    compact_errors = len(program.code) > 1500
    region_size = 384
    def error_at(name, index):
        if compact_errors:
            e.branch(0xa7, ('error_region', index // region_size, name))
        else:
            error(name)
    def push(n):
        if -1<=n<=5: e.op(0x03+n)
        elif -128<=n<=127: e.op(0x10,n&255)
        elif -32768<=n<=32767: e.op(0x11,*u2(n&65535))
        else: e.op(0x13,*u2(cp.integer(n)))
    def call(c,n,d):e.op(0xb6,*u2(cp.method(c,n,d)))
    def error(name):
        e.op(0xbb,*u2(cp.cls('java/lang/IllegalStateException')))
        e.op(0x59)
        e.op(0x13,*u2(cp.string(name)))
        e.op(0xb7,*u2(cp.method('java/lang/IllegalStateException','<init>','(Ljava/lang/String;)V')))
        e.op(0xbf)
    def spend(n,index):
        if n>127: raise ValueError('optimizer run too large')
        e.op(0x84,4,(-n)&255)
        e.op(0x15,4)
        e.branch(0x9c,('fuel_ok',index))  # ifge
        error_at('FUEL_EXHAUSTED',index)
        e.mark(('fuel_ok',index))
    # local 0 input; 1 tape byte[]; 2 pointer; 3 input index; 4 remaining steps; 5 output
    push(tape_size);e.op(0xbc,8);e.op(0x4c)  # newarray byte; astore_1
    e.op(0x03,0x3d,0x03,0x3e)  # ptr=0 input index=0
    push(max_steps); e.op(0x36,4)
    e.op(0xbb,*u2(cp.cls('java/io/ByteArrayOutputStream')),0x59)
    e.op(0xb7,*u2(cp.method('java/io/ByteArrayOutputStream','<init>','()V')))
    e.op(0x3a,5)
    code=program.code
    index=0
    last_error_region = None
    while index<len(code):
        if compact_errors and index // region_size != last_error_region:
            region=index//region_size
            last_error_region=region
            e.branch(0xa7, ('region_body', region))
            for name in ('FUEL_EXHAUSTED','POINTER_BOUNDS','OUTPUT_LIMIT'):
                e.mark(('error_region', region, name))
                error(name)
            e.mark(('region_body', region))
        e.mark(('token',index))
        op=code[index]
        if (optimize or compact_errors) and op in '+-':
            end=index
            delta=0
            while end<len(code) and code[end] in '+-' and end-index<127:
                delta+=1 if code[end]=='+' else -1
                end+=1
            spend(end-index,index)
            if delta%256:
                e.op(0x2b,0x1c,0x5c,0x33) # aload_1 iload_2 dup2 baload
                push(delta)
                e.op(0x60,0x54)  # iadd bastore (wrap)
            for skipped in range(index+1,end):
                e.mark(('token',skipped))
            index=end
            continue
        # Long same-direction pointer runs can be lowered as one checked,
        # fuel-accounted pointer displacement. Both original exception classes
        # and their ordering are preserved, including when a run would both
        # exhaust fuel and cross a tape boundary.
        if compact_errors and op in '><':
            end=index+1
            while end<len(code) and code[end]==op and end-index<127:
                end+=1
            n=end-index
            if n>1:
                if op=='>':
                    e.op(0x1c);push(n);e.op(0x60);push(tape_size)
                    e.branch(0xa1,('ptr_run_in_bounds',index))
                    # Before the invalid step, remaining fuel must cover
                    # tape_size-pointer instructions. Otherwise fuel wins.
                    e.op(0x15,4);push(tape_size);e.op(0x1c,0x64)
                else:
                    e.op(0x1c);push(n);e.op(0x64);push(0)
                    e.branch(0xa2,('ptr_run_in_bounds',index))
                    e.op(0x15,4,0x1c);push(1);e.op(0x60)
                e.branch(0xa2,('ptr_run_bounds_first',index))
                error_at('FUEL_EXHAUSTED',index)
                e.mark(('ptr_run_bounds_first',index))
                error_at('POINTER_BOUNDS',index)
                e.mark(('ptr_run_in_bounds',index))
                spend(n,index)
                e.op(0x84,2,n if op=='>' else (-n)&255)
                for skipped in range(index+1,end):
                    e.mark(('token',skipped))
                index=end
                continue
        spend(1,index)
        if op in '><':
            e.op(0x1c);push(1)
            e.op(0x60 if op=='>' else 0x64) # iadd/isub
            e.op(0x3d,0x1c) # istore_2 iload_2
            e.branch(0x9c,('ptr_nonnegative',index))
            error_at('POINTER_BOUNDS',index)
            e.mark(('ptr_nonnegative',index))
            e.op(0x1c);push(tape_size)
            e.branch(0xa1,('ptr_valid',index)) # if_icmplt
            error_at('POINTER_BOUNDS',index)
            e.mark(('ptr_valid',index))
        elif op in '+-':
            e.op(0x2b,0x1c,0x5c,0x33) # aload1 iload2 dup2 baload
            push(1)
            e.op(0x60 if op=='+' else 0x64,0x54)
        elif op==',':
            e.op(0x2b,0x1c,0x1d,0x2a,0xbe) # tape,ptr,inputidx,input.length
            e.branch(0xa1,('input',index))
            push(0)
            e.branch(0xa7,('input_store',index))
            e.mark(('input',index))
            e.op(0x2a,0x1d,0x33) # input[index] (signed)
            e.op(0x84,3,1)       # input index ++
            e.mark(('input_store',index))
            e.op(0x54)           # bastore
        elif op=='.':
            e.op(0x19,5)
            call('java/io/ByteArrayOutputStream','size','()I')
            push(max_output)
            e.branch(0xa1,('output_ok',index))
            error_at('OUTPUT_LIMIT',index)
            e.mark(('output_ok',index))
            e.op(0x19,5,0x2b,0x1c,0x33)
            call('java/io/ByteArrayOutputStream','write','(I)V')
        elif op in '[]':
            e.op(0x2b,0x1c,0x33)
            if op=='[':e.branch(0x99,('token',program.jumps[index]+1)) # ifeq
            else:e.branch(0x9a,('token',program.jumps[index]+1)) # ifne
        index+=1
    e.mark(('token',len(code)))
    e.op(0x19,5)
    call('java/io/ByteArrayOutputStream','toByteArray','()[B')
    e.op(0xb0)
    body=e.finalize()
    classname=cp.cls(class_name)
    parent=cp.cls('java/lang/Object')
    methodname=cp.utf('run');desc=cp.utf('([B)[B');codeidx=cp.utf('Code')
    cp_bytes=b''.join(cp.entries)
    codeattr=u2(12)+u2(6)+u4(len(body))+body+u2(0)+u2(0)
    method=b''.join([u2(0x0009),u2(methodname),u2(desc),u2(1),u2(codeidx),u4(len(codeattr)),codeattr])
    return b''.join([b'\xca\xfe\xba\xbe',u2(0),u2(49),u2(len(cp.entries)+1),cp_bytes,
                    u2(0x0021),u2(classname),u2(parent),u2(0),u2(0),u2(1),method,u2(0)])
