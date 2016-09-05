from tokens import *


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
    'BEGIN': Token('BEGIN', 'BEGIN'),
    'END': Token('END', 'END'),
}


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position]

    def error(self):
        raise Exception('Error parsing input')

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
        peek_pos = self.position + 1
        if peek_pos > len(self.text) -1:
            return None
        return self.text[peek_pos]

    def _id(self):
        """ Handle identifiers and reserved keywords """
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.next()
        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def skip_whitespace(self):
        while self.current_char is not None and \
                 self.current_char.isspace():
            self.next()

    def integer(self):
        """ 
        Return integer from the input
        """
        result = ''
        while self.current_char is not None and \
                self.current_char.isdigit():
            result += self.current_char
            self.next()
        return int(result)

    def get_next_token(self):
        """ 
        Lexical anaylzer (tokenizer)
        Breaks sentence apart into tokens
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char is ':' and self.peek() == '=':
                self.next(); self.next()
                return Token(ASSIGN, ':=')

            if self.current_char is ';':
                self.next()
                return Token(SEMI, ';')

            if self.current_char is '.':
                self.next()
                return Token(DOT, '.')

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

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
                return Token(DIV, '/')

            if self.current_char == '(':
                self.next()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.next()
                return Token(RPAREN, ')')

            self.error()
        return Token(EOF, None)