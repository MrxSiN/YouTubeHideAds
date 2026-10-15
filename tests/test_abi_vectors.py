"""Golden test vectors must be byte-exact and BF-source-derived."""
import json
import unittest
from toolchain.brainfuck.abi_vectors import VECTOR_PATH,vectors
from toolchain.brainfuck.host_abi import Request,Reply

class GoldenVectorsTests(unittest.TestCase):
    def test_checked_in_vectors_match_current_executable_programs(self):
        self.assertEqual(json.loads(VECTOR_PATH.read_text()),vectors())
        for record in vectors()['records']:
            self.assertEqual(Request.unpack(bytes.fromhex(record['request_hex'])).feature_id,record['feature_id'])
            r=Reply.unpack(bytes.fromhex(record['reply_hex']))
            raw=bytes.fromhex(record['brainfuck_output_hex'])
            self.assertEqual((r.action,r.data),(raw[0],raw[1:]))

if __name__=='__main__':unittest.main()
