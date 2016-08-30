#!/usr/bin/env python3
import unittest

from .factories import InterpreterFactory
from tokens import *


class TestUnaryOperator(unittest.TestCase):
    def test_basic(self):
        interpreter = InterpreterFactory('5 -- 2')
        self.assertEqual(interpreter.interpret(), 7)
        interpreter = InterpreterFactory('5 +- 2')
        self.assertEqual(interpreter.interpret(), 3)

    def test_complex(self):
        interpreter = InterpreterFactory('5 -+--+- 2')
        self.assertEqual(interpreter.interpret(), 7)

    def test_in_the_middle(self):
        interpreter = InterpreterFactory('2 + 5 -- 2 ++ 3')
        self.assertEqual(interpreter.interpret(), 12)


class TestCalculations(unittest.TestCase):
    def test_addition(self):
        interpreter = InterpreterFactory('20 + 4')
        self.assertEqual(interpreter.interpret(), 24)
        interpreter = InterpreterFactory('2220 + 4')
        self.assertEqual(interpreter.interpret(), 2224)

    def test_substraction(self):
        interpreter = InterpreterFactory('16-6')
        self.assertEqual(interpreter.interpret(), 10)

    def test_negative_substraction(self):
        interpreter = InterpreterFactory('6 - 16')
        self.assertEqual(interpreter.interpret(), -10)

    def test_multiplication(self):
        interpreter = InterpreterFactory('4 * 3')
        self.assertEqual(interpreter.interpret(), 12)

    def test_division(self):
        interpreter = InterpreterFactory('12 / 3')
        self.assertEqual(interpreter.interpret(), 4)


class TestPrecedenceOfOperators(unittest.TestCase):
    def test_last(self):
        interpreter = InterpreterFactory('10 + 4 / 2')
        self.assertEqual(interpreter.interpret(), 12)
        interpreter = InterpreterFactory('10 + 4 * 2')
        self.assertEqual(interpreter.interpret(), 18)

    def test_first(self):
        interpreter = InterpreterFactory('4 * 2 + 10')
        self.assertEqual(interpreter.interpret(), 18)

    def test_middle(self):
        interpreter = InterpreterFactory('10 + 4 * 2 - 8')
        self.assertEqual(interpreter.interpret(), 10)


class TestParenthesizedExpressions(unittest.TestCase):
    def test_basic(self):
        interpreter = InterpreterFactory('(10 + 4) / 2')
        self.assertEqual(interpreter.interpret(), 7)

        interpreter = InterpreterFactory('(1 + 4) * 2')
        self.assertEqual(interpreter.interpret(), 10)

    def test_two_parenthesis(self):
        interpreter = InterpreterFactory('(2 + 1) * (6 - 2)')
        self.assertEqual(interpreter.interpret(), 12)

    def test_nested_parenthesis(self):
        interpreter = InterpreterFactory('1 + 3 * ((4 + 2) / 2)')
        self.assertEqual(interpreter.interpret(), 10)

    def test_complex_expression(self):
        interpreter = InterpreterFactory('7+3 * (10 / (12 / (3+1) - 1))')
        self.assertEqual(interpreter.interpret(), 22)
