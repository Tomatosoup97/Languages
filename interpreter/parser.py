from tokens import *
from ast import *


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, extra=''):
        raise SyntaxError(
            'Invalid syntax on: token {type}, val {val}. {extra}'.format(
                type=self.current_token.type,
                val=self.current_token.value,
                extra=extra))

    def consume(self, token_type):
        """
        If token match with expected token,
        consume current and get next token
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error("Expected: {}".format(token_type))

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
        elif token.type == STRING:
            self.consume(STRING)
        elif token.type == BOOLEAN:
            self.consume(BOOLEAN)
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
        assignment_statement : variable ASSIGN expression
        """
        left = self.variable()
        token = self.current_token
        self.consume(ASSIGN)
        right = self.expression()
        return Assign(left, token, right)

    def expression(self):
        """
        expression : simple_expression
                   | boolean_expression
                   | string_expression
        """
        token = self.current_token
        if token.type in (TRUE, FALSE):
            return self.boolean_expression()
        elif token.type == STRING_CONST:
            return self.string_expression()
        else:
            return self.simple_expression()

    def boolean_expression(self):
        """
        boolean_expression : (TRUE | FALSE)
        """
        token = self.current_token
        if token.type == TRUE:
            self.consume(TRUE)
            return Boolean(token)

        elif token.type == FALSE:
            self.consume(FALSE)
            return Boolean(token)

    def string_expression(self):
        """
        string_expression : STRING_CONST
        """
        token = self.current_token
        if token.type == STRING_CONST:
            self.consume(STRING_CONST)
            return String(token)

    def simple_expression(self):
        """
        simple_expression : term ((PLUS | MINUS) term)*
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
               | LPAREN expression RPAREN
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
            node = self.simple_expression()
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