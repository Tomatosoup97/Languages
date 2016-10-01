from collections import OrderedDict

from node_visitor import NodeVisitor


class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def __str__(self):
        return '<{name}:{type}>'.format(name=self.name, type=self.type)

    __repr__ = __str__


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super(BuiltinTypeSymbol, self).__init__(name)

    def __str__(self):
        return self.name


class VarSymbol(Symbol):
    pass


class SymbolTable(object):
    def __init__(self):
        self._symbols = OrderedDict()
        self._init_builtins()

    def _init_builtins(self):
        BUILTINS = ('INTEGER', 'REAL', 'STRING', 'BOOLEAN')
        for builtin in BUILTINS:
            self.define(BuiltinTypeSymbol(builtin))

    def define(self, symbol):
        """Procedure that defines symbol in table
        """
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        """Return symbol with given name
        """
        symbol = self._symbols.get(name)
        return symbol

    def __str__(self):
        return 'Symbols: {symbols}'.format(
            symbols=[val for val in self._symbols.values()]
        )
