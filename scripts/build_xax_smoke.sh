#!/usr/bin/env bash
# Separate lifecycle APK and byte-array JNI transport; no YouTube hooks.
set -euo pipefail
cd "$(dirname "$0")/.."
: "${XAX_SOURCE_DIR:?Set XAX_SOURCE_DIR to the pinned EXTERNAL XAX checkout}"
export PYTHONPATH=.
python3 -m toolchain.xax.smoke_build \
  --xax-source "$XAX_SOURCE_DIR" \
  --out build/xax-lifecycle-smoke \
  --local-research-only
python3 -m toolchain.xax.verify_apk \
  build/xax-lifecycle-smoke/lifecycle-smoke-unsigned.apk --mode smoke
python3 -m toolchain.xax.transport_build --xax-source "$XAX_SOURCE_DIR" --out build/xax-transport
