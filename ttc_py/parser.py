import sys
from ttc_py.lexer import *
from ttc_py.emitter import *


class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter
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
        self.emitter.header_line("#include <stdio.h>")
        self.emitter.header_line("int main(int argc, char *argv[])")
        self.emitter.header_line("{")

        while self.check_token(TokenType.NEWLINE):
            self.match(TokenType.NEWLINE)

        while not self.check_token(TokenType.EOF):
            self.statement()

        self.emitter.emit_line("return 0;")
        self.emitter.emit_line("}")

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
            self.match(TokenType.PRINT)

            if self.check_token(TokenType.STRING):
                self.emitter.emit_line(
                    'printf("%s\\n", "{}");'.format(self.curtoken.spelling)
                )
                self.match(TokenType.STRING)
            else:
                self.emitter.emit('printf("%.2f\\n", (float)(')
                self.expression()
                self.emitter.emit_line("));")
        elif self.check_token(TokenType.IF):
            self.match(TokenType.IF)
            self.emitter.emit("if(")
            self.comparison()
            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emit(") {")

            while not self.check_token(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
            self.emitter.emit_line("}")
        elif self.check_token(TokenType.WHILE):
            self.match(TokenType.WHILE)
            self.emitter.emit("while (")
            self.comparison()
            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emit_line(") {")

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emit_line("}")
        elif self.check_token(TokenType.LABEL):
            self.match(TokenType.LABEL)

            if self.curtoken.spelling in self.declared_labels:
                self.abort("Label {} already exists".format(self.curtoken.spelling))

            self.declared_labels.add(self.curtoken.spelling)
            self.emitter.emit_line("{}:".format(self.curtoken.spelling))
            self.match(TokenType.IDENT)
        elif self.check_token(TokenType.GOTO):
            self.match(TokenType.GOTO)
            self.gotoed_labels.add(self.curtoken.spelling)
            self.emitter.emit_line("goto {};".format(self.curtoken.spelling))
            self.match(TokenType.IDENT)
        elif self.check_token(TokenType.LET):
            self.match(TokenType.LET)

            if self.curtoken.spelling not in self.symbols:
                self.emitter.header_line("float {};".format(self.curtoken.spelling))
                self.symbols.add(self.curtoken.spelling)

            self.emitter.emit("{} = ".format(self.curtoken.spelling))
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
            self.emitter.emit_line(";")
        elif self.check_token(TokenType.INPUT):
            self.match(TokenType.INPUT)

            if self.curtoken.spelling not in self.symbols:
                self.emitter.header_line(f"float {self.curtoken.spelling};")
                self.symbols.add(self.curtoken.spelling)

            self.emitter.emit_line(
                'if(0 == scanf("%' + 'f", &' + self.curtoken.spelling + ")) {"
            )
            self.emitter.emit_line(self.curtoken.spelling + " = 0;")
            self.emitter.emit('scanf("%')
            self.emitter.emit_line('*s");')
            self.emitter.emit_line("}")
            self.match(TokenType.IDENT)
        else:
            self.abort("{} does not start a valid statement".format(self.curtoken))

        self.nl()

    def comparison(self):
        """
        comparison ::= expression (("==" | "!=" | "<" | "<=" | ">" | ">=") expression)+
        """
        self.expression()

        if self.is_comparison_operator():
            self.emitter.emit(self.curtoken.spelling)
            self.next_token()
            self.expression()
        else:
            self.abort(
                "Expected comparison operator, but found {}".format(self.curtoken)
            )

        while self.is_comparison_operator():
            self.emitter.emit(self.curtoken.spelling)
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
        self.term()
        while self.check_token(TokenType.MINUS) or self.check_token(TokenType.PLUS):
            self.emitter.emit(self.curtoken.spelling)
            self.next_token()
            self.term()

    def term(self):
        """term ::= unary { ("*" | "/") unary }"""
        self.unary()
        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH):
            self.emitter.emit(self.curtoken.spelling)
            self.next_token()
            self.unary()

    def unary(self):
        """unary ::= ["+" | "-"] primary"""
        if self.check_token(TokenType.MINUS) or self.check_token(TokenType.PLUS):
            self.emitter.emit(self.curtoken.spelling)
            self.next_token()
            self.primary()
        else:
            self.primary()

    def primary(self):
        """primary ::= number | ident"""
        if self.check_token(TokenType.NUMBER):
            self.emitter.emit(self.curtoken.spelling)
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            if self.curtoken.spelling not in self.symbols:
                self.abort(
                    "Referencing a non-existent variable {}".format(
                        self.curtoken.spelling
                    )
                )
            self.emitter.emit(self.curtoken.spelling)
            self.next_token()
        else:
            self.abort(
                "Expected a number or an ident, but found {}".format(self.curtoken)
            )

    def nl(self):
        """NL ::= "\n"+"""
        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.match(TokenType.NEWLINE)

    # public API

    def parse(self):
        """parse the source file - starting rule is `program`"""
        self.program()
