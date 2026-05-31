import unittest

from path import find_path
from constants import *

class TestPath(unittest.TestCase):
    def test_already_satisfied(self):
        env = [
            [0, 1],
            [0, 2]
        ]
        self.assertIsNotNone(find_path(env, 1, 0))
        
        env = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        self.assertIsNotNone(find_path(env, 4, 0))
    
      
    def test_movement(self):
        env = [
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
        ]
        self.assertIsNotNone(find_path(env, 0, 1))
        
        env = [
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.assertIsNotNone(find_path(env, 0, 1))
        
        env = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 1],
        ]
        self.assertIsNotNone(find_path(env, 0, 2))
        
        env = [
            [31, 3, 0],
            [3, 7, 1],
            [1146, 3, 3],
        ]
        self.assertIsNotNone(find_path(env, 2, 1))
    
    def test_symmetry(self):
        env = [
            [GOAL , EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNotNone(find_path(env, 15, 2))
        
        env = [
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, GOAL],
        ]
        self.assertIsNotNone(find_path(env, 0, 2))
        
        env = [
            [EMPTY, EMPTY, EMPTY, GOAL],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNotNone(find_path(env, 12, 2))
        
        env = [
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [GOAL , EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNotNone(find_path(env, 3, 2))
    
    
    def test_obstacles(self):
        env = [
            [EMPTY, EMPTY, EMPTY],
            [WALL , WALL , WALL],
            [EMPTY, EMPTY, GOAL],
        ]
        self.assertIsNone(find_path(env, 0, 2))
        
        env = [
            [EMPTY, WALL , EMPTY],
            [WALL , WALL , EMPTY],
            [EMPTY, EMPTY, GOAL],
        ]
        self.assertIsNone(find_path(env, 0, 2))
        
        env = [
            [EMPTY, WALL, EMPTY],
            [EMPTY, WALL, EMPTY],
            [EMPTY, WALL, GOAL],
        ]
        self.assertIsNone(find_path(env, 0, 2))
        
        env = [
            [EMPTY, WALL , EMPTY],
            [WALL , GOAL , EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNone(find_path(env, 0, 2))
        
        env = [
            [EMPTY, BOX  , EMPTY],
            [BOX  , GOAL , EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNone(find_path(env, 0, 2))
        
        env = [
            [EMPTY, BOX  , EMPTY],
            [BOX  , GOAL , EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNone(find_path(env, 0, 2))
        
        env = [
            [EMPTY, BOX  , EMPTY, EMPTY],
            [BOX  , EMPTY, EMPTY, EMPTY],
            [EMPTY, BOX  , BOX  , EMPTY],
            [EMPTY, WALL , GOAL , WALL],
        ]
        self.assertIsNone(find_path(env, 2, 4))
    
    
    def test_pathing_around_obstacles(self):
        env = [
            [EMPTY, EMPTY, EMPTY],
            [WALL , WALL , EMPTY],
            [GOAL , EMPTY, EMPTY]
        ]
        
        self.assertIsNone(find_path(env, 1, 1))
        self.assertIsNone(find_path(env, 1, 2))
        self.assertIsNotNone(find_path(env, 1, 3))
        
        env = [
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, WALL , EMPTY, EMPTY],
            [GOAL , WALL , EMPTY, EMPTY],
            [EMPTY, WALL , EMPTY, EMPTY],
        ]
        
        self.assertIsNone(find_path(env, 7, 2))
        self.assertIsNotNone(find_path(env, 7, 3))
        
        env = [
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, WALL , WALL , EMPTY],
            [EMPTY, GOAL , WALL , EMPTY],
            [EMPTY, EMPTY, WALL , EMPTY],
        ]
        
        self.assertIsNone(find_path(env, 7, 3))
        self.assertIsNotNone(find_path(env, 7, 4))
    
    def test_large_move_numbers(self):
        env = [
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, WALL , EMPTY, EMPTY],
            [GOAL , WALL , EMPTY, EMPTY],
            [EMPTY, WALL , EMPTY, EMPTY],
        ]
        
        self.assertIsNotNone(find_path(env, 15, 3))
        
        env = [
            [0, WALL, 0, 0   , 0, WALL, GOAL],
            [0, WALL, 0, WALL, 0, WALL, 0],
            [0, WALL, 0, WALL, 0, WALL, 0],
            [0, WALL, 0, WALL, 0, WALL, 0],
            [0, WALL, 0, WALL, 0, WALL, 0],
            [0, WALL, 0, WALL, 0, WALL, 0],
            [0, 0   , 0, WALL, 0, 0   , 0],
        ]
        
        self.assertIsNone(find_path(env, 0, 6))
        self.assertIsNotNone(find_path(env, 0, 7))
    
    def test_wall_not_stop_pathing(self):
        env = [
            [0, WALL, 0, 0],
            [0, WALL, 0, 0],
            [0, WALL, 0, GOAL],
            [0, WALL, 0, 0],
        ]
        
        self.assertIsNotNone(find_path(env, 0, 2, wall_is_stop=False))
