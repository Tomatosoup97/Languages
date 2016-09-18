import unittest

from tokens import *
from .factories import InterpreterFactory


class InterpreterTestCase(unittest.TestCase):
    def test_integer_arithmetic_exprs(self):
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
            self.assertEqual(globals['A'], result)

    def test_float_arithmetic_exprs(self):
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
            self.assertEqual(globals['A'], result)

    def test_expr_invalid_syntax_bin_op(self):
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

    def test_expr_invalid_syntax_no_bin_op(self):
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

    def test_numbers(self):
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
            'NUMBER': 2, 'A': 2, 'B': 25, 'C': 27, 'X': 11, 'Y': 5.0/2
        }
        assert globals == expected

    def test_string_and_bool(self):
        text = """\
            PROGRAM testing;
            VAR
               bool       : BOOLEAN;
               str        : STRING;
            BEGIN
               BEGIN
                  bool := True;
                  str := 'abc';
               END;
               str := 'xyz';
            END.
        """
        interpreter = InterpreterFactory(text)
        interpreter.interpret()

        globals = interpreter.GLOBAL_SCOPE
        expected = {
            'STR': 'xyz', 'BOOL': True,
        }
        assert globals == expected

    def test_rel_op(self):
        text = """\
            PROGRAM testing;
            VAR
               bool       : BOOLEAN;
               another    : BOOLEAN;
               helper     : INTEGER;
            BEGIN
                BEGIN
                    bool := 6 < 3 * 3;
                END;
                another := 12 / 2 <= 4;
            END.
        """
        interpreter = InterpreterFactory(text)
        interpreter.interpret()

        globals = interpreter.GLOBAL_SCOPE
        expected = {'BOOL': True, 'ANOTHER': False}
        assert globals == expected

    def test_conditional_statement(self):
        text = """\
            PROGRAM testing;
            VAR
               bool       : BOOLEAN;
               a          : INTEGER;
               b          : STRING;
            BEGIN
                BEGIN
                    bool := 6 < 10;
                    if bool then
                      a := 5
                    else
                      a := 10
                END;
                if 2 <> 2 then
                  b := 'two isnt two'
                else
                  b := 'two is two'
            END.
        """
        interpreter = InterpreterFactory(text)
        interpreter.interpret()

        globals = interpreter.GLOBAL_SCOPE
        expected = {'B': 'two is two', 'A': 5, 'BOOL': True}
        assert globals == expected

    def test_forloop_statement(self):
        text = """\
            PROGRAM testing;
            VAR
               a          : INTEGER;
            BEGIN
                a := 5;
                for i := 1 to a do 
                BEGIN
                  i := i * 10
                END;
            END.
        """
        interpreter = InterpreterFactory(text)
        interpreter.interpret()

        globals = interpreter.GLOBAL_SCOPE
        expected = {'A': 5, 'I': 50}
        assert globals == expected


if __name__ == '__main__':
    unittest.main()