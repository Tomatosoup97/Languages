from tokens import *


class AST(object):
    """ Abstract Syntax Tree """
    pass


class Compound(AST):
    """ 'BEGIN ... END' block """
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.token = self.operator = operator
        self.right = right


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class BinOp(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.token = self.operator = operator
        self.right = right


class UnaryOp(AST):
    def __init__(self, operator, expr):
        self.token = self.operator = operator
        self.expr = expr


class NoOp(AST):
    pass


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise SyntaxError('Invalid syntax')

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

    def program(self):
        """
        program : compound_statement DOT
        """
        node = self.compound_statement()
        self.consume(DOT)
        return node

    def compound_statement(self):
        """
        compound_statement : BEGIN statement_list END
        """
        self.consume(BEGIN)
        nodes = self.statement_list()
        self.consume(END)
        root = Compound()

        for node in nodes:
            root.children.append(node)
        return root

    def statement_list(self):
        """
        statement_list : statement
                       | statement SEMI statement_list
        """
        node = self.statement()
        results = [node]
        while self.current_token.type == SEMI:
            self.consume(SEMI)
            results.append(self.statement())
        return results

    def statement(self):
        """
        statement : compound_statement
                  | assignment_statement
                  | empty
        """
        if self.current_token.type == BEGIN:
            return self.compound_statement()
        elif self.current_token.type == ID:
            return self.assignment_statement()
        else:
            return self.empty()

    def empty(self):
        """
        empty :
        """
        return NoOp()

    def assignment_statement(self):
        """ 
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.consume(ASSIGN)
        right = self.expr()
        return Assign(left, token, right)

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
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

    def term(self):
        """
        term : factor ((MUL | DIV) factor)*
        """
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.consume(MUL)
            if token.type == DIV:
                self.consume(DIV)
            node = BinOp(left=node, operator=token, right=self.factor())
        return node

    def factor(self):
        """
        factor : PLUS  factor 
               | MINUS factor
               | INTEGER 
               | LPAREN expr RPAREN
               | variable
        """
        token = self.current_token
        if token.type == PLUS:
            self.consume(PLUS)
            return UnaryOp(token, self.factor())

        elif token.type == MINUS:
            self.consume(MINUS)
            return UnaryOp(token, self.factor())

        elif token.type == INTEGER:
            self.consume(INTEGER)
            return Num(token)

        elif token.type == LPAREN:
            self.consume(LPAREN)
            node = self.expr()
            self.consume(RPAREN)
            return node
        else:
            return self.variable()

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.consume(ID)
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()
        return node