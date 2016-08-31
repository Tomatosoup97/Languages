#!/usr/bin/env python3
import unittest

from .factories import LexerFactory, InterpreterFactory
from lexer import Token
from tokens import *


class TestLexerReservedKeywords(unittest.TestCase):
    def test_keywords(self):
        lexer = LexerFactory('BEGIN END.')
        assert lexer.get_next_token() == Token(BEGIN, 'BEGIN')
        assert lexer.get_next_token() == Token(END, 'END')
        assert lexer.get_next_token() == Token(DOT, '.')


class LexerTestCase(unittest.TestCase):
    def test_integer(self):
        value = '123'
        lexer = LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, INTEGER)
        self.assertEqual(token.value, int(value))

    def test_MUL(self):
        value = '*'
        lexer = LexerFactory(value)
        token = lexer.get_next_token()
        self.assertEqual(token.type, MUL)
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