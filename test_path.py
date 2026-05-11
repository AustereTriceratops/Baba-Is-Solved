import unittest

from path import findPath

class TestPath(unittest.TestCase):
    def test_movement(self):
        env = [
            [1, 0, 0],
            [2, 0, 0],
            [0, 0, 0],
        ]
        self.assertIsNotNone(findPath(env, 1))
        
        env = [
            [1, 2, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.assertIsNotNone(findPath(env, 1))
        
        env = [
            [1, 0, 0],
            [0, 0, 0],
            [0, 0, 2],
        ]
        self.assertIsNotNone(findPath(env, 4))
    
    
    def test_obstacles(self):
        env = [
            [1, 0, 0],
            [3, 3, 3],
            [0, 0, 2],
        ]
        self.assertIsNone(findPath(env, 4))
        
        env = [
            [1, 3, 0],
            [3, 3, 0],
            [0, 0, 2],
        ]
        self.assertIsNone(findPath(env, 4))
        
        env = [
            [1, 3, 0],
            [0, 3, 0],
            [0, 3, 2],
        ]
        self.assertIsNone(findPath(env, 4))
        
        env = [
            [1, 3, 0],
            [3, 2, 0],
            [0, 0, 0],
        ]
        self.assertIsNone(findPath(env, 4))