#!/usr/bin/env python3
import unittest

from .factories import LexerFactory, InterpreterFactory
from tokens import *


class LexerTestCase(unittest.TestCase):
    def test_integer(self):
        value = '123'
        lexer = LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, INTEGER)
        self.assertEqual(token.value, int(value))

    def test_multiply(self):
        value = '*'
        lexer = LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, MULTIPLY)
        self.assertEqual(token.value, value)

    def test_division(self):
        value = '/'
        lexer = LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, DIV)
        self.assertEqual(token.value, value)

    def test_whitespace_ommition(self):
        interpreter = InterpreterFactory('2 +   3')
        self.assertEqual(interpreter.interpret(), 5)

        interpreter = InterpreterFactory('  7 +  4 ')
        self.assertEqual(interpreter.interpret(), 11)