import unittest

from path import findPath
from constants import *

class TestPath(unittest.TestCase):
    def test_already_satisfied(self):
        env = [
            [0, 1],
            [0, 2]
        ]
        self.assertIsNotNone(findPath(env, 1, 0))
        
        env = [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
        self.assertIsNotNone(findPath(env, 4, 0))
    
      
    def test_movement(self):
        env = [
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
        ]
        self.assertIsNotNone(findPath(env, 0, 1))
        
        env = [
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.assertIsNotNone(findPath(env, 0, 1))
        
        env = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 1],
        ]
        self.assertIsNotNone(findPath(env, 0, 2))
        
        env = [
            [31, 3, 0],
            [3, 7, 1],
            [1146, 3, 3],
        ]
        self.assertIsNotNone(findPath(env, 2, 1))
    
    def test_symmetry(self):
        env = [
            [GOAL , EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNotNone(findPath(env, 15, 2))
        
        env = [
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, GOAL],
        ]
        self.assertIsNotNone(findPath(env, 0, 2))
        
        env = [
            [EMPTY, EMPTY, EMPTY, GOAL],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNotNone(findPath(env, 12, 2))
        
        env = [
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY],
            [GOAL, EMPTY, EMPTY, EMPTY],
        ]
        self.assertIsNotNone(findPath(env, 3, 2))
    
    
    def test_obstacles(self):
        env = [
            [0, 0, 0],
            [2, 2, 2],
            [0, 0, 1],
        ]
        self.assertIsNone(findPath(env, 0, 2))
        
        env = [
            [0, 2, 0],
            [2, 2, 0],
            [0, 0, 1],
        ]
        self.assertIsNone(findPath(env, 0, 2))
        
        env = [
            [0, 2, 0],
            [0, 2, 0],
            [0, 2, 1],
        ]
        self.assertIsNone(findPath(env, 0, 2))
        
        env = [
            [0, 2, 0],
            [2, 1, 0],
            [0, 0, 0],
        ]
        self.assertIsNone(findPath(env, 0, 2))
        
        env = [
            [0, 3, 0],
            [3, 1, 0],
            [0, 0, 0],
        ]
        self.assertIsNone(findPath(env, 0, 2))
        
        env = [
            [0, 3, 0],
            [3, 1, 0],
            [0, 0, 0],
        ]
        self.assertIsNone(findPath(env, 0, 2))
        
        env = [
            [0, 3, 0, 0],
            [3, 0, 0, 0],
            [0, 3, 3, 0],
            [0, 2, 1, 2],
        ]
        self.assertIsNone(findPath(env, 2, 4))
    
    
    def test_pathing_around_obstacles(self):
        env = [
            [0, 0, 0],
            [2, 2, 0],
            [1, 0, 0]
        ]
        
        self.assertIsNone(findPath(env, 1, 1))
        self.assertIsNone(findPath(env, 1, 2))
        self.assertIsNotNone(findPath(env, 1, 3))
        
        env = [
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [1, 2, 0, 0],
            [0, 2, 0, 0],
        ]
        
        self.assertIsNone(findPath(env, 7, 2))
        self.assertIsNotNone(findPath(env, 7, 3))
        
        env = [
            [0, 0, 0, 0],
            [0, 2, 2, 0],
            [0, 1, 2, 0],
            [0, 0, 2, 0],
        ]
        
        self.assertIsNone(findPath(env, 7, 3))
        self.assertIsNotNone(findPath(env, 7, 4))
    
    def test_large_move_numbers(self):
        env = [
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [1, 2, 0, 0],
            [0, 2, 0, 0],
        ]
        
        self.assertIsNotNone(findPath(env, 15, 3))
        
        env = [
            [0, 2, 0, 0, 0, 2, 1],
            [0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0],
            [0, 0, 0, 2, 0, 0, 0],
        ]
        
        self.assertIsNotNone(findPath(env, 0, 20))
    
    def test_wall_not_stop_pathing(self):
        env = [
            [0, 2, 0, 0],
            [0, 2, 0, 0],
            [0, 2, 0, 1],
            [0, 2, 0, 0],
        ]
        
        self.assertIsNotNone(findPath(env, 0, 2, wall_is_stop=False))
