"""Package pinned DexKit dependencies and source-compiled BF component policy."""
from pathlib import Path
import hashlib
import zipfile

from toolchain.brainfuck.build import ROOT
from toolchain.brainfuck.core import load
from toolchain.brainfuck.jvm import compile_class

# Exact artifacts already present in this workspace's Gradle dependency cache.
DEPENDENCIES = (
    ('org.luckypray/dexkit/2.3.0', 'aar', '8df532c4126b58490667f71127dc57aef62ccf3578d1d17330f2a1cb8836218e'),
    ('com.google.flatbuffers/flatbuffers-java/23.5.26', 'jar', '8d10cac2ea9878896077ba437d76fdb1b9a07f55a863c560bb8a024b04103f8b'),
    ('org.jetbrains.kotlin/kotlin-stdlib/2.4.10', 'jar', '4ec0293bc3751423b203f1d8493251c57c42e73eb6377a6b8560d0974ff0a6df'),
)


def ad_dependencies(output, cache):
    jars, native, evidence = [], [], []
    for relative, extension, digest in DEPENDENCIES:
        matches = list((cache / relative).rglob('*.' + extension))
        if len(matches) != 1 or hashlib.sha256(matches[0].read_bytes()).hexdigest() != digest:
            raise ValueError('missing or mismatched pinned dependency: ' + relative)
        artifact = matches[0]
        evidence.append({'coordinate': relative, 'sha256': digest})
        if extension == 'aar':
            with zipfile.ZipFile(artifact) as archive:
                jar = output / 'dexkit.jar'
                jar.write_bytes(archive.read('classes.jar'))
                jars.append(jar)
                # shortcut: arm64 device route; add other ABI libraries when testing those devices.
                native.append(('lib/arm64-v8a/libdexkit.so', archive.read('jni/arm64-v8a/libdexkit.so')))
        else:
            jars.append(artifact)
    from xax_jvm import _class_file, _Pool
    storage, _ = _class_file('org/youtubehideads/module/AdBindings', (), _Pool(),
                            (('values', '[Ljava/lang/Object;', 0x0049),))
    policy = load(ROOT / 'source/brainfuck-runtime/ad_component.bf')
    image = compile_class(policy, 'org/youtubehideads/bf/classify_ad_component', optimize=True)
    settings = load(ROOT / 'source/brainfuck-runtime/settings_snapshot.bf')
    settings_image = compile_class(settings, 'org/youtubehideads/bf/settings_snapshot', optimize=True)
    jar = output / 'ad-policy-and-bindings.jar'
    with zipfile.ZipFile(jar, 'w') as archive:
        for name, data in (('org/youtubehideads/module/AdBindings.class', storage),
                           ('org/youtubehideads/bf/classify_ad_component.class', image),
                           ('org/youtubehideads/bf/settings_snapshot.class', settings_image)):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            archive.writestr(info, data)
    jars.append(jar)
    return jars, native, {'dependencies': evidence, 'component_policy_sha256': policy.digest,
                           'component_policy_commands': len(policy.code), 'settings_policy_sha256': settings.digest, 'storage_abi': 'public static volatile Object[] values'}
