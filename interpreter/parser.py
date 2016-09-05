from tokens import *


class AST(object):
    """ Abstract Syntax Tree """
    pass


class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement


class Compound(AST):
    """
    'BEGIN ... END' block
    """
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, operator, right):
        self.left = left
        self.token = self.operator = operator
        self.right = right


class VarDecl(AST):
    def __init__(self, var, var_type):
        self.var = var
        self.type = var_type


class Type(AST):
    def __init__(self, token):
        self.token = self.type = token
        self.value = token.value


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
        raise SyntaxError('Invalid syntax on: {type} token, {val} val'.format(
            type=self.current_token.type, val=self.current_token.value))

    def consume(self, token_type):
        """
        If token match with expected token,
        consume current and get next token
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        """
        program : PROGRAM variable SEMI block DOT
        """
        self.consume(PROGRAM)
        program_name = self.variable().value
        self.consume(SEMI)
        block_node = self.block()
        self.consume(DOT)
        return Program(program_name, block_node)

    def block(self):
        """ 
        block : declarations compound_statement
        """
        return Block(self.declarations(), self.compound_statement())

    def declarations(self):
        """
        declarations : VAR (variable_declaration SEMI)+ 
                     | empty
        """
        declarations = []
        if self.current_token.type == VAR:
            self.consume(VAR)
            while self.current_token.type == ID:
                declarations.extend(self.variable_declaration())
                self.consume(SEMI)
        return declarations

    def variable_declaration(self):
        """
        variable_declaration : ID (COMMA ID)* COLON type_spec
        """
        variables = [self.variable()]
        while self.current_token.type == COMMA:
            self.consume(COMMA)
            variables.append(self.variable())
        
        self.consume(COLON)
        var_type = self.type_spec()
        var_declarations = [
            VarDecl(variable, var_type)
            for variable in variables
        ]
        return var_declarations

    def type_spec(self):
        """type_spec : INTEGER
                     | REAL
        """
        token = self.current_token
        if token.type == INTEGER:
            self.consume(INTEGER)
        elif token.type == REAL:
            self.consume(REAL)
        return Type(token)

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
        term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
        """
        node = self.factor()

        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            if token.type == MUL:
                self.consume(MUL)
            if token.type == INTEGER_DIV:
                self.consume(INTEGER_DIV)
            if token.type == FLOAT_DIV:
                self.consume(FLOAT_DIV)

            node = BinOp(left=node, operator=token, right=self.factor())
        return node

    def factor(self):
        """
        factor : PLUS  factor 
               | MINUS factor
               | INTEGER_CONST
               | REAL_CONST 
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

        elif token.type == INTEGER_CONST:
            self.consume(INTEGER_CONST)
            return Num(token)

        elif token.type == REAL_CONST:
            self.consume(REAL_CONST)
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