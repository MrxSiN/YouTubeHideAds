"""Missing prerequisites are reported, never interpreted as a successful APK."""
import unittest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch
from scripts.probe_android_integration import probe

class ProbeTests(unittest.TestCase):
    def test_windows_sdk_executable_suffixes_are_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            sdk = Path(folder)
            (sdk / 'build-tools/36.0.0').mkdir(parents=True)
            (sdk / 'build-tools/36.0.0/d8.bat').write_text('')
            (sdk / 'platform-tools').mkdir()
            (sdk / 'platform-tools/adb.exe').write_bytes(b'')
            with patch.dict(os.environ, {'ANDROID_SDK_ROOT': folder, 'ANDROID_HOME': ''}), \
                    patch('scripts.probe_android_integration.shutil.which', return_value=None):
                info = probe()
            for blocker in ('ANDROID_SDK_NOT_FOUND', 'D8_NOT_FOUND', 'ADB_NOT_FOUND'):
                self.assertNotIn(blocker, info['blockers'])
            self.assertIn('VALIDATED_XAX_AD_DISPATCH_NOT_IMPLEMENTED', info['blockers'])

    def test_no_unproven_integration_completion(self):
        info=probe()
        self.assertEqual(info['status'],'BLOCKED')
        self.assertFalse(info['android_apk_tested'])
        self.assertFalse(info['xposed_hooks_tested'])
        self.assertIn('CANONICAL_XAX_AD_HOST_STORE_NOT_CONSTRUCTED',info['blockers'])
        self.assertIn('XAX_REDISTRIBUTION_LICENSE_UNRESOLVED',info['blockers'])
        self.assertEqual(info['scope'], 'PRODUCTION_AD_HOST_ONLY')
        self.assertIn('YOUTUBE_AD_RUNTIME_TEST_NOT_EXECUTED', info['blockers'])
        self.assertNotIn('XAX_MODULE_CLASSLOADER_LOOKUP_NOT_IMPLEMENTED', info['blockers'])

if __name__=='__main__':unittest.main()
