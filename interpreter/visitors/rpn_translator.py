from ..interpreter import NodeVisitor
from ..lexer import Lexer
from ..parser import Parser


class RPNTranslator(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return "{left} {right} {operator}".format(
            left=left,
            right=right,
            operator=node.operator.type
        )

    def visit_num(self, node):
        return node.value

    def translate(self):
        return self.visit(self.tree)


def rpn(text):
    lexer = Lexer(text)
    parser = Parser(text)
    tree = parser.parse()
    rpn_translator = RPNTranslator(tree)
    translation = rpn_translator.translate()
    return translation