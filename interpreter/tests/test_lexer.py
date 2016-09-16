#!/usr/bin/env python3
import unittest

from .factories import LexerFactory
from tokens import *


class LexerTestCase(unittest.TestCase):
    def test_tokens(self):
        records = (
            ('234', INTEGER_CONST, 234),
            ('3.14', REAL_CONST, 3.14),
            ('*', MUL, '*'),
            ('DIV', INTEGER_DIV, 'DIV'),
            ('/', FLOAT_DIV, '/'),
            ('+', PLUS, '+'),
            ('-', MINUS, '-'),
            ('(', LPAREN, '('),
            (')', RPAREN, ')'),
            (':=', ASSIGN, ':='),
            ('.', DOT, '.'),
            ('NUMBER', ID, 'NUMBER'),
            (';', SEMI, ';'),
            ("'abc'", STRING_CONST, 'abc'),
            ('BEGIN', BEGIN, 'BEGIN'),
            ('END', END, 'END'),
            ('>', GT, '>'),
            ('<', LT, '<'),
            ('<=', LTE, '<='),
            ('>=', GTE, '>='),
            ('=', EQ, '='),
            ('<>', NE, '<>'),
            ('END', END, 'END'),
            ('IF', IF, 'IF'),
            ('THEN', THEN, 'THEN'),
        )
        for text, tok_type, tok_val in records:
            lexer = LexerFactory(text)
            token = lexer.get_next_token()
            self.assertEqual(token.type, tok_type)
            self.assertEqual(token.value, tok_val)