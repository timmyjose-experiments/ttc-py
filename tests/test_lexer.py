from ttc_py.lexer import *


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
