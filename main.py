import sys
from pathlib import Path

from ttc_py.lexer import *
from ttc_py.parser import *


def usage():
    print("Usage: ttc <source-fie>")
    sys.exit(0)


def read_source_file(infile):
    return Path(infile).read_text()


def main():
    if len(sys.argv) != 2:
        usage()

    parser = Parser(Lexer(read_source_file(sys.argv[1])))
    parser.parse()
    print("Program parsed successfully")


if __name__ == "__main__":
    main()
