"""Optional external BrainfuckC AArch64 compiler; build tooling, not app code."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
from uuid import uuid4

from .build import FEATURES, ROOT
from .core import load

# Run upstream in a separate interpreter so its bootstrap imports stay isolated.
COMPILE = '''import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from bootstrap.run_policy_native import PolicyCompiler
c = PolicyCompiler(Path(sys.argv[4]))
Path(sys.argv[3]).write_bytes(c.compile(Path(sys.argv[2]).read_bytes()))
'''


def validate_image(image: bytes) -> None:
    """Check the bounded backend's callable layout before publishing its bytes."""
    if (len(image) < 196 or image[:16] != b'\x7fELF\x02\x01\x01' + bytes(9)
            or struct.unpack_from('<HHIQQ', image, 16) != (3, 183, 1, 128, 64)
            or struct.unpack_from('<IIQQQQQQ', image, 64)
            != (1, 5, 0, 0, 0, len(image), len(image), 16384)
            or image[120:124] != b'BFP1' or (len(image) - 128) % 4):
        raise ValueError('invalid BrainfuckC bounded AArch64 callable ELF')


def compile_policy(source: Path, checkout: Path, out: Path) -> dict:
    program = load(source)
    if not program.name.isascii() or not program.name.isidentifier():
        raise ValueError('invalid native policy name')
    checkout = checkout.resolve(strict=True)
    compiler = checkout / 'bootstrap/run_policy_native.py'
    if not compiler.is_file():
        raise FileNotFoundError(f'BrainfuckC policy compiler missing: {compiler}')
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.brainfuckc-', dir=out) as folder:
        work = Path(folder)
        pure = work / 'source.bf'
        pure.write_bytes(program.code.encode('ascii'))
        artifact = work / 'policy.elf'
        subprocess.run([sys.executable, '-B', '-c', COMPILE, str(checkout),
                        str(pure.resolve()), str(artifact.resolve()),
                        str((work / 'stages').resolve())],
                       check=True, capture_output=True, timeout=900)
        image = artifact.read_bytes()
        validate_image(image)
        record = {'source': str(source.resolve()), 'source_sha256': program.digest,
                  'commands': len(program.code), 'artifact': program.name + '.elf',
                  'artifact_sha256': hashlib.sha256(image).hexdigest(),
                  'artifact_bytes': len(image),
                  'compiler_sha256': hashlib.sha256(compiler.read_bytes()).hexdigest(),
                  'stages': json.loads((work / 'stages/stages.json').read_text()),
                  'entry_offset': 128, 'format': 'BFP1_BOUNDED_CALLABLE_AARCH64',
                  'android_executed': False}
        # Inherit the output directory ACL, not TemporaryDirectory's private ACL.
        pending = out / ('.' + uuid4().hex + '.elf')
        try:
            with pending.open('xb') as stream:
                stream.write(image)
            pending.replace(out / record['artifact'])
        finally:
            pending.unlink(missing_ok=True)
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=ROOT / 'build/brainfuckc')
    args = parser.parse_args()
    # Remove stale success evidence before starting a new batch.
    manifest = args.out / 'policies.json'
    manifest.unlink(missing_ok=True)
    (args.out / 'device-result.json').unlink(missing_ok=True)
    records = {}
    for source in sorted(FEATURES.rglob('*.bf')):
        record = compile_policy(source, args.checkout, args.out)
        records[load(source).name] = record
        print(f'{source.name}: {record["artifact_bytes"]} bytes', flush=True)
    manifest.write_text(json.dumps(records, indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
