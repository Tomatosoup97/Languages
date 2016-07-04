import unittest
from interpreter import Interpreter

class CalculationTestCase(unittest.TestCase):
    
    def test_addition(self):
        interpreter = Interpreter('2+4')
        self.assertEqual(interpreter.expr(), 6)

    def test_substraction(self):
        interpreter = Interpreter('6-2')
        self.assertEqual(interpreter.expr(), 4)

    def test_multiplication(self):
        interpreter = Interpreter('4*3')
        self.assertEqual(interpreter.expr(), 12)

    def test_division(self):
        interpreter = Interpreter('12/3')
        self.assertEqual(interpreter.expr(), 4)

    def test_whitespace_ommition(self):
        interpreter = Interpreter('2 +   3')
        self.assertEqual(interpreter.expr(), 5)

if __name__ == '__main__':
    unittest.main()