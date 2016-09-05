""" Pascal Interpreter """

from parser import Parser
from lexer import Lexer
from tokens import *


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(
                'No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        value = self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            raise NameError(repr(var_name))
        return value

    def visit_BinOp(self, node):
        op_type = node.operator.type
        if op_type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif op_type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif op_type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif op_type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_UnaryOp(self, node):
        op_type = node.operator.type
        if op_type == PLUS:
            return +self.visit(node.expr)
        elif op_type == MINUS: 
            return -self.visit(node.expr)

    def visit_NoOp(self, node):
        pass

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    import sys
    text = open(sys.argv[1], 'r').read()
    
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)


if __name__ == '__main__':
    main()