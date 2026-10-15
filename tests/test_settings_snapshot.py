import itertools
import unittest

from toolchain.brainfuck.build import ROOT
from toolchain.brainfuck.core import interpret, load


class SettingsSnapshotTest(unittest.TestCase):
    def test_all_preference_states(self):
        program = load(ROOT / 'source/brainfuck-runtime/settings_snapshot.bf')
        # Each switch is absent, stored off, or stored on: 3**5 cases.
        for states in itertools.product(((0, 0), (1, 0), (1, 1)), repeat=5):
            raw = [1 if present == 0 else value for present, value in states]
            gated = [bit & raw[0] for bit in raw[1:]]
            data = bytes(b for pair in states for b in pair)
            self.assertEqual(interpret(program, data), bytes(raw + gated), states)


if __name__ == '__main__':
    unittest.main()
