#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH=.
python3 -m unittest discover -s tests -v
python3 -m toolchain.brainfuck.build --out generated
python3 -m toolchain.brainfuck.build --out generated-optimized --optimize
python3 -m toolchain.brainfuck.router --out generated
python3 -m toolchain.brainfuck.router --out generated-optimized --optimize
python3 -m scripts.verify_linkage
python3 -m toolchain.brainfuck.audit
sha256sum generated/brainfuck-policies.jar generated-optimized/brainfuck-policies.jar \
    generated/brainfuck-router.jar generated-optimized/brainfuck-router.jar
printf '\nThe default build does not invoke external XAX/D8 or build an APK.\n'
printf 'To attempt external-toolchain smoke-link research: XAX_SOURCE_DIR=... D8_BIN=... ./scripts/link_xax_smoke.sh\n'
printf 'Android integration: environment prerequisites are reported below; no APK is built.\n'
python3 -m scripts.probe_android_integration
