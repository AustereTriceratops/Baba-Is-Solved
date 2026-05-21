import unittest
from z3 import is_true, simplify

from utils import A_before_B, A_below_B, are_adjacent

class TestPath(unittest.TestCase):
    def test_A_before_B_true(self):
        self.assertTrue(simplify(A_before_B(0, 0, 1, 0, 2)))
        self.assertTrue(simplify(A_before_B(0, 0, 1, 0, 3)))
        self.assertTrue(simplify(A_before_B(0, 0, 1, 0, 5)))
        self.assertTrue(simplify(A_before_B(0, 0, 1, 0, 8)))
        
        self.assertTrue(simplify(A_before_B(1, 0, 2, 0, 5)))
        self.assertTrue(simplify(A_before_B(1, 6, 2, 6, 7)))
        self.assertTrue(simplify(A_before_B(4, 3, 5, 3, 6)))
        
    def test_A_before_B_false(self):
        self.assertFalse(simplify(A_before_B(0, 0, 0, 1, 5)))
        self.assertFalse(simplify(A_before_B(0, 0, 1, 1, 5)))
        self.assertFalse(simplify(A_before_B(1, 0, 0, 0, 5)))
        self.assertFalse(simplify(A_before_B(1, 0, 0, 1, 5)))
        self.assertFalse(simplify(A_before_B(1, 0, 1, 1, 5)))
        self.assertFalse(simplify(A_before_B(1, 0, 2, 1, 5)))
        self.assertFalse(simplify(A_before_B(1, 0, 0, 1, 5)))
        
        self.assertFalse(simplify(A_before_B(0, 0, 4, 4, 5)))
        self.assertFalse(simplify(A_before_B(0, 0, 2, 1, 5)))
        self.assertFalse(simplify(A_before_B(3, 3, 0, 1, 5)))
        self.assertFalse(simplify(A_before_B(4, 0, 1, 2, 5)))
    
    def test_A_below_B_true(self):
        self.assertTrue(simplify(A_below_B(0, 0, 0, 1, 2)))
        self.assertTrue(simplify(A_below_B(0, 0, 0, 1, 3)))
        self.assertTrue(simplify(A_below_B(0, 0, 0, 1, 5)))
        self.assertTrue(simplify(A_below_B(0, 0, 0, 1, 8)))
        
        self.assertTrue(simplify(A_below_B(0, 1, 0, 2, 5)))
        self.assertTrue(simplify(A_below_B(6, 1, 6, 2, 7)))
        self.assertTrue(simplify(A_below_B(3, 4, 3, 5, 6)))
    
    def test_A_below_B_false(self):
        self.assertFalse(simplify(A_below_B(0, 0, 1, 0, 5)))
        self.assertFalse(simplify(A_below_B(0, 0, 1, 1, 5)))
        self.assertFalse(simplify(A_below_B(1, 0, 0, 0, 5)))
        self.assertFalse(simplify(A_below_B(1, 0, 1, 0, 5)))
        self.assertFalse(simplify(A_below_B(0, 1, 1, 1, 5)))
        self.assertFalse(simplify(A_below_B(1, 0, 1, 2, 5)))
        self.assertFalse(simplify(A_below_B(1, 0, 1, 0, 5)))
        
        self.assertFalse(simplify(A_below_B(0, 0, 4, 4, 5)))
        self.assertFalse(simplify(A_below_B(0, 0, 1, 1, 5)))
        self.assertFalse(simplify(A_below_B(0, 0, 1, 2, 5)))
        self.assertFalse(simplify(A_below_B(3, 3, 1, 0, 5)))
        self.assertFalse(simplify(A_below_B(4, 0, 2, 1, 5)))
    
    def test_adjacent_true(self):
        pass
    
    def test_adjacent_false(self):
        pass