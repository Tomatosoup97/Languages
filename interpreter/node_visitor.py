from excepts import NoSuchVisitorException


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NoSuchVisitorException(
            'No visit_{} method'.format(type(node).__name__))
