"""Usage: python3 -m unittest discover -s tests -v"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from blocks import State, dfs, state_error, verify
from experiments import generate_problems

START = State([0, 1, 0, 2, 3])
GOAL = State([2, 3, 4, 5, 0])


class BlocksWorldTests(unittest.TestCase):
    def test_invalid_states(self):
        for support in ([0, 2, 0], [0, 1, 7], [0, 1, 1], [2, 1, 0]):
            self.assertIsNotNone(state_error(support))
        self.assertIsNone(state_error([0, 1, 0, 2, 3]))

    def test_assignment_example(self):
        moves, expanded, elapsed = dfs(START, GOAL)
        self.assertEqual(len(moves), 7)
        self.assertEqual(verify(START, GOAL, moves), "OK")

    def test_verification_detects_errors(self):
        self.assertTrue(verify(START, GOAL, [(2, 0)]).startswith("error in move 1"))
        self.assertTrue(verify(START, GOAL, [(4, 0), (4, 1)]).startswith("error in move 2"))
        self.assertTrue(verify(START, GOAL, [(4, 5)]).startswith("error in move 1"))
        self.assertTrue(verify(START, GOAL, [(5, 0)]).startswith("error: the final"))

    def test_random_problems(self):
        for n, i, start, goal in generate_problems():
            moves, expanded, elapsed = dfs(start, goal)
            self.assertEqual(verify(start, goal, moves), "OK")


if __name__ == "__main__":
    unittest.main()
