INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=str(self.value))

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """ Lexical anaylzer (a.k.a scanner or tokenizer) """
        text = self.text
        if self.pos > len(text) -1:
            return Token(EOF, None)

        current_char = text[self.pos]
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        self.error()

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
        self.current_token = self.get_next_token()
        
        # expected left character
        left = self.current_token
        self.consume(INTEGER)

        # expected operator
        operator = self.current_token
        if operator.type == PLUS:
            self.consume(PLUS)
        elif operator.type == MINUS:
            self.consume(MINUS)

        # expected right character
        right = self.current_token
        self.consume(INTEGER)

        result = left.value + right.value
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