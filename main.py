import sys

import ply.yacc as yacc
from Cparser import Cparser
# import TreePrinter    # -- Parser --
from interpreter.Interpreter import Interpreter
from semantics.TypeChecker import TypeChecker
# from interpreter.Interpreter import Interpreter

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    # -- Parser --
    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()
    ast = parser.parse(text, lexer=Cparser.scanner)
    #  print(ast)

    # -- Type Checker --
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    for err in typeChecker.errors:
        print(err)
    if len(typeChecker.errors) == 0:
        ast.accept(Interpreter())
