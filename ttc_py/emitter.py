from pathlib import Path
from ttc_py.lexer import *
from ttc_py.parser import *


class Emitter:
    """Translate the source program into equivalent valid C code"""

    def __init__(self, outfile):
        self.outfile = outfile
        self.header = ""
        self.code = ""

    def emit(self, code):
        self.code += code

    def emit_line(self, code):
        self.code += code + "\n"

    def header_line(self, code):
        self.header += code + "\n"

    def write_file(self):
        Path(self.outfile).write_text(self.header + self.code)