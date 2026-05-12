import unittest

from sokoban import findSolution

class TestPath(unittest.TestCase):
    def test_already_solved(self):
        env = [
            [3, 3, 3],
            [3, 3, 2],
            [3, 3, 3],
        ]
        self.assertIsNotNone(findSolution(env, 5, 0))
        
        env = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertIsNotNone(findSolution(env, 8, 0))
        
        
    def test_basic_puzzles(self):
        env = [
            [0, 3, 0],
            [3, 0, 2],
            [0, 0, 0],
        ]
        self.assertIsNotNone(findSolution(env, 0, 1))