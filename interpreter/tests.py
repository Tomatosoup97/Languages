import unittest

from interpreter import Parser, Lexer, Interpreter
from tokens import *


class LexerTestCase(unittest.TestCase):
    def LexerFactory(self, text):
        lexer = Lexer(text)
        return lexer

    def test_integer(self):
        value = '123'
        lexer = self.LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, INTEGER)
        self.assertEqual(token.value, int(value))

    def test_multiply(self):
        value = '*'
        lexer = self.LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, MULTIPLY)
        self.assertEqual(token.value, value)

    def test_division(self):
        value = '/'
        lexer = self.LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, DIV)
        self.assertEqual(token.value, value)


class CalculationTestCase(unittest.TestCase):
    def InterpreterFactory(self, text):
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        return interpreter

    def test_addition(self):
        interpreter = self.InterpreterFactory('20 + 4')
        self.assertEqual(interpreter.interpret(), 24)
        interpreter = self.InterpreterFactory('2220 + 4')
        self.assertEqual(interpreter.interpret(), 2224)

    def test_substraction(self):
        interpreter = self.InterpreterFactory('16-6')
        self.assertEqual(interpreter.interpret(), 10)

    def test_negative_substraction(self):
        interpreter = self.InterpreterFactory('6 - 16')
        self.assertEqual(interpreter.interpret(), -10)

    def test_multiplication(self):
        interpreter = self.InterpreterFactory('4 * 3')
        self.assertEqual(interpreter.interpret(), 12)

    def test_division(self):
        interpreter = self.InterpreterFactory('12 / 3')
        self.assertEqual(interpreter.interpret(), 4)

    def test_precedence_of_operators(self):
        interpreter = self.InterpreterFactory('10 + 4 / 2')
        self.assertEqual(interpreter.interpret(), 12)

        interpreter = self.InterpreterFactory('10 + 4 * 2')
        self.assertEqual(interpreter.interpret(), 18)

        interpreter = self.InterpreterFactory('4 * 2 + 10')
        self.assertEqual(interpreter.interpret(), 18)

        interpreter = self.InterpreterFactory('10 + 4 * 2 - 8')
        self.assertEqual(interpreter.interpret(), 10)

    def test_parenthesized_expressions(self):
        interpreter = self.InterpreterFactory('(10 + 4) / 2')
        self.assertEqual(interpreter.interpret(), 7)

        interpreter = self.InterpreterFactory('(1 + 4) * 2')
        self.assertEqual(interpreter.interpret(), 10)
        
        interpreter = self.InterpreterFactory('(2 + 1) * (6 - 2)')
        self.assertEqual(interpreter.interpret(), 12)

        interpreter = self.InterpreterFactory('1 + 3 * ((4 + 2) / 2)')
        self.assertEqual(interpreter.interpret(), 10)

        interpreter = self.InterpreterFactory('7+3 * (10 / (12 / (3+1) - 1))')
        self.assertEqual(interpreter.interpret(), 22)

    def test_whitespace_ommition(self):
        interpreter = self.InterpreterFactory('2 +   3')
        self.assertEqual(interpreter.interpret(), 5)

        interpreter = self.InterpreterFactory('  7 +  4 ')
        self.assertEqual(interpreter.interpret(), 11)


if __name__ == '__main__':
    unittest.main()