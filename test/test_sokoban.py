import unittest

from sokoban import find_solution
from constants import *


class TestPath(unittest.TestCase):
    def test_already_solved(self):
        env = [
            [WALL, WALL, WALL],
            [WALL, WALL, GOAL],
            [WALL, WALL, WALL],
        ]
        self.assertIsNotNone(find_solution(env, 5, 0))
        
        env = [
            [BOX, BOX, BOX],
            [BOX, BOX, GOAL],
            [BOX, BOX, BOX],
        ]
        self.assertIsNotNone(find_solution(env, 5, 0))
        
        env = [
            [BOX, BOX, EMPTY],
            [BOX, BOX, GOAL],
            [BOX, BOX, BOX],
        ]
        self.assertIsNotNone(find_solution(env, 2, 0))
        
        env = [
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [GOAL , EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY]
        ]
        self.assertIsNotNone(find_solution(env, 8, 0))
        
        env = [
            [EMPTY, BOX  , EMPTY, EMPTY],
            [BOX  , EMPTY, GOAL , EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNotNone(find_solution(env, 2, 0))
        
        
    def test_basic_puzzles(self):
        env = [
            [EMPTY, BOX  , EMPTY],
            [BOX  , EMPTY, GOAL],
            [EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNotNone(find_solution(env, 0, 1, r=3))
        
        # this puzzle can be solved in 2 moves but not 1
        env = [
            [EMPTY, BOX  , EMPTY],
            [BOX  , BOX  , GOAL],
            [EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNone(find_solution(env, 0, 1, r=3))
        self.assertIsNotNone(find_solution(env, 0, 2, r=3))
        
        env = [
            [EMPTY, BOX  , EMPTY, EMPTY],
            [BOX  , BOX  , EMPTY, EMPTY],
            [EMPTY, EMPTY, BOX  , EMPTY],
            [EMPTY, WALL , GOAL , WALL],
        ]
        self.assertIsNone(find_solution(env, 0, 1, r=3))
        self.assertIsNotNone(find_solution(env, 0, 2, r=3))
        
        env = [
            [EMPTY, WALL , EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, WALL , EMPTY, EMPTY, EMPTY],
            [BOX  , WALL , EMPTY, EMPTY, EMPTY],
            [EMPTY, WALL , EMPTY, GOAL , EMPTY]
        ]
        self.assertIsNotNone(find_solution(env, 20, 1, r=3))
        
        
    
    def test_wall_not_stop(self):
        env = [
            [EMPTY   , EMPTY   , EMPTY, EMPTY],
            [EMPTY   , EMPTY   , WALL , BOX],
            [WALL_TXT, STOP_TXT, BOX  , GOAL],
            [EMPTY   , EMPTY   , EMPTY, EMPTY],
        ]
        
        self.assertIsNone(find_solution(env, 0, 1, r=3))
        self.assertIsNotNone(find_solution(env, 0, 2, r=3))
        
        env = [
            [EMPTY   , EMPTY   , WALL, EMPTY],
            [EMPTY   , EMPTY   , WALL, EMPTY],
            [WALL_TXT, STOP_TXT, WALL, EMPTY],
            [EMPTY   , EMPTY   , WALL, GOAL],
        ]
        
        self.assertIsNotNone(find_solution(env, 0, 1, r=3))
