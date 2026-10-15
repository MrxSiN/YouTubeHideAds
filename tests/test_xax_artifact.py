"""Synthetic corruption fixtures only: no generated APK here is installable."""
from __future__ import annotations

import hashlib
import io
import struct
import subprocess
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path
from unittest.mock import patch

from toolchain.brainfuck.host_abi import FEATURE_IDS
from toolchain.xax.verify_apk import ArtifactError, inspect_dex, inspect_module_apk
from toolchain.xax.smoke_build import XAXUnavailable, require_pinned_checkout
from scripts.probe_android_integration import XAX_COMMIT


def synthetic_header_dex(names: list[str]) -> bytes:
    """Minimal structural fixture for our bounded verifier, NOT executable DEX."""
    names = list(names)
    data = bytearray(b'\0' * 112)
    data[:8] = b'dex\n039\0'
    struct.pack_into('<I', data, 36, 112)
    struct.pack_into('<I', data, 40, 0x12345678)
    n = len(names)
    offstrings = len(data)
    data.extend(b'\0' * (4*n))
    offtypes = len(data)
    for i in range(n): data.extend(struct.pack('<I', i))
    offclasses = len(data)
    for i in range(n):
        entry = bytearray(32)
        struct.pack_into('<I', entry, 0, i)
        data.extend(entry)
    for i, name in enumerate(names):
        struct.pack_into('<I', data, offstrings+4*i, len(data))
        raw = name.encode('ascii')
        if len(raw) < 128:
            data.append(len(raw))
        else:
            data.extend(bytes((len(raw)&127|128, len(raw)>>7)))
        data.extend(raw+b'\0')
    for loc, val in ((56,n),(60,offstrings),(64,n),(68,offtypes),(96,n),(100,offclasses)):
        struct.pack_into('<I', data, loc, val)
    struct.pack_into('<I', data, 32, len(data))
    data[12:32] = hashlib.sha1(data[32:]).digest()
    struct.pack_into('<I', data, 8, zlib.adler32(data[12:]))
    return bytes(data)


def synthetic_method_dex(classes: list[str], *, method_name: str = "run", extra_classes: set[str] | None = None) -> bytes:
    """Incomplete structural fixture with run methods; NOT executable Android DEX.

    Each policy's method body is deliberately a dummy return-object instruction:
    structural inspection does not establish semantic Brainfuck execution.
    """
    import zlib
    from toolchain.brainfuck.host_abi import FEATURE_IDS
    bf_classes={f'Lorg/youtubehideads/bf/{name};' for name in FEATURE_IDS}
    data=bytearray(b'\0'*112)
    data[:8]=b'dex\n039\0'
    strings=classes+['[B',method_name,'L']
    class_count=len(classes)
    strids=len(data); data.extend(b'\0'*(4*len(strings)))
    typeids=len(data)
    for i in range(class_count+1):data.extend(struct.pack('<I',i))
    protoids=len(data);data.extend(b'\0'*12)
    method_classes=[(i,name) for i,name in enumerate(classes) if name in (bf_classes | (extra_classes or set()))]
    methodids=len(data)
    for i,_ in method_classes:data.extend(struct.pack('<HHI',i,0,class_count+1))
    classdefs=len(data);data.extend(b'\0'*(32*class_count))
    type_list=len(data);data.extend(struct.pack('<IH',1,class_count));data.extend(b'\0\0')
    struct.pack_into('<III',data,protoids,class_count+2,class_count,type_list)
    code_off=len(data)
    # A single shared code item is sufficient for a noninstallable parser fixture.
    data.extend(struct.pack('<HHHHIIH',1,1,0,0,0,1,0x0011))
    for method_index,(class_index,_) in enumerate(method_classes):
        off=len(data)
        def enc(n):
            while True:
                b=n & 127;n >>= 7
                data.append(b | (128 if n else 0))
                if not n:break
        for x in (0,0,1,0,method_index,9,code_off):enc(x)
        struct.pack_into('<I',data,classdefs+32*class_index+24,off)
    for i in range(class_count):struct.pack_into('<I',data,classdefs+32*i,i)
    for i,string in enumerate(strings):
        struct.pack_into('<I',data,strids+4*i,len(data))
        raw=string.encode('ascii')
        data.append(len(raw))
        data.extend(raw+b'\0')
    for offset,value in ((56,len(strings)),(60,strids),(64,class_count+1),(68,typeids),
                         (72,1),(76,protoids),(88,len(method_classes)),(92,methodids),
                         (96,class_count),(100,classdefs)):
        struct.pack_into('<I',data,offset,value)
    struct.pack_into('<I',data,32,len(data))
    struct.pack_into('<I',data,36,112)
    struct.pack_into('<I',data,40,0x12345678)
    data[12:32]=hashlib.sha1(data[32:]).digest()
    struct.pack_into('<I',data,8,zlib.adler32(data[12:]))
    return bytes(data)


