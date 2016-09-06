import unittest

from tokens import *
from .factories import InterpreterFactory


class InterpreterTestCase(unittest.TestCase):
    def test_integer_arithmetic_expressions(self):
        for expr, result in (
            ('3', 3),
            ('2 + 7 * 4', 30),
            ('7 - 8 DIV 4', 5),
            ('14 + 2 * 3 - 6 DIV 2', 17),
            ('7 + 3 * (10 DIV (12 DIV (3 + 1) - 1))', 22),
            ('7 + 3 * (10 DIV (12 DIV (3 + 1) - 1)) DIV (2 + 3) - 5 - 3 + (8)', 10),
            ('7 + (((3 + 2)))', 12),
            ('- 3', -3),
            ('+ 3', 3),
            ('5 - - - + - 3', 8),
            ('5 - - - + - (3 + 4) - +2', 10),
        ):
            interpreter = InterpreterFactory(
                """PROGRAM Test;
                   VAR
                       a : INTEGER;
                   BEGIN
                       a := {}
                   END.
                """.format(expr)
            )
            interpreter.interpret()
            globals = interpreter.GLOBAL_SCOPE
            self.assertEqual(globals['a'], result)

    def test_float_arithmetic_expressions(self):
        for expr, result in (
            ('3.14', 3.14),
            ('2.14 + 7 * 4', 30.14),
            ('7.14 - 8 / 4', 5.14),
        ):
            interpreter = InterpreterFactory(
                """PROGRAM Test;
                   VAR
                       a : REAL;
                   BEGIN
                       a := {}
                   END.
                """.format(expr)
            )
            interpreter.interpret()
            globals = interpreter.GLOBAL_SCOPE
            self.assertEqual(globals['a'], result)

    def test_expression_invalid_syntax_01(self):
        interpreter = InterpreterFactory(
            """
            PROGRAM Test;
            BEGIN
               a := 10 * ;  {Invalid syntax}
            END.
            """
        )
        with self.assertRaises(Exception):
            interpreter.interpret()

    def test_expression_invalid_syntax_02(self):
        interpreter = InterpreterFactory(
            """
            PROGRAM Test;
            BEGIN
               a := 1 (1 + 2); {Invalid syntax}
            END.
            """
        )
        with self.assertRaises(Exception):
            interpreter.interpret()

    def test_program(self):
        text = """\
            PROGRAM testing;
            VAR
               number     : INTEGER;
               a, b, c, x : INTEGER;
               y          : REAL;
            BEGIN
               BEGIN
                  number := 2;
                  a := number;
                  b := 10 * a + 10 * number DIV 4;
                  c := a - -b
               END;
               x := 11;
               y := 5 / 2;
            END.
        """
        interpreter = InterpreterFactory(text)
        interpreter.interpret()

        globals = interpreter.GLOBAL_SCOPE
        expected = {
            'number': 2, 'a': 2, 'b': 25, 'c': 27, 'x': 11, 'y': 5/2
        }
        assert globals == expected


if __name__ == '__main__':
    unittest.main()