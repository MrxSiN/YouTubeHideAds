"""External compiler boundary checks; no external checkout needed by unit tests."""
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from toolchain.brainfuck.brainfuckc import compile_policy, validate_image
from toolchain.brainfuck.build import FEATURES
from toolchain.brainfuck.core import load
from scripts.verify_brainfuckc_device import corpus, inputs


def image():
    data = bytearray(196)
    data[:16] = b'\x7fELF\x02\x01\x01' + bytes(9)
    struct.pack_into('<HHIQQ', data, 16, 3, 183, 1, 128, 64)
    struct.pack_into('<IIQQQQQQ', data, 64, 1, 5, 0, 0, 0, len(data), len(data), 16384)
    data[120:124] = b'BFP1'
    return bytes(data)


class BrainfuckCTests(unittest.TestCase):
    def test_invalid_elf_rejected(self):
        valid = image()
        validate_image(valid)
        for offset in (0, 4, 18, 24, 32, 64, 96, 104, 120):
            corrupt = bytearray(valid)
            corrupt[offset] ^= 1
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                validate_image(corrupt)
        for bad in (b'', valid[:128], valid + b'\0'):
            with self.assertRaises(ValueError):
                validate_image(bad)

    def test_annotation_stripping_and_atomic_failure(self):
        source = next(FEATURES.rglob('suppress_feed_item.bf'))
        program = load(source)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'bootstrap').mkdir()
            (root / 'bootstrap/run_policy_native.py').write_text('# fake compiler')
            out = root / 'out'

            def emit(command, **kwargs):
                self.assertEqual(Path(command[5]).read_bytes(), program.code.encode('ascii'))
                Path(command[6]).write_bytes(image())
                stages = Path(command[7])
                stages.mkdir()
                (stages / 'stages.json').write_text('{}')

            with patch('toolchain.brainfuck.brainfuckc.subprocess.run', side_effect=emit):
                record = compile_policy(source, root, out)
            artifact = out / record['artifact']
            self.assertEqual(artifact.read_bytes(), image())
            self.assertEqual(record['source_sha256'], program.digest)
            self.assertEqual(record['artifact_sha256'], hashlib.sha256(image()).hexdigest())
            self.assertFalse(record['android_executed'])
            for failure in (OSError('stage unavailable'), subprocess.CalledProcessError(1, 'compiler')):
                with patch('toolchain.brainfuck.brainfuckc.subprocess.run', side_effect=failure):
                    with self.assertRaises(type(failure)):
                        compile_policy(source, root, out)
                self.assertEqual(artifact.read_bytes(), image())
            with patch('toolchain.brainfuck.brainfuckc.subprocess.run', side_effect=emit), \
                    patch('toolchain.brainfuck.brainfuckc.validate_image', side_effect=ValueError('bad ELF')):
                with self.assertRaises(ValueError):
                    compile_policy(source, root, out)
            self.assertEqual(artifact.read_bytes(), image())

    def test_missing_compiler_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                compile_policy(next(FEATURES.rglob('*.bf')), Path(folder), Path(folder) / 'out')

    def test_policy_name_cannot_escape_output_directory(self):
        source = next(FEATURES.rglob('suppress_feed_item.bf')).read_text()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / 'bad.bf'
            path.write_text(source.replace('@feature suppress_feed_item', '@feature ../escape'))
            with self.assertRaisesRegex(ValueError, 'invalid native policy name'):
                compile_policy(path, root, root / 'out')

    def test_device_corpus_requires_current_sources_and_artifacts(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            manifest = {}
            for source in FEATURES.rglob('*.bf'):
                program = load(source)
                (root / (program.name + '.elf')).write_bytes(image())
                manifest[program.name] = {'source_sha256': program.digest,
                    'artifact_sha256': hashlib.sha256(image()).hexdigest()}
            path = root / 'policies.json'
            path.write_text(json.dumps(manifest))
            wire, counts = corpus(root)
            self.assertEqual(len(wire.splitlines()), sum(counts.values()))
            self.assertEqual(counts['suppress_video_slot'], 16)
            self.assertEqual(counts['select_sponsor_category'], 2048)
            self.assertEqual(counts['sponsor_skip_pipeline'], 2080)
            manifest['suppress_feed_item']['source_sha256'] = 'stale'
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'source/artifact mismatch'):
                corpus(root)
            del manifest['suppress_feed_item']
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'policy set mismatch'):
                corpus(root)

    def test_time_vectors_cover_end_exclusion_and_large_values(self):
        program = load(next(FEATURES.rglob('sponsor_time_window.bf')))
        vectors = list(inputs(program))
        self.assertTrue(all(len(data) == 24 for data in vectors))
        self.assertIn((5).to_bytes(8, 'little') + (6).to_bytes(8, 'little') * 2, vectors)
        self.assertTrue(any(int.from_bytes(data[16:], 'little') == (1 << 63) - 1 for data in vectors))


if __name__ == '__main__':
    unittest.main()