def synthetic_apk(*, integrated=False, transport=False, extra_scope='', drop=(), override=None) -> bytes:
    """NOT AN ANDROID APK: deliberately skeletal binary-XML/ELF fixtures."""
    scope = 'com.google.android.youtube' if integrated else 'com.example.target'
    classes = ['Lxax/generated/XaxModule;']
    if transport:
        classes += ['Lorg/youtubehideads/bridge/BinaryTransport;']
    if integrated:
        classes += [f'Lorg/youtubehideads/bf/{x};' for x in FEATURE_IDS]
    elf = bytearray(40); elf[:6] = b'\x7fELF\x02\x01'; struct.pack_into('<H', elf, 18, 183)
    manifest = struct.pack('<HHI', 3, 8, 8)
    files = {
        'AndroidManifest.xml': manifest,
        'META-INF/xposed/module.prop': b'name=YouTubeHideAds Smoke\n',
        'META-INF/xposed/java_init.list': b'xax.generated.XaxModule\n',
        'META-INF/xposed/scope.list': (scope+'\n'+extra_scope).encode('utf-8'),
        'lib/arm64-v8a/libxaxapp.so': bytes(elf),
        'classes.dex': (synthetic_method_dex(classes, method_name='roundTrip',
            extra_classes={'Lorg/youtubehideads/bridge/BinaryTransport;'}) if transport
            else synthetic_method_dex(classes) if integrated else synthetic_header_dex(classes)),
    }
    for name in drop:
        files.pop(name)
    files.update(override or {})
    f = io.BytesIO()
    with zipfile.ZipFile(f, 'w') as z:
        for name, content in files.items():z.writestr(name,content)
    return f.getvalue()


