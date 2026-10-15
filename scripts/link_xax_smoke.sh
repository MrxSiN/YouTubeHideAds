#!/usr/bin/env bash
# RESEARCH ONLY: XAX controlled-target lifecycle APK + Brainfuck classes through D8.
# Produces a deterministic unsigned APK with NO XAX-to-BF call/YouTube hooks.
set -euo pipefail
cd "$(dirname "$0")/.."
: "${XAX_SOURCE_DIR:?Set XAX_SOURCE_DIR to the exact pinned external XAX checkout}"
: "${D8_BIN:?Set D8_BIN to an installed Android SDK D8 executable}"
./scripts/build_xax_smoke.sh
PYTHONPATH=. python3 -m toolchain.brainfuck.build --out generated
PYTHONPATH=. python3 -m toolchain.brainfuck.router --out generated
PYTHONPATH=. python3 -m toolchain.xax.link_d8 \
 --xax-smoke-apk build/xax-lifecycle-smoke/lifecycle-smoke-unsigned.apk \
 --jar generated/brainfuck-policies.jar \
 --manifest generated/policies.json \
 --router-jar generated/brainfuck-router.jar \
 --router-manifest generated/router.json \
 --d8 "$D8_BIN" \
 --out build/xax-lifecycle-smoke/bf-packaged-unsigned.apk
PYTHONPATH=. python3 -m toolchain.xax.verify_apk \
 build/xax-lifecycle-smoke/bf-packaged-unsigned.apk --mode linked_router_smoke
