from scanner import Scanner


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '|'),
        ("left", '^'),
        ("left", '&'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", 'SHL', 'SHR'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))
        else:
            print("Unexpected end of input")

    # TODO - PG
    def p_program(self, p):
        """program : segments """
        p[0] = "Result for matching goes here"

    def p_segments(self, p):
        """segments : segments segment
                   | """

    def p_segment(self, p):
        """segment : declarations
                   | fundefs_opt
                   | instructions_opt """

    # TODO - PG
    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """

    # TODO - PG
    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """

    # TODO - PG
    def p_inits(self, p):
        """inits : inits ',' init
                 | init """

    # TODO - PG
    def p_init(self, p):
        """init : ID '=' expression """

    # TODO - PG
    def p_instructions_opt(self, p):
        """instructions_opt : instructions
                            | """

    # TODO - PG
    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """

    # TODO - PG
    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """

    # TODO - PG
    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """

    # TODO - PG
    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """

    # TODO - PG
    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """

    # TODO - PG
    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """

    # TODO - PG
    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """

    # TODO - WB
    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """

    # TODO - WB
    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """

    # TODO - WB
    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """

    # TODO - WB
    def p_break_instr(self, p):
        """break_instr : BREAK ';' """

    # TODO - WB
    def p_compound_instr(self, p):
        """compound_instr : '{' compound_segments '}' """

    def p_compound_segments(self, p):
        """compound_segments : compound_segments compound_segment
                             | """

    def p_compound_segment(self, p):
        """compound_segment : declarations
                             | instructions_opt """

    # TODO - WB
    def p_condition(self, p):
        """condition : expression"""

    # TODO - WB
    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""

    # TODO - WB
    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """

    # TODO - WB
    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """

    # TODO - WB
    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """

    # TODO - WB
    def p_fundefs_opt(self, p):
        """fundefs_opt : fundefs
                       | """

    # TODO - WB
    def p_fundefs(self, p):
        """fundefs : fundefs fundef
                   | fundef """

    # TODO - WB
    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """

    # TODO - WB
    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """

    # TODO - WB
    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """

    # TODO - WB
    def p_arg(self, p):
        """arg : TYPE ID """
