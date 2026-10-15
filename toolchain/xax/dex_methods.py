"""Bounded DEX method-table inspection for build-time Brainfuck linkage.

Parses structural method declarations and code offsets, not ART verification.
Never infer the meaning of a method body from its existence. This file is
build infrastructure; policy behavior stays in the annotated .bf sources.
"""
from __future__ import annotations
import struct

class DexMethodsError(ValueError):
    pass


def _err(code):
    raise DexMethodsError(code)


def _read_u32(buf: bytes, offset: int) -> int:
    if offset < 0 or offset + 4 > len(buf): _err('DEX_METHOD_TRUNCATED')
    return struct.unpack_from('<I', buf, offset)[0]


def _read_u16(buf: bytes, offset: int) -> int:
    if offset < 0 or offset + 2 > len(buf): _err('DEX_METHOD_TRUNCATED')
    return struct.unpack_from('<H', buf, offset)[0]


def _uleb(buf: bytes, off: int) -> tuple[int,int]:
    out = 0
    for n in range(5):
        if off >= len(buf): _err('DEX_METHOD_BAD_ULEB')
        c = buf[off]; off += 1
        if n == 4 and c > 0x0f: _err('DEX_METHOD_ULEB_OVERFLOW')
        out |= (c & 127) << (n*7)
        if c < 128: return out, off
    _err('DEX_METHOD_BAD_ULEB')


def inspect_methods(buf: bytes, *, required_classes: set[str]) -> dict[str, dict]:
    """For required class definitions, list methods and nonempty DEX code items.

    Enforces the public v035+ DEX index format with checked offsets. Does not
    decode every DEX instruction, resolve framework types or certify execution.
    """
    if len(buf) < 112 or buf[:4] != b'dex\n': _err('DEX_METHOD_BAD_HEADER')
    s_count, s_off = _read_u32(buf, 56), _read_u32(buf, 60)
    t_count, t_off = _read_u32(buf, 64), _read_u32(buf, 68)
    p_count, p_off = _read_u32(buf, 72), _read_u32(buf, 76)
    m_count, m_off = _read_u32(buf, 88), _read_u32(buf, 92)
    c_count, c_off = _read_u32(buf, 96), _read_u32(buf, 100)
    if any(n > 2000000 for n in (s_count,t_count,p_count,m_count,c_count)):
        _err('DEX_METHOD_TABLE_LIMIT')
    for n, off, width in ((s_count,s_off,4),(t_count,t_off,4),(p_count,p_off,12),
                          (m_count,m_off,8),(c_count,c_off,32)):
        if off < 0 or off + n*width > len(buf): _err('DEX_METHOD_BAD_TABLE')

    strings = []
    for i in range(s_count):
        pos = _read_u32(buf, s_off + 4*i)
        _,pos = _uleb(buf,pos)
        end = buf.find(b'\0',pos)
        if end < 0: _err('DEX_METHOD_STRING_TRUNCATED')
        try: strings.append(buf[pos:end].decode('ascii'))
        except UnicodeDecodeError: strings.append(None)
    types = []
    for i in range(t_count):
        idx = _read_u32(buf,t_off + i*4)
        if idx >= len(strings): _err('DEX_METHOD_TYPE_INDEX')
        types.append(strings[idx])
    protos = []
    for i in range(p_count):
        _,ret,params_off = struct.unpack_from('<III', buf, p_off + i*12)
        if ret >= len(types): _err('DEX_METHOD_RETURN_TYPE')
        params = []
        if params_off:
            count = _read_u32(buf, params_off)
            if count > 255 or params_off + 4 + count*2 > len(buf): _err('DEX_METHOD_PARAMETERS')
            for j in range(count):
                idx = _read_u16(buf, params_off + 4+j*2)
                if idx >= len(types): _err('DEX_METHOD_PARAMETER_INDEX')
                params.append(types[idx])
        protos.append('(' + ''.join(p or '?' for p in params) + ')' + (types[ret] or '?'))
    method_ids=[]
    for i in range(m_count):
        cls,proto,name = struct.unpack_from('<HHI', buf, m_off+i*8)
        if cls >= len(types) or proto >= len(protos) or name >= len(strings):
            _err('DEX_METHOD_ID_INDEX')
        method_ids.append((types[cls], strings[name], protos[proto]))

    found = {}
    for i in range(c_count):
        cls_idx = _read_u32(buf,c_off+i*32)
        if cls_idx >= len(types): _err('DEX_METHOD_CLASS_INDEX')
        cls_name=types[cls_idx]
        if cls_name not in required_classes: continue
        if cls_name in found: _err('DEX_METHOD_DUPLICATE_CLASS')
        data_off=_read_u32(buf,c_off+i*32+24)
        if not data_off: _err('DEX_METHOD_NO_CLASS_DATA')
        pos=data_off
        counts=[]
        for _ in range(4):
            n,pos=_uleb(buf,pos)
            if n > 1000000: _err('DEX_METHOD_COUNT_LIMIT')
            counts.append(n)
        for field_count in counts[:2]:
            for _ in range(field_count):
                _,pos=_uleb(buf,pos); _,pos=_uleb(buf,pos)
        signatures={}
        for method_count in counts[2:]:
            previous=0
            for _ in range(method_count):
                diff,pos=_uleb(buf,pos)
                method_idx=previous+diff
                previous=method_idx
                _flags,pos=_uleb(buf,pos)
                code_off,pos=_uleb(buf,pos)
                if method_idx >= len(method_ids): _err('DEX_METHOD_CLASS_DATA_INDEX')
                owner,name,signature=method_ids[method_idx]
                if owner != cls_name or not name: _err('DEX_METHOD_CLASS_MISMATCH')
                if code_off:
                    registers = _read_u16(buf,code_off)
                    ins_size = _read_u16(buf,code_off+2)
                    insns_size = _read_u32(buf,code_off+12)
                    if not (registers >= ins_size and 0 < insns_size <= 65535 and
                            code_off+16+2*insns_size <= len(buf)):
                        _err('DEX_METHOD_BAD_CODE_ITEM')
                signatures[name + signature]={'code_offset':code_off,
                                               'code_units':insns_size if code_off else 0}
        found[cls_name]=signatures
    if set(found) != required_classes: _err('DEX_METHOD_CLASSES_MISSING')
    return found
