""" Pascal Interpreter """


from tests.factories import InterpreterFactory
from tokens import *
from interpreter import Parser
from lexer import Lexer


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
        interpreter = InterpreterFactory(text)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()