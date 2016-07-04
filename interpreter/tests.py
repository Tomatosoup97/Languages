import unittest

from interpreter import Interpreter, Lexer

class LexerTestCase(unittest.TestCase):
    def LexerFactory(self, text):
        lexer = Lexer(text)
        return lexer

    def test_integer(self):
        from interpreter import INTEGER
        value = '123'
        lexer = self.LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, INTEGER)
        self.assertEqual(token.value, int(value))

    def test_multiply(self):
        from interpreter import MULTIPLY
        value = '*'
        lexer = self.LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, MULTIPLY)
        self.assertEqual(token.value, value)

    def test_division(self):
        from interpreter import DIV
        value = '/'
        lexer = self.LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, DIV)
        self.assertEqual(token.value, value)

class CalculationTestCase(unittest.TestCase):

    def InterpreterFactory(self, text):
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        return interpreter

    def test_addition(self):
        interpreter = self.InterpreterFactory('20 + 4')
        self.assertEqual(interpreter.expr(), 24)

    def test_substraction(self):
        interpreter = self.InterpreterFactory('16-6')
        self.assertEqual(interpreter.expr(), 10)

    def test_negative_substraction(self):
        interpreter = self.InterpreterFactory('6 - 16')
        self.assertEqual(interpreter.expr(), -10)

    def test_multiplication(self):
        interpreter = self.InterpreterFactory('4 * 3')
        self.assertEqual(interpreter.expr(), 12)

    def test_division(self):
        interpreter = self.InterpreterFactory('12 / 3')
        self.assertEqual(interpreter.expr(), 4)

    def test_precedence_of_operators(self):
        interpreter = self.InterpreterFactory('10 + 4 / 2')
        self.assertEqual(interpreter.expr(), 12)

        interpreter = self.InterpreterFactory('10 + 4 * 2')
        self.assertEqual(interpreter.expr(), 18)

        interpreter = self.InterpreterFactory('4 * 2 + 10')
        self.assertEqual(interpreter.expr(), 18)

        interpreter = self.InterpreterFactory('10 + 4 * 2 - 8')
        self.assertEqual(interpreter.expr(), 10)

    def test_parenthesized_expressions(self):
        interpreter = self.InterpreterFactory('(10 + 4) / 2')
        self.assertEqual(interpreter.expr(), 7)

        interpreter = self.InterpreterFactory('(1 + 4) * 2')
        self.assertEqual(interpreter.expr(), 10)
        
        interpreter = self.InterpreterFactory('(2 + 1) * (6 - 2)')
        self.assertEqual(interpreter.expr(), 12)

        interpreter = self.InterpreterFactory('1 + 3 * ((4 + 2) / 2)')
        self.assertEqual(interpreter.expr(), 10)

        interpreter = self.InterpreterFactory('7+3 * (10 / (12 / (3+1) - 1))')
        self.assertEqual(interpreter.expr(), 22)

    def test_whitespace_ommition(self):
        interpreter = self.InterpreterFactory('2 +   3')
        self.assertEqual(interpreter.expr(), 5)

        interpreter = self.InterpreterFactory('  7 +  4 ')
        self.assertEqual(interpreter.expr(), 11)

if __name__ == '__main__':
    unittest.main()