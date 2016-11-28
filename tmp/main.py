import sys
import ply.yacc as yacc
from Cparser import Cparser
from SymbolTable import SymbolTable
from TypeChecker import TypeChecker
import TreePrinter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()
    ast = parser.parse(text, lexer=Cparser.scanner)
    if Cparser.errors:
        lines = text.split('\n')
        for err in Cparser.errors:
            try:
                line = lines[err.line - 1]
                # extract leading whitespace
                indent = line[:-len(line.lstrip())]
                arrows = indent + err.arrows(len(indent))
                print(err)
                print(line)
                print(arrows)
            except AttributeError:
                print(err)
    else:
        typeChecker = TypeChecker()
        global_scope = SymbolTable(None, "<global scope>")
        typeChecker.visit(ast, global_scope)
        if typeChecker.errors:
            for err in typeChecker.errors:
                print(err)
        # else:
            # print(ast)
