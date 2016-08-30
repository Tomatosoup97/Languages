from ..interpreter import NodeVisitor
from ..lexer import Lexer
from ..parser import Parser


class LispNotationTranslator(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return "({operator} {left} {right})".format(
            left=left,
            right=right,
            operator=node.operator.type
        )

    def visit_num(self, node):
        return node.value

    def translate(self):
        return self.visit(self.tree)


def lisp_notation(text):
    lexer = Lexer(text)
    parser = Parser(text)
    tree = parser.parse()
    translator = LispNotationTranslator(tree)
    translation = translator.translate()
    return translation