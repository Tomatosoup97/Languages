INTEGER = 'INTEGER'
PLUS, MINUS, MULTIPLY, DIV = 'PLUS', 'MINUS', 'MULTIPLY', 'DIV'
EOF = 'EOF'

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
        Lexical anaylzer
        Breaks sentence apart into tokens
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

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
                return Token(MULTIPLY, '*')

            if self.current_char == '/':
                self.next()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def consume(self, token_type):
        """
        If token match with expected token,
        consume current and get next token
        Otherwise throw exception
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """Return token value

        factor : INTEGER
        """
        token = self.current_token
        self.consume(INTEGER)
        return token.value

    def expr(self):
        """
        Parser / Interpreter
        """
        result = self.factor()

        while self.current_token.type in (PLUS, MINUS, MULTIPLY, DIV):
            operator = self.current_token
            if operator.type == PLUS:
                self.consume(PLUS)
                result += self.factor()
            elif operator.type == MINUS:
                self.consume(MINUS)
                result -= self.factor()
            elif operator.type == MULTIPLY:
                self.consume(MULTIPLY)
                result *= self.factor()
            elif operator.type == DIV:
                self.consume(DIV)
                result //= self.factor()

        return result

def main():
    while True:
        try:
            text = input('>>> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()