import os
import sys
import ply.yacc as yacc
from grammar_parser import GrammarParser


# filters input into only '\"\"\"' and what is between two '\"\"\"'
def truncate_input(text):
    state = -3
    length = len(text)
    output = ""
    p = 0
    while p < length:
        character = text[p]
        if character == "\"":
            if state == -3:
                state += 1
            elif state == -2:
                state += 1
            elif state == -1:
                state += 1
                output += "\"\"\""
            elif state == 0:
                state += 1
            elif state == 1:
                state += 1
            elif state == 2:
                output += "\"\"\"\n"
                state = -3
        else:
            if state == -3:
                pass
            elif state == -2:
                state = -3
            elif state == -1:
                state = -3
            elif state == 0:
                output += character
            elif state == 1:
                output += "\"" + character
                state = 0
            elif state == 2:
                output += "\"\"" + character
                state = 0
        p += 1
    return output


def extract_grammar():
    try:
        grammar_path = sys.argv[1] if len(sys.argv) > 1 else ".." + os.path.sep + "Cparser.py"
        grammar_file = open(grammar_path, "r")
    except IOError:
        print("Cannot open {0} file".format(grammar_path))
        sys.exit(0)

    grammar_parser = GrammarParser()
    parser = yacc.yacc(module=grammar_parser)
    text = truncate_input(grammar_file.read())
    productions = parser.parse(text, lexer=grammar_parser.scanner)
    grammar = ""
    if productions is None:
        print("No grammar")
        return
    for production in productions:
        grammar += str(production)

    output_path = "." + os.path.sep + "grammar_generated.txt"
    output_file = open(output_path, "w")
    output_file.write(grammar)
    print("Grammar extracted successfully to file: " + output_path)


if __name__ == '__main__':
    extract_grammar()
