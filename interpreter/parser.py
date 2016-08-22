from tokens import *


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
        factor: INTEGER | LPAREN expr RPAREN
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
        term: factor ((MULTIPLY | DIV) factor)*
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
        Parser

        expr    : term ((PLUS | MINUS) term)*
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