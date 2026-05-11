import unittest

from path import findPath

class TestPath(unittest.TestCase):
    def test_already_satisfied(self):
        env = [
            [0, 2],
            [0, 1]
        ]
        self.assertIsNotNone(findPath(env, 1, 0))
        
        env = [
            [0, 0, 0],
            [0, 2, 0],
            [0, 0, 0]
        ]
        self.assertIsNotNone(findPath(env, 4, 0))
    
      
    def test_movement(self):
        env = [
            [0, 0, 0],
            [2, 0, 0],
            [0, 0, 0],
        ]
        self.assertIsNotNone(findPath(env, 0, 1))
        
        env = [
            [0, 2, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.assertIsNotNone(findPath(env, 0, 1))
        
        env = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 2],
        ]
        self.assertIsNotNone(findPath(env, 0, 4))
    
    
    def test_obstacles(self):
        env = [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 2],
        ]
        self.assertIsNone(findPath(env, 0, 4))
        
        env = [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 2],
        ]
        self.assertIsNone(findPath(env, 0, 4))
        
        env = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 2],
        ]
        self.assertIsNone(findPath(env, 0, 4))
        
        env = [
            [0, 1, 0],
            [1, 2, 0],
            [0, 0, 0],
        ]
        self.assertIsNone(findPath(env, 0, 4))
    
    
    def test_pathing_around_obstacles(self):
        env = [
            [0, 0, 0],
            [1, 1, 0],
            [2, 0, 0]
        ]
        
        self.assertIsNone(findPath(env, 1, 1))
        self.assertIsNone(findPath(env, 1, 2))
        self.assertIsNone(findPath(env, 1, 3))
        self.assertIsNone(findPath(env, 1, 4))
        self.assertIsNotNone(findPath(env, 1, 5))
        
        env = [
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [2, 1, 0, 0],
            [0, 1, 0, 0],
        ]
        
        self.assertIsNone(findPath(env, 7, 5))
        self.assertIsNotNone(findPath(env, 7, 6))
