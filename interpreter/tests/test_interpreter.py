#!/usr/bin/env python3
import unittest

from .factories import InterpreterFactory
from tokens import *


class CalculationTestCase(unittest.TestCase):
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

    def test_precedence_of_operators(self):
        interpreter = InterpreterFactory('10 + 4 / 2')
        self.assertEqual(interpreter.interpret(), 12)

        interpreter = InterpreterFactory('10 + 4 * 2')
        self.assertEqual(interpreter.interpret(), 18)

        interpreter = InterpreterFactory('4 * 2 + 10')
        self.assertEqual(interpreter.interpret(), 18)

        interpreter = InterpreterFactory('10 + 4 * 2 - 8')
        self.assertEqual(interpreter.interpret(), 10)

    def test_parenthesized_expressions(self):
        interpreter = InterpreterFactory('(10 + 4) / 2')
        self.assertEqual(interpreter.interpret(), 7)

        interpreter = InterpreterFactory('(1 + 4) * 2')
        self.assertEqual(interpreter.interpret(), 10)
        
        interpreter = InterpreterFactory('(2 + 1) * (6 - 2)')
        self.assertEqual(interpreter.interpret(), 12)

        interpreter = InterpreterFactory('1 + 3 * ((4 + 2) / 2)')
        self.assertEqual(interpreter.interpret(), 10)

        interpreter = InterpreterFactory('7+3 * (10 / (12 / (3+1) - 1))')
        self.assertEqual(interpreter.interpret(), 22)

    def test_whitespace_ommition(self):
        interpreter = InterpreterFactory('2 +   3')
        self.assertEqual(interpreter.interpret(), 5)

        interpreter = InterpreterFactory('  7 +  4 ')
        self.assertEqual(interpreter.interpret(), 11)
