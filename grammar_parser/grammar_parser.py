from ProductionBlock import ProductionBlock
from grammar_scanner import GrammarScanner


class GrammarParser(object):
    def __init__(self):
        self.scanner = GrammarScanner()
        self.scanner.build()

    tokens = GrammarScanner.tokens

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))
        else:
            print("Unexpected end of input")

    # [ProductionBlock] or None
    def p_grammar(self, p):
        """grammar : production_blocks
                   | """
        # print("GRAMMAR")
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = None

    # [ProductionBlock]
    def p_production_blocks(self, p):
        """production_blocks : production_blocks production_block
                             | production_block """
        # print("BLOCKS")
        if len(p) == 3:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = [p[1]]

    # ProductionBlock(string, [[string]])
    def p_production_block(self, p):
        """production_block : PAREN STRING ':' productions PAREN"""
        # print("BLOCK")
        p[0] = ProductionBlock(p[2], p[4])

    # [[string]]
    def p_productions(self, p):
        """productions : productions production
                       | production """
        # print("PRODUCTIONS")
        if len(p) == 3:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = [p[1]]

    # [string]
    def p_production(self, p):
        """production : '|' strings_opt
                      | strings_opt """
        # print("PRODUCTION")
        if len(p) == 3:
            p[0] = p[2]
        else:
            p[0] = p[1]

    # [string]
    def p_strings_opt(self, p):
        """strings_opt : strings_opt STRING
                       | STRING
                       | """
        # print("STRINGS")
        if len(p) == 3:
            p[0] = p[1]
            p[0].append(p[2])
        elif len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = []
