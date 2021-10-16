from pathlib import Path
from ttc_py.lexer import *


def read_source_file(infile):
    return Path(infile).read_text()


def test_next_char():
    input = "LET foo = 123"
    lexer = Lexer(input)

    while lexer.peek() != "\0":
        print(lexer.curchar)
        lexer.next_char()


def test_get_token():
    input = "+- */ >>= = != <<="
    lexer = Lexer(input)

    assert lexer.get_token() == Token("+", TokenType.PLUS)
    assert lexer.get_token() == Token("-", TokenType.MINUS)
    assert lexer.get_token() == Token("*", TokenType.ASTERISK)
    assert lexer.get_token() == Token("/", TokenType.SLASH)
    assert lexer.get_token() == Token(">", TokenType.GT)
    assert lexer.get_token() == Token(">=", TokenType.GTEQ)
    assert lexer.get_token() == Token("=", TokenType.EQ)
    assert lexer.get_token() == Token("!=", TokenType.NOTEQ)
    assert lexer.get_token() == Token("<", TokenType.LT)
    assert lexer.get_token() == Token("<=", TokenType.LTEQ)
    assert lexer.get_token() == Token("\n", TokenType.NEWLINE)
    assert lexer.get_token() == Token("\0", TokenType.EOF)
    assert lexer.get_token() == Token("\0", TokenType.EOF)
    assert lexer.get_token() == Token("\0", TokenType.EOF)
    assert lexer.get_token() == Token("\0", TokenType.EOF)
    assert lexer.get_token() == Token("\0", TokenType.EOF)


def test_skip_comment():
    input = "+- # This is a comment!\n */"
    lexer = Lexer(input)

    assert lexer.get_token() == Token("+", TokenType.PLUS)
    assert lexer.get_token() == Token("-", TokenType.MINUS)
    assert lexer.get_token() == Token("\n", TokenType.NEWLINE)
    assert lexer.get_token() == Token("*", TokenType.ASTERISK)
    assert lexer.get_token() == Token("/", TokenType.SLASH)


def test_get_token_for_string():
    input = '+- "This is a string" # This is a comment!\n */'
    lexer = Lexer(input)

    assert lexer.get_token() == Token("+", TokenType.PLUS)
    assert lexer.get_token() == Token("-", TokenType.MINUS)
    assert lexer.get_token() == Token("This is a string", TokenType.STRING)
    assert lexer.get_token() == Token("\n", TokenType.NEWLINE)
    assert lexer.get_token() == Token("*", TokenType.ASTERISK)
    assert lexer.get_token() == Token("/", TokenType.SLASH)


def test_get_token_for_number():
    input = "+-123 9.8654*/"
    lexer = Lexer(input)

    assert lexer.get_token() == Token("+", TokenType.PLUS)
    assert lexer.get_token() == Token("-", TokenType.MINUS)
    assert lexer.get_token() == Token("123", TokenType.NUMBER)
    assert lexer.get_token() == Token("9.8654", TokenType.NUMBER)
    assert lexer.get_token() == Token("*", TokenType.ASTERISK)
    assert lexer.get_token() == Token("/", TokenType.SLASH)


def test_get_token_ident_and_keyword():
    input = "IF+-123 foo*THEN/"
    lexer = Lexer(input)

    assert lexer.get_token() == Token("IF", TokenType.IF)
    assert lexer.get_token() == Token("+", TokenType.PLUS)
    assert lexer.get_token() == Token("-", TokenType.MINUS)
    assert lexer.get_token() == Token("123", TokenType.NUMBER)
    assert lexer.get_token() == Token("foo", TokenType.IDENT)
    assert lexer.get_token() == Token("*", TokenType.ASTERISK)
    assert lexer.get_token() == Token("THEN", TokenType.THEN)
    assert lexer.get_token() == Token("/", TokenType.SLASH)


def test_lex_average():
    lexer = Lexer(read_source_file("samples/average.teeny"))

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.get_token()


def test_lex_factorial():
    lexer = Lexer(read_source_file("samples/factorial.teeny"))

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.get_token()


def test_lex_hello():
    lexer = Lexer(read_source_file("samples/hello.teeny"))

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.get_token()


def test_lex_statements():
    lexer = Lexer(read_source_file("samples/statements.teeny"))

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.get_token()


def test_lex_expression():
    lexer = Lexer(read_source_file("samples/expression.teeny"))

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.get_token()


def test_lex_fib():
    lexer = Lexer(read_source_file("samples/fib.teeny"))

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.get_token()


def test_lex_minmax():
    lexer = Lexer(read_source_file("samples/minmax.teeny"))

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.get_token()


def test_lex_vector():
    lexer = Lexer(read_source_file("samples/vector.teeny"))

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.get_token()
