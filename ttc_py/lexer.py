import sys
from enum import Enum


class TokenType(Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211

    @staticmethod
    def check_if_keyword(spelling):
        for kind in TokenType:
            if kind.name == spelling and kind.value > 100 and kind.value < 200:
                return kind
        return None


class Token:
    def __init__(self, spelling, kind):
        self.spelling = spelling
        self.kind = kind

    def __eq__(self, other):
        return self.spelling == other.spelling and self.kind == other.kind

    def __str__(self):
        return "Token {{ spelling = {}, kind = {} }}".format(self.spelling, self.kind)


class Lexer:
    def __init__(self, input):
        self.source = input + "\n"
        self.curpos = -1
        self.curchar = ""
        self.next_char()

    def next_char(self):
        self.curpos += 1
        if self.curpos >= len(self.source):
            self.curchar = "\0"
        else:
            self.curchar = self.source[self.curpos]

    def peek(self):
        if self.curpos + 1 >= len(self.source):
            return "\0"
        else:
            return self.source[self.curpos + 1]

    def abort(self, message):
        sys.exit("Lexer error: {}".format(message))

    def skip_whitespace(self):
        while self.curchar == " " or self.curchar == "\t" or self.curchar == "\r":
            self.next_char()

    def skip_comments(self):
        if self.curchar == "#":
            while self.curchar != "\n":
                self.next_char()

    def get_token(self):
        self.skip_whitespace()
        self.skip_comments()
        token = None

        if self.curchar == "+":
            token = Token(self.curchar, TokenType.PLUS)
        elif self.curchar == "-":
            token = Token(self.curchar, TokenType.MINUS)
        elif self.curchar == "*":
            token = Token(self.curchar, TokenType.ASTERISK)
        elif self.curchar == "/":
            token = Token(self.curchar, TokenType.SLASH)
        elif self.curchar == "\n":
            token = Token(self.curchar, TokenType.NEWLINE)
        elif self.curchar == "\0":
            token = Token(self.curchar, TokenType.EOF)
        elif self.curchar == "=":
            if self.peek() == "=":
                lastchar = self.curchar
                self.next_char()
                token = Token(lastchar + self.curchar, TokenType.EQEQ)
            else:
                token = Token(self.curchar, TokenType.EQ)
        elif self.curchar == "<":
            if self.peek() == "=":
                lastchar = self.curchar
                self.next_char()
                token = Token(lastchar + self.curchar, TokenType.LTEQ)
            else:
                token = Token(self.curchar, TokenType.LT)
        elif self.curchar == ">":
            if self.peek() == "=":
                lastchar = self.curchar
                self.next_char()
                token = Token(lastchar + self.curchar, TokenType.GTEQ)
            else:
                token = Token(self.curchar, TokenType.GT)
        elif self.curchar == "!":
            if self.peek() == "=":
                lastchar = self.curchar
                self.next_char()
                token = Token(lastchar + self.curchar, TokenType.NOTEQ)
            else:
                self.abort(
                    "Expected !=, got {} which is not a valid token".format(self.peek())
                )
        elif self.curchar == '"':
            self.next_char()
            startpos = self.curpos

            while self.curchar != '"':
                if self.curchar in ["\r", "\n", "\t", "\\", "%"]:
                    self.abort("Illegal character in string: {}".format(self.curchar()))
                self.next_char()
            token = Token(self.source[startpos : self.curpos], TokenType.STRING)
        elif self.curchar.isdigit():
            startpos = self.curpos
            while self.peek().isdigit():
                self.next_char()

            if self.peek() == ".":
                self.next_char()

                if not self.peek().isdigit():
                    self.abort("Illegal character in number: {}".format(self.peek()))

                while self.peek().isdigit():
                    self.next_char()

            token = Token(self.source[startpos : self.curpos + 1], TokenType.NUMBER)

        elif self.curchar.isalpha():
            startpos = self.curpos
            while self.peek().isalnum():
                self.next_char()

            spelling = self.source[startpos : self.curpos + 1]
            keyword = TokenType.check_if_keyword(spelling)
            if keyword is None:
                token = Token(spelling, TokenType.IDENT)
            else:
                token = Token(spelling, keyword)
        else:
            self.abort("Unknown token: {}".format(self.curchar))

        self.next_char()
        return token