import unittest

from sokoban import findSolution
from constants import *

### env
# 0: empty
# 1: goal
# 2: wall
# >= 3: pushable
# 3: box
# 4: wall text
# 5: is stop text
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
        self.assertIsNotNone(findSolution(env, 0, 1, r=3))
        
        # this puzzle can be solved in 2 moves but not 1
        env = [
            [0, 3, 0],
            [3, 3, 1],
            [0, 0, 0],
        ]
        self.assertIsNone(findSolution(env, 0, 1, r=3))
        self.assertIsNotNone(findSolution(env, 0, 2, r=3))
        
        env = [
            [0, 3, 0, 0],
            [3, 3, 0, 0],
            [0, 0, 3, 0],
            [0, 2, 1, 2],
        ]
        self.assertIsNone(findSolution(env, 0, 1, r=3))
        self.assertIsNotNone(findSolution(env, 0, 2, r=3))
        
        env = [
            [EMPTY, WALL , EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, WALL , EMPTY, EMPTY, EMPTY],
            [BOX  , WALL , EMPTY, EMPTY, EMPTY],
            [EMPTY, WALL , EMPTY, GOAL , EMPTY]
        ]
        self.assertIsNotNone(findSolution(env, 20, 1, r=3))
        
        
    
    def test_wall_not_stop(self):
        env = [
            [EMPTY   , EMPTY   , EMPTY, EMPTY],
            [EMPTY   , EMPTY   , WALL , BOX],
            [WALL_TXT, STOP_TXT, BOX  , GOAL],
            [EMPTY   , EMPTY   , EMPTY, EMPTY],
        ]
        
        self.assertIsNone(findSolution(env, 0, 1, r=3))
        self.assertIsNotNone(findSolution(env, 0, 2, r=3))
        
        env = [
            [EMPTY   , EMPTY   , WALL, EMPTY],
            [EMPTY   , EMPTY   , WALL, EMPTY],
            [WALL_TXT, STOP_TXT, WALL, EMPTY],
            [EMPTY   , EMPTY   , WALL, GOAL],
        ]
        
        self.assertIsNotNone(findSolution(env, 0, 1, r=3))
