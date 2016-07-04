import unittest
from interpreter import Interpreter, Lexer

class CalculationTestCase(unittest.TestCase):
    
    def test_addition(self):
        lexer = Lexer('20+4')
        interpreter = Interpreter(lexer)
        self.assertEqual(interpreter.expr(), 24)

    def test_substraction(self):
        lexer = Lexer('16-6')
        interpreter = Interpreter(lexer)
        self.assertEqual(interpreter.expr(), 10)

    def test_negative_substraction(self):
        lexer = Lexer('6-16')
        interpreter = Interpreter(lexer)
        self.assertEqual(interpreter.expr(), -10)

    def test_multiplication(self):
        lexer = Lexer('4*3')
        interpreter = Interpreter(lexer)
        self.assertEqual(interpreter.expr(), 12)

    def test_division(self):
        lexer = Lexer('12/3')
        interpreter = Interpreter(lexer)
        self.assertEqual(interpreter.expr(), 4)

    def test_whitespace_ommition(self):
        lexer = Lexer('2 +   3')
        interpreter = Interpreter(lexer)
        self.assertEqual(interpreter.expr(), 5)

        lexer = Lexer('  7 +  4 ')
        interpreter = Interpreter(lexer)
        self.assertEqual(interpreter.expr(), 11)

if __name__ == '__main__':
    unittest.main()