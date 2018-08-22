"""
Pascal Interpreter

Check current supported language grammar in README before use
"""

import tokens
from factories import ParserFactory, InterpreterFactory
from node_visitor import NodeVisitor
from symbol_table import SymbolTableBuilder


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.GLOBAL_SCOPE = {}

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_ProcedureDeclaration(self, node):
        pass

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Condition(self, node):
        if self.visit(node.condition):
            self.visit(node.statement)
        elif node.otherwise:
            self.visit(node.otherwise)

    def visit_ForLoop(self, node):
        self.visit(node.identifier)
        var = self.GLOBAL_SCOPE[node.identifier.left.value]
        boundary = self.visit(node.boundary) + 1
        for i in range(var, boundary):
            self.GLOBAL_SCOPE[node.identifier.left.value] = i
            self.visit(node.statement)

    def visit_Writeln(self, node):
        first = self.visit(node.first)
        if first:
            print(first)
        if node.second:
            second = self.visit(node.second)
            print(second)

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_VarDecl(self, node):
        pass

    def visit_Type(self, node):
        pass

    def visit_Var(self, node):
        var_name = node.value
        value = self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            raise NameError(repr(var_name))
        return value

    def visit_RelOp(self, node):
        op_type = node.operator.type
        if op_type == tokens.NE:
            return self.visit(node.left) != self.visit(node.right)
        if op_type == tokens.EQ:
            return self.visit(node.left) == self.visit(node.right)
        if op_type == tokens.LT:
            return self.visit(node.left) < self.visit(node.right)
        if op_type == tokens.LTE:
            return self.visit(node.left) <= self.visit(node.right)
        if op_type == tokens.GT:
            return self.visit(node.left) > self.visit(node.right)
        if op_type == tokens.GTE:
            return self.visit(node.left) >= self.visit(node.right)

    def visit_BinOp(self, node):
        op_type = node.operator.type
        if op_type == tokens.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif op_type == tokens.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif op_type == tokens.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif op_type == tokens.INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif op_type == tokens.FLOAT_DIV:
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_UnaryOp(self, node):
        op_type = node.operator.type
        if op_type == tokens.PLUS:
            return +self.visit(node.expr)
        elif op_type == tokens.MINUS:
            return -self.visit(node.expr)

    def visit_Num(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Boolean(self, node):
        return node.value

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        if self.tree is None:
            return ''
        return self.visit(self.tree)


def main():
    """
    Pass file with pascal code to interpretself.
    """
    import sys
    text = open(sys.argv[1], 'r').read()

    parser = ParserFactory(text)
    tree = parser.parse()

    symtab = SymbolTableBuilder()
    symtab.build(tree)
    # Print for debugging
    print('\nSymbol table: ')
    print(symtab.symtab)

    interpreter = InterpreterFactory(tree)
    interpreter.interpret()
    # Print for debugging
    print('\nGlobal scope: ')
    print(interpreter.GLOBAL_SCOPE)


if __name__ == '__main__':
    main()
