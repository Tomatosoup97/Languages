#!/usr/bin/env python3
from parser import Parser
from lexer import Lexer
from interpreter import Interpreter


def LexerFactory(value):
    return Lexer(value)


def ParserFactory(text):
    lexer = Lexer(text)
    return Parser(lexer)


def InterpreterFactory(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    return Interpreter(parser)
