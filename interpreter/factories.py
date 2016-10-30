from parser import Parser
from lexer import Lexer
from interpreter import Interpreter


class ParserFactory(object):
    def __call__(self, text):
        lexer = Lexer(text)
        parser = Parser(lexer)
        return parser


class InterpreterFactory(object):
    def __call__(self, data, istree=True):
        """Create interpreter instance.

        :param data: string input text or parsed AST tree
        :param istree: boolean if data is tree or text
        """
        if istree:
            tree = data
        else:
            parser = ParserFactory(data)
            tree = parser.parse()
        interpreter = Interpreter(tree)
        return interpreter
