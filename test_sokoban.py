import unittest

from sokoban import findSolution

class TestPath(unittest.TestCase):
    def test_already_solved(self):
        env = [
            [2, 2, 2],
            [2, 2, 1],
            [2, 2, 2],
        ]
        self.assertIsNotNone(findSolution(env, 5, 0))
        
        env = [
            [3, 3, 3],
            [3, 3, 1],
            [3, 3, 3],
        ]
        self.assertIsNotNone(findSolution(env, 5, 0))
        
        env = [
            [3, 3, 0],
            [3, 3, 1],
            [3, 3, 3],
        ]
        self.assertIsNotNone(findSolution(env, 2, 0))
        
        env = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.assertIsNotNone(findSolution(env, 8, 0))
        
        env = [
            [0, 3, 0, 0],
            [3, 0, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.assertIsNotNone(findSolution(env, 2, 0))
        
        
    def test_basic_puzzles(self):
        env = [
            [0, 3, 0],
            [3, 0, 1],
            [0, 0, 0],
        ]
        self.assertIsNotNone(findSolution(env, 0, 1))
        
        # this puzzle can be solved in 2 moves but not 1
        env = [
            [0, 3, 0],
            [3, 3, 1],
            [0, 0, 0],
        ]
        self.assertIsNotNone(findSolution(env, 0, 2))
        self.assertIsNone(findSolution(env, 0, 1))
        
        env = [
            [0, 3, 0, 0],
            [3, 3, 0, 0],
            [0, 0, 3, 0],
            [0, 2, 1, 2],
        ]
        self.assertIsNotNone(findSolution(env, 0, 3))