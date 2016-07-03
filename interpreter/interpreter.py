INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

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

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_token = None
        self.current_char = self.text[self.position]

    def error(self):
        raise Exception('Error parsing input')

    def next(self):
        """ Set pointer to next character """
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
        """ Return integer from the input """
        result = ''
        while self.current_char is not None and \
                self.current_char.isdigit():
            result += self.current_char
            self.next()
        return int(result)

    def get_next_token(self):
        """ Lexical anaylzer (tokenizer) """
        while self.current_char is not None:
            self.skip_whitespace()

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.next()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.next()
                return Token(MINUS, '-')

            self.error()

        return Token(EOF, None)

    def consume(self, token_type):
        """
        If token match with expected token,
        consume current and get next token
        Otherwise thorw exception
        """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """ Parser """
        self.current_token = self.get_next_token()
        
        # expected left character
        left = self.current_token
        self.consume(INTEGER)

        # operator
        operator = self.current_token
        if operator.type == PLUS:
            self.consume(PLUS)
        elif operator.type == MINUS:
            self.consume(MINUS)

        # expected right character
        right = self.current_token
        self.consume(INTEGER)

        if operator.type == PLUS:
            result = left.value + right.value
        elif operator.type == MINUS:
            result  = left.value - right.value
        return result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()