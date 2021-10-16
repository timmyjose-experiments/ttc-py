import sys
from ttc_py.lexer import *


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curtoken = None
        self.peektoken = None
        self.symbols = set()
        self.declared_labels = set()
        self.gotoed_labels = set()
        self.next_token()  # peektoken is set
        self.next_token()  # curtoken is set

    def check_token(self, kind):
        """Return true if the passed-in token kind matches the current token's kind"""
        return kind == self.curtoken.kind

    def check_peek(self, kind):
        """Returns true if passed-in token kind matches the next token's kind"""
        return kind == self.peektoken.kind

    def match(self, kind):
        """Try to match the current token. If not match, error. Advances the current token"""
        if not self.check_token(kind):
            self.abort("Expected {}, but found {}".format(kind, self.curtoken.kind))
        self.next_token()

    def next_token(self):
        """Advances the current token"""
        self.curtoken = self.peektoken
        self.peektoken = self.lexer.get_token()

    def abort(self, message):
        """exit the parser with an error message"""
        sys.exit("Parser error: {}".format(message))

    ## production rules

    def program(self):
        """program ::= { statement }"""
        print("PROGRAM")

        while self.check_token(TokenType.NEWLINE):
            self.match(TokenType.NEWLINE)

        while not self.check_token(TokenType.EOF):
            self.statement()

        # basic typechecking - ensure that all the labels that
        # have been GOTOed are valid labels
        for label in self.gotoed_labels:
            if label not in self.declared_labels:
                self.abort("Attempting to GOTO to an undeclared label {}".format(label))

    def statement(self):
        """
        statement ::= "PRINT" (expression | string) NL
                    | "IF" comparison "THEN" NL {  statement } "ENDIF" NL
                    | "WHILE" comparison "REPEAT" NL { statement } "ENDWHILE" NL
                    | "LABEL" ident NL
                    | "GOTO" ident NL
                    | "LET" ident "=" expression NL
                    | "INPUT" ident NL
        """
        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.match(TokenType.PRINT)

            if self.check_token(TokenType.STRING):
                self.match(TokenType.STRING)
            else:
                self.expression()
        elif self.check_token(TokenType.IF):
            print("STATEMENT-IF")

            self.match(TokenType.IF)
            self.comparison()
            self.match(TokenType.THEN)
            self.nl()

            while not self.check_token(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.match(TokenType.WHILE)
            self.comparison()
            self.match(TokenType.REPEAT)
            self.nl()

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.match(TokenType.LABEL)

            if self.curtoken.spelling in self.declared_labels:
                self.abort("Label {} already exists".format(self.curtoken.spelling))

            self.declared_labels.add(self.curtoken.spelling)
            self.match(TokenType.IDENT)
        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.match(TokenType.GOTO)
            self.gotoed_labels.add(self.curtoken.spelling)
            self.match(TokenType.IDENT)
        elif self.check_token(TokenType.LET):
            print("STATEMENT-LET")
            self.match(TokenType.LET)

            if self.curtoken.spelling not in self.symbols:
                self.symbols.add(self.curtoken.spelling)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
        elif self.check_token(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.match(TokenType.INPUT)

            if self.curtoken.spelling not in self.symbols:
                self.symbols.add(self.curtoken.spelling)

            self.match(TokenType.IDENT)
        else:
            self.abort("{} does not start a valid statement".format(self.curtoken))

        self.nl()

    def comparison(self):
        """
        comparison ::= expression (("==" | "!=" | "<" | "<=" | ">" | ">=") expression)+
        """
        print("COMPARISON")
        self.expression()

        if self.is_comparison_operator():
            self.next_token()
            self.expression()
        else:
            self.abort(
                "Expected comparison operator, but found {}".format(self.curtoken)
            )

        while self.is_comparison_operator():
            self.next_token()
            self.expression()

    def is_comparison_operator(self):
        return (
            self.check_token(TokenType.EQEQ)
            or self.check_token(TokenType.NOTEQ)
            or self.check_token(TokenType.LT)
            or self.check_token(TokenType.LTEQ)
            or self.check_token(TokenType.GT)
            or self.check_token(TokenType.GTEQ)
        )

    def expression(self):
        """expression ::= term { ("-" | "+") term }"""
        print("EXPRESSION")

        self.term()
        while self.check_token(TokenType.MINUS) or self.check_token(TokenType.PLUS):
            self.next_token()
            self.term()

    def term(self):
        """term ::= unary { ("*" | "/") unary }"""
        print("TERM")

        self.unary()
        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH):
            self.next_token()
            self.unary()

    def unary(self):
        """unary ::= ["+" | "-"] primary"""
        print("UNARY")

        if self.check_token(TokenType.MINUS) or self.check_token(TokenType.PLUS):
            self.next_token()
            self.primary()
        else:
            self.primary()

    def primary(self):
        """primary ::= number | ident"""
        print("PRIMARY {}".format(self.curtoken.spelling))

        if self.check_token(TokenType.NUMBER):
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            if self.curtoken.spelling not in self.symbols:
                self.abort(
                    "Referencing a non-existent variable {}".format(
                        self.curtoken.spelling
                    )
                )
            self.next_token()
        else:
            self.abort(
                "Expected a number or an ident, but found {}".format(self.curtoken)
            )

    def nl(self):
        """NL ::= "\n"+"""
        print("NEWLINE")

        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.match(TokenType.NEWLINE)

    # public API

    def parse(self):
        """parse the source file - starting rule is `program`"""
        self.program()
