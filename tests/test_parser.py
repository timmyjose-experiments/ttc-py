from pathlib import Path
from ttc_py.lexer import *
from ttc_py.parser import *


def read_source_file(infile):
    return Path(infile).read_text()


def parse_file(infile):
    emitter = Emitter("dummy.c")
    parser = Parser(Lexer(read_source_file(infile)), emitter)
    parser.parse()


def test_parse_hello():
    parse_file("samples/hello.teeny")


def test_statements():
    parse_file("samples/statements.teeny")


def test_expressions():
    parse_file("samples/expression.teeny")


def test_parse_average():
    parse_file("samples/average.teeny")


def test_parse_factorial():
    parse_file("samples/factorial.teeny")


def test_parse_fib():
    parse_file("samples/fib.teeny")


def test_parse_minmax():
    parse_file("samples/minmax.teeny")


def test_parse_vector():
    parse_file("samples/vector.teeny")
