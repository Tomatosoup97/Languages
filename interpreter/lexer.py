import re

from tokens import *
from exceptions import LexerException


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value))

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'PROGRAM': Token('PROGRAM', 'PROGRAM'),
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
    'DIV': Token('INTEGER_DIV', 'DIV'),
    'VAR': Token('VAR', 'VAR'),
    'INTEGER': Token('INTEGER', 'INTEGER'),
    'REAL': Token('REAL', 'REAL'),
}


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position]

    def error(self):
        raise LexerException(
            """Error tokenizing input on character: {} and {} position
            """.format(self.current_char, self.position)
        )

    def next(self):
        """
        Set pointer to next character 
        """
        self.position += 1
        if self.position > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.position]

    def peek(self):
        """
        Check what next char will be without advancing position
        """
        peek_pos = self.position + 1
        if peek_pos > len(self.text) -1:
            return None
        return self.text[peek_pos]

    def _id(self):
        """
        Handle identifiers and reserved keywords
        """
        result = ''
        while self.current_char is not None and \
                re.match('\w', self.current_char):
            result += self.current_char
            self.next()
        result = result.upper()
        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next()

    def skip_comment(self):
        self.next() # the opening curly brace
        while self.current_char != '}':
            self.next()
        self.next() # the closing curly brace

    def integer(self):
        result = ''
        while self.current_char is not None and \
                self.current_char.isdigit():
            result += self.current_char
            self.next()
        return int(result)

    def number(self):
        result = str(self.integer())
        if self.current_char == '.':
            self.next()
            result += '.' + str(self.integer())
            return Token(REAL_CONST, float(result))
        else:
            return Token(INTEGER_CONST, int(result))

    def get_next_token(self):
        """ 
        Lexical anaylzer (tokenizer)
        Breaks sentence apart into tokens
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char is '{':
                self.skip_comment()
                continue

            if re.match('[_a-zA-Z]', self.current_char):
                return self._id()

            if self.current_char is ':' and self.peek() == '=':
                self.next(); self.next()
                return Token(ASSIGN, ':=')

            if self.current_char is ';':
                self.next()
                return Token(SEMI, ';')

            if self.current_char is ':':
                self.next()
                return Token(COLON, ':')

            if self.current_char is '.':
                self.next()
                return Token(DOT, '.')

            if self.current_char is ',':
                self.next()
                return Token(COMMA, ',')

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '+':
                self.next()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.next()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.next()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.next()
                return Token(FLOAT_DIV, '/')

            if self.current_char == '(':
                self.next()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.next()
                return Token(RPAREN, ')')

            self.error()
        return Token(EOF, None)