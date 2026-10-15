"""Offline APK/DEX structure verifier for an eventual XAX-backed module.

This is test/build infrastructure, never an Android-side policy host. It does
not equate structural verification with installation or functioning hooks.
"""
from __future__ import annotations

import hashlib
import io
from pathlib import Path
import re
import struct
import zipfile
import zlib

from toolchain.brainfuck.host_abi import FEATURE_IDS
from toolchain.brainfuck.router import ROUTER_CLASS
from .dex_methods import inspect_methods, DexMethodsError
from .managed_transport import TRANSPORT_DESCRIPTOR, TRANSPORT_METHOD

MODULE_PACKAGE = 'org.youtubehideads.module'
SMOKE_TARGET = 'com.example.target'
RELEASE_TARGET = 'com.google.android.youtube'
XPOSED_ENTRY = 'xax.generated.XaxModule'


class ArtifactError(ValueError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ArtifactError(code)


def _u32(blob: bytes, offset: int) -> int:
    _require(offset >= 0 and offset + 4 <= len(blob), 'DEX_TRUNCATED')
    return struct.unpack_from('<I', blob, offset)[0]


def _slice(blob: bytes, offset: int, length: int) -> bytes:
    _require(offset >= 0 and length >= 0 and offset + length <= len(blob), 'DEX_BOUNDS')
    return blob[offset:offset+length]


def _decode_uleb(blob: bytes, offset: int) -> tuple[int,int]:
    value = 0
    for index in range(5):
        _require(offset < len(blob), 'DEX_BAD_ULEB')
        b = blob[offset]
        offset += 1
        value |= (b & 127) << (7 * index)
        if not b & 128:
            return value, offset
    raise ArtifactError('DEX_BAD_ULEB')


def inspect_dex(data: bytes) -> dict:
    """Verify SHA1+Adler32 header and extract actually defined class descriptors.

    DEX string decoding here is intentionally restricted to ASCII descriptors;
    non-ASCII ordinary strings are ignored, not decoded as arbitrary UTF-8.
    Method/code verification is outside this bounded structural gate.
    """
    _require(len(data) >= 112, 'DEX_SHORT_HEADER')
    _require(re.fullmatch(rb'dex\n0(?:35|37|38|39|40|41)\x00', data[:8]) is not None,
             'DEX_MAGIC')
    _require(_u32(data, 32) == len(data), 'DEX_FILE_SIZE')
    _require(_u32(data, 36) == 112, 'DEX_HEADER_SIZE')
    _require(_u32(data, 40) == 0x12345678, 'DEX_ENDIAN')
    _require(hashlib.sha1(data[32:]).digest() == data[12:32], 'DEX_SIGNATURE')
    _require(zlib.adler32(data[12:]) == _u32(data, 8), 'DEX_CHECKSUM')
    nstrings, stringoff = _u32(data, 56), _u32(data, 60)
    ntypes, typeoff = _u32(data, 64), _u32(data, 68)
    nclasses, classoff = _u32(data, 96), _u32(data, 100)
    _require(nstrings <= 2000000 and ntypes <= 200000 and nclasses <= 200000,
             'DEX_TABLE_LIMIT')
    _slice(data, stringoff, nstrings * 4)
    _slice(data, typeoff, ntypes * 4)
    _slice(data, classoff, nclasses * 32)
    strings: list[str | None] = []
    for i in range(nstrings):
        offset = _u32(data, stringoff + i * 4)
        _, offset = _decode_uleb(data, offset)
        _require(offset < len(data), 'DEX_STRING_BOUNDS')
        end = data.find(b'\0', offset)
        _require(end >= 0, 'DEX_UNTERMINATED_STRING')
        raw = data[offset:end]
        try:
            strings.append(raw.decode('ascii'))
        except UnicodeDecodeError:
            strings.append(None)
    descriptors: list[str | None] = []
    for i in range(ntypes):
        index = _u32(data, typeoff + i * 4)
        _require(index < nstrings, 'DEX_TYPE_INDEX')
        descriptors.append(strings[index])
    classes: set[str] = set()
    for i in range(nclasses):
        idx = _u32(data, classoff + i * 32)
        _require(idx < ntypes, 'DEX_CLASS_INDEX')
        name = descriptors[idx]
        _require(bool(name and name.startswith('L') and name.endswith(';')),
                 'DEX_CLASS_DESCRIPTOR')
        _require(name not in classes, 'DEX_DUPLICATE_CLASS')
        classes.add(name)
    return {'dex_version': data[4:7].decode('ascii'),
            'class_descriptors': sorted(classes), 'sha256': hashlib.sha256(data).hexdigest()}


def _scope(archive: zipfile.ZipFile) -> str:
    try:
        entries = archive.read('META-INF/xposed/scope.list').decode('utf-8').splitlines()
    except (KeyError, UnicodeDecodeError) as exc:
        raise ArtifactError('SCOPE_MISSING_OR_INVALID') from exc
    _require(len(entries) == 1 and entries[0] in (SMOKE_TARGET, RELEASE_TARGET),
             'INCORRECT_OR_BROAD_SCOPE')
    return entries[0]


def inspect_module_apk(source: bytes | Path, *, mode: str = 'integrated') -> dict:
    """Reject missing Xposed metadata or unlinked Brainfuck classes.

    smoke: controlled-target XAX lifecycle carrier only; cannot be released.
    linked_smoke: controlled-target XAX carrier plus BF DEX, without runtime calls.
    integrated: all registered BF class definitions, run method code items and YouTube-only scope; an APK passing
    still requires runtime tests and real JNI hook wiring to be functional.
    """
    _require(mode in {'smoke','transport_smoke','integrated','linked_smoke','linked_router_smoke'}, 'INVALID_VERIFICATION_MODE')
    contents = source if isinstance(source, bytes) else Path(source).read_bytes()
    try:
        archive = zipfile.ZipFile(io.BytesIO(contents))
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        raise ArtifactError('INVALID_APK_ZIP') from exc
    with archive:
        names = archive.namelist()
        _require(len(names) == len(set(names)), 'DUPLICATE_APK_ENTRY')
        _require(all(n and not n.startswith('/') and '..' not in n.split('/') for n in names),
                 'INVALID_APK_PATH')
        files = set(names)
        _require('AndroidManifest.xml' in files, 'MISSING_MANIFEST')
        manifest = archive.read('AndroidManifest.xml')
        _require(len(manifest) >= 8 and struct.unpack_from('<HHI', manifest) == (3, 8, len(manifest)),
                 'INVALID_BINARY_MANIFEST')
        _require('META-INF/xposed/module.prop' in files, 'MISSING_XPOSED_PROPERTIES')
        try:
            java_entries = archive.read('META-INF/xposed/java_init.list').decode('utf-8').splitlines()
        except (KeyError, UnicodeDecodeError) as exc:
            raise ArtifactError('JAVA_ENTRY_MISSING') from exc
        _require(java_entries == [XPOSED_ENTRY], 'INCORRECT_JAVA_ENTRY')
        scope = _scope(archive)
        _require(scope == (SMOKE_TARGET if mode != 'integrated' else RELEASE_TARGET),
                 'SCOPE_NOT_MATCHING_MODE')
        _require('assets/xposed_init' not in files and 'assets/native_init' not in files,
                 'LEGACY_XPOSED_METADATA')
        _require('lib/arm64-v8a/libxaxapp.so' in files, 'MISSING_JNI_LIBRARY')
        lib = archive.read('lib/arm64-v8a/libxaxapp.so')
        _require(len(lib) >= 20 and lib[:6] == b'\x7fELF\x02\x01'
                 and struct.unpack_from('<H', lib, 18)[0] == 183,
                 'INVALID_ARM64_ELF')
        dex_names = sorted((name for name in names if re.fullmatch(r'classes(?:[2-9]\d*)?\.dex', name)),
                           key=lambda value: int(value[7:-4]) if value != 'classes.dex' else 1)
        _require(bool(dex_names), 'MISSING_DEX')
        parsed = [inspect_dex(archive.read(name)) for name in dex_names]
        classes = [name for dex in parsed for name in dex['class_descriptors']]
        _require(len(classes) == len(set(classes)), 'DUPLICATE_MULTIDEX_CLASS')
        _require('Lxax/generated/XaxModule;' in classes, 'MISSING_MANAGED_ENTRY_CLASS')
        if mode == 'transport_smoke':
            _require(TRANSPORT_DESCRIPTOR in classes, 'XAX_TRANSPORT_CLASS_MISSING')
            carrier_dex = [name for name, parsed_dex in zip(dex_names, parsed)
                           if TRANSPORT_DESCRIPTOR in parsed_dex['class_descriptors']]
            _require(len(carrier_dex) == 1, 'XAX_TRANSPORT_CLASS_AMBIGUOUS')
            try:
                bridge_methods = inspect_methods(archive.read(carrier_dex[0]),
                                                 required_classes={TRANSPORT_DESCRIPTOR})
            except DexMethodsError as exc:
                raise ArtifactError(f'XAX_TRANSPORT_METHOD_TABLE_INVALID: {exc}') from exc
            _require(bridge_methods[TRANSPORT_DESCRIPTOR].get(TRANSPORT_METHOD, {}).get('code_units', 0) > 0,
                     'XAX_TRANSPORT_FORWARDER_MISSING')
        compiled = {f'Lorg/youtubehideads/bf/{name};' for name in FEATURE_IDS}
        seen = set(classes) & compiled
        if mode in {'integrated','linked_smoke','linked_router_smoke'}:
            _require(seen == compiled, 'BRAINFUCK_CLASSES_NOT_LINKED')
            verified_methods = {}
            for name, data in zip(dex_names, parsed):
                relevant = compiled.intersection(data['class_descriptors'])
                if not relevant:
                    continue
                try:
                    per_class = inspect_methods(archive.read(name), required_classes=relevant)
                except DexMethodsError as exc:
                    raise ArtifactError(f'INVALID_POLICY_METHOD_TABLE: {exc}') from exc
                for cls, methods in per_class.items():
                    method = methods.get('run([B)[B')
                    _require(bool(method and method['code_units'] > 0), 'BF_RUN_BODY_MISSING')
                    verified_methods[cls] = method['code_units']
            _require(set(verified_methods) == compiled, 'BRAINFUCK_RUN_METHOD_MISSING')
            if mode == 'linked_router_smoke':
                route_class = 'L'+ROUTER_CLASS+';'
                route_dex = [name for name, info in zip(dex_names, parsed)
                             if route_class in info['class_descriptors']]
                _require(len(route_dex) == 1, 'BF_ROUTER_CLASS_MISSING_OR_AMBIGUOUS')
                try:
                    route_methods = inspect_methods(archive.read(route_dex[0]),
                                                    required_classes={route_class})
                except DexMethodsError as exc:
                    raise ArtifactError(f'BF_ROUTER_METHOD_TABLE_INVALID: {exc}') from exc
                _require(route_methods[route_class].get('run([B)[B', {}).get('code_units',0)>0,
                         'BF_ROUTER_RUN_METHOD_MISSING')
        else:
            _require(not seen, 'SMOKE_MUST_NOT_PRETEND_BF_INTEGRATION')
            verified_methods = {}
        return {
            'mode': mode, 'sha256': hashlib.sha256(contents).hexdigest(),
            'scope': scope, 'libxposed_java_entry': XPOSED_ENTRY,
            'dex_files': dex_names, 'dex_sha256': [item['sha256'] for item in parsed],
            'defined_classes_count': len(classes), 'linked_brainfuck_class_count': len(seen),
            'brainfuck_run_code_units': verified_methods,
            'brainfuck_router_run_present': mode == 'linked_router_smoke',
            'dex_structure_checked': True, 'dex_method_bodies_verified': False,
            'module_runtime_verified': False, 'youtube_functionality_verified': False,
            'jni_transport_structurally_present': mode == 'transport_smoke',
            'jni_transport_runtime_tested': False,
        }


def main() -> None:
    import argparse
    import json
    parser = argparse.ArgumentParser(description='Structural inspection only; NOT proof of runtime functionality')
    parser.add_argument('apk', type=Path)
    parser.add_argument('--mode', choices=['smoke', 'transport_smoke', 'integrated', 'linked_smoke', 'linked_router_smoke'], default='smoke')
    args = parser.parse_args()
    try:
        result = inspect_module_apk(args.apk, mode=args.mode)
    except (ArtifactError, OSError, zipfile.BadZipFile) as exc:
        parser.exit(2, f'APK_VERIFICATION_FAILED: {exc}\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
