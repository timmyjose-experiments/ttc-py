import sys
from pathlib import Path

from ttc_py.lexer import *


def usage():
    print("Usage: ttc <source-fie>")
    sys.exit(0)


def main():
    if len(sys.argv) != 2:
        usage()

    source_text = Path(sys.argv[1]).read_text()
    lexer = Lexer(source_text)

    token = lexer.get_token()
    while token.kind != TokenType.EOF:
        print(token)
        token = lexer.get_token()


if __name__ == "__main__":
    main()