class XAXSmokeToolTests(unittest.TestCase):
    def test_pinned_revision_also_requires_clean_source_tree(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'compiler/src').mkdir(parents=True)
            (root / 'compiler/src/xax_compiler.py').write_text('')
            for status in (' M compiler/src/xax_compiler.py\n', '?? compiler/src/injected.py\n'):
                results = [subprocess.CompletedProcess([], 0, XAX_COMMIT + '\n'),
                           subprocess.CompletedProcess([], 0, status)]
                with patch('toolchain.xax.smoke_build.subprocess.run', side_effect=results):
                    with self.assertRaisesRegex(XAXUnavailable, 'must be clean'):
                        require_pinned_checkout(root)
            results = [subprocess.CompletedProcess([], 0, XAX_COMMIT + '\n'),
                       subprocess.CompletedProcess([], 0, '')]
            with patch('toolchain.xax.smoke_build.subprocess.run', side_effect=results):
                self.assertEqual(require_pinned_checkout(root), root.resolve())

    def test_hard_reject_missing_and_incorrect_revision(self):
        with tempfile.TemporaryDirectory() as p:
            with self.assertRaises(XAXUnavailable):require_pinned_checkout(Path(p))
            (Path(p)/'compiler/src').mkdir(parents=True)
            (Path(p)/'compiler/src/xax_compiler.py').write_text('')
            with self.assertRaises(XAXUnavailable):require_pinned_checkout(Path(p))

    def test_smoke_only_structural_fixture(self):
        result = inspect_module_apk(synthetic_apk(), mode='smoke')
        self.assertEqual(result['linked_brainfuck_class_count'],0)
        self.assertFalse(result['module_runtime_verified'])
        self.assertFalse(result['dex_method_bodies_verified'])
        with self.assertRaises(ArtifactError):
            inspect_module_apk(synthetic_apk(),mode='integrated')

    def test_integrated_descriptor_gate(self):
        result=inspect_module_apk(synthetic_apk(integrated=True),mode='integrated')
        self.assertEqual(result['linked_brainfuck_class_count'],len(FEATURE_IDS))
        with self.assertRaises(ArtifactError):
            inspect_module_apk(synthetic_apk(integrated=True),mode='smoke')
        with self.assertRaises(ArtifactError):
            inspect_module_apk(synthetic_apk(integrated=True),mode='linked_smoke')
        altered = synthetic_apk(integrated=True, override={
            'classes.dex': synthetic_header_dex(['Lxax/generated/XaxModule;',
                 *[f'Lorg/youtubehideads/bf/{x};' for x in list(FEATURE_IDS)[:-1]]]),
        })
        with self.assertRaisesRegex(ArtifactError,'BRAINFUCK_CLASSES_NOT_LINKED'):
            inspect_module_apk(altered,mode='integrated')

    def test_scope_and_metadata_fail_closed(self):
        cases = (
            ({'extra_scope':'com.example.also\n'},'INCORRECT_OR_BROAD_SCOPE'),
            ({'drop':['META-INF/xposed/java_init.list']},'JAVA_ENTRY_MISSING'),
            ({'drop':['META-INF/xposed/module.prop']},'MISSING_XPOSED_PROPERTIES'),
            ({'drop':['AndroidManifest.xml']},'MISSING_MANIFEST'),
            ({'drop':['lib/arm64-v8a/libxaxapp.so']},'MISSING_JNI_LIBRARY'),
            ({'drop':['classes.dex']},'MISSING_DEX'),
            ({'override':{'META-INF/xposed/java_init.list':b'bad.Module\n'}},'INCORRECT_JAVA_ENTRY'),
            ({'override':{'AndroidManifest.xml':b'not xml'}},'INVALID_BINARY_MANIFEST'),
        )
        for kwargs, error in cases:
            with self.subTest(error=error),self.assertRaisesRegex(ArtifactError,error):
                inspect_module_apk(synthetic_apk(**kwargs),mode='smoke')

    def test_dex_integrity_and_class_rejection(self):
        good = synthetic_header_dex(['Lxax/generated/XaxModule;'])
        self.assertEqual(len(inspect_dex(good)['class_descriptors']),1)
        corruptions=[(8,0),(12,8),(32,0),(36,4),(40,5),(56,0xff),(60,0xff), (64,255)]
        for offset,bit in corruptions:
            sample=bytearray(good);sample[offset] ^= (bit or 1)
            with self.subTest(offset=offset), self.assertRaises(ArtifactError):
                inspect_dex(bytes(sample))
        with self.assertRaises(ArtifactError):inspect_dex(good[:30])
        with self.assertRaisesRegex(ArtifactError,'DEX_DUPLICATE_CLASS'):
            inspect_dex(synthetic_header_dex(['Lxax/generated/XaxModule;']*2))

    def test_allows_no_packaged_python_app_features(self):
        # Structural verifiers are build-only Python modules, not Android runtime.
        for module in ('toolchain.xax.smoke_build','toolchain.xax.verify_apk'):
            mod=__import__(module,fromlist=['__file__'])
            self.assertTrue(str(mod.__file__).endswith('.py'))

if __name__=='__main__': unittest.main()
