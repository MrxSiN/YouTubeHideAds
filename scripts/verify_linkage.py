#!/usr/bin/env python3
"""Verify both actual JVM JARs against the executable BF source and manifest."""
from pathlib import Path
from toolchain.brainfuck.host_link import verify_jar
from toolchain.brainfuck.router import verify_router

for folder,optimized in [('generated',False),('generated-optimized',True)]:
    root=Path(folder)
    registry=verify_jar(root/'brainfuck-policies.jar',root/'policies.json',optimized=optimized)
    router=verify_router(root/'brainfuck-router.jar',root/'router.json',optimize=optimized)
    print(f'{folder}: {len(registry)} source-verified AOT policies + {len(router["policies"])}-branch BF router; Android not verified')
