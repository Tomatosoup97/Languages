""" Pascal Interpreter """

#-----------------------------------------------------------------------------
# 
#  LEXER
#
#-----------------------------------------------------------------------------

# Token types
#
INTEGER, LPAREN, RPAREN, EOF = (
    'INTEGER',  '(', ')', 'EOF',
)
PLUS, MINUS, MULTIPLY, DIV, = (
    'PLUS', 'MINUS', 'MULTIPLY', 'DIV',
)


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

            if self.current_char == '(':
                self.next()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.next()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)


#-----------------------------------------------------------------------------
# 
#  PARSER
#
#-----------------------------------------------------------------------------

class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.token = self.operator = operator
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
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
        """
        factor : INTEGER | LPAREN expr RPAREN
        """
        token = self.current_token
        if token.type == INTEGER:
            self.consume(INTEGER)
            return Num(token)

        elif token.type == LPAREN:
            self.consume(LPAREN)
            node = self.expr()
            self.consume(RPAREN)
            return node

    def term(self):
        """
        term : factor ((MULTIPLY | DIV) factor)*
        """
        node = self.factor()

        while self.current_token.type in (MULTIPLY, DIV):
            token = self.current_token
            if token.type == MULTIPLY:
                self.consume(MULTIPLY)
            if token.type == DIV:
                self.consume(DIV)

            node = BinOp(left=node, operator=token, right=self.factor())
        return node

    def expr(self):
        """
        Parser / Interpreter

        expr     : term ((PLUS | MINUS) term)*
        term    : factor ((MULTIPLY | DIV) factor)*
        factor  : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.consume(PLUS)
            elif token.type == MINUS:
                self.consume(MINUS)

            node = BinOp(left=node, operator=token, right=self.term())
        return node

    def parse(self):
        return self.expr()


#-----------------------------------------------------------------------------
# 
#  INTERPRETER
#
#-----------------------------------------------------------------------------

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        op_type = node.operator.type
        if op_type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif op_type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif op_type == MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif op_type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    while True:
        try:
            text = input('>>> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)

if __name__ == '__main__':
    main()