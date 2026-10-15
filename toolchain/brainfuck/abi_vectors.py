"""Generate reproducible bf-host-v1 conformance vectors from executable BF.

NOT an alternate policy implementation. The result is an audit/test fixture; the
real Android/XAX host will need to pass these before runtime hooks may be enabled.
"""
from __future__ import annotations
import json
from pathlib import Path
from .core import interpret
from .host_abi import ABIError, Request, Reply, FEATURE_IDS, checked_reply, load_programs
from .build import ROOT

VECTOR_PATH=ROOT/'testdata/bf_abi_v1_vectors.json'

def vectors() -> dict:
    programs=load_programs()
    records=[]
    for name, feature_id in FEATURE_IDS.items():
        p=programs[feature_id]
        length=p.code.count(',')
        for variant in ('disabled','eligible'):
            if name=='authorize_seek':
                bits=bytes(([0 if variant=='disabled' else 1]+[1]*5))+int(0x123456789ABCDEF).to_bytes(8,'little')
            elif name=='sponsor_time_window':
                times = (10, 9, 20) if variant == 'disabled' else (10, 11, 20)
                bits=b''.join(value.to_bytes(8,'little') for value in times)
            elif name=='sponsor_skip_pipeline':
                category=bytearray(16)
                category[1]=1
                category[0]=int(variant=='eligible')
                bits=bytes(category)+bytes([1]*5)+int(0x123456789ABCDEF).to_bytes(8,'little')
            elif name=='select_sponsor_category':
                pair_bits=bytearray(16)
                pair_bits[1]=1  # sponsor selected (position is a wire-contract field)
                pair_bits[0]=int(variant=='eligible')
                bits=bytes(pair_bits)
            else:
                flags=[1]*length
                if variant=='disabled':flags[0]=0
                if name=='suppress_video_slot':flags[-1]=0
                bits=bytes(flags)
            req=Request(feature_id,0x34561234,bits)
            raw=interpret(p,req.data)
            if not raw or len(raw)!=(9 if raw[0]==4 else 1):
                raise ABIError('BAD_BF_RESULT_LENGTH')
            reply=Reply(feature_id,req.generation,raw[0],raw[1:])
            try:
                checked_reply(req,reply,active_generation=req.generation)
                status='ACCEPTED'
            except ABIError as exc:
                status=exc.code
            records.append({
                'feature':name, 'feature_id':feature_id, 'code_sha256':p.digest,
                'variant':variant,'request_hex':req.pack().hex(),
                'brainfuck_output_hex':raw.hex(),
                'reply_hex':reply.pack().hex(), 'status':status,
            })
    return {
        'format':'bf-host-v1-vectors',
        'notes':'Synthetic conformance fixtures, not live Android/XAX results',
        'request_size':14,'reply_size':15,'max_payload':256,
        'records':records,
    }

def write() -> Path:
    VECTOR_PATH.parent.mkdir(parents=True,exist_ok=True)
    VECTOR_PATH.write_text(json.dumps(vectors(),indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return VECTOR_PATH

if __name__=='__main__': print(write())
