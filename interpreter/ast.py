

class AST(object):
    """Abstract Syntax Tree """
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
    `BEGIN ... END` block
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


class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Boolean(AST):
    def __init__(self, token):
        self.token = token
        self.value = bool(token.value)