import AST as ast
from scanner import Scanner
import TreePrinter


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

    def p_program(self, p):
        """program : segments"""
        if len(p) == 2:
            segments = p[1]
            program = ast.Program()
            program.set_segments(segments=segments)
            p[0] = program
        else:
            raise Exception

    def p_segments(self, p):
        """segments : segments segment
                    | """
        if len(p) == 3:
            if p[1] is None:
                p[0] = ast.Segments()
                p[0].add_segment(p[2])
            else:
                p[0] = p[1]
                p[0].add_segment(p[2])
        elif len(p) == 1:
            p[0] = ast.Segments()
        else:
            raise Exception

    def p_segment(self, p):
        """segment : declaration
                   | fundef
                   | instruction """
        if len(p) == 2:
            p[0] = ast.Segment(p[1])
        else:
            raise Exception
        if p[1] is None:
            raise Exception

    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        if len(p) == 4:
            p[0] = ast.Declaration(p[1], p[2])
        else:
            raise Exception

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 4:
            p[0] = p[1]
            p[0].add_init(p[3])
        elif len(p) == 2:
            p[0] = ast.Inits()
            p[0].add_init(p[1])
        else:
            raise Exception

    def p_init(self, p):
        """init : ID '=' expression """
        if len(p) == 4:
            p[0] = ast.Init()
            variable = ast.Variable()
            variable.set_identifier(p[1])
            p[0].set_variable(variable=variable)
            p[0].set_expression(p[3])

    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 3:
            p[0] = p[1]
            p[0].add_instruction(p[2])
        elif len(p) == 2:
            p[0] = ast.Instructions()
            p[0].add_instruction(p[1])

    def p_instruction(self, p):
        """instruction : print_instruction
                       | labeled_instruction
                       | assignment
                       | choice_instruction
                       | while_instruction
                       | repeat_instruction
                       | return_instruction
                       | break_instruction
                       | continue_instruction
                       | compound_instruction
                       | expression ';' """
        if len(p) == 2 or len(p) == 3:
            p[0] = p[1]

    def p_print_instruction(self, p):
        """print_instruction : PRINT expr_list ';'
                             | PRINT error ';' """
        if len(p) == 4:
            p[0] = ast.PrintInstruction()
            p[0].set_args(p[2])

    def p_labeled_instruction(self, p):
        """labeled_instruction : ID ':' instruction """
        p[0] = ast.LabeledInstruction()
        p[0].set_identifier(p[1])
        p[0].set_instruction(p[3])

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        if len(p) == 5:
            variable = ast.Variable()
            variable.set_identifier(p[1])
            p[0] = ast.Assignment()
            p[0].set_variable(variable=variable)
            p[0].set_expression(p[3])

    def p_choice_instruction(self, p):
        """choice_instruction : IF '(' condition ')' instruction  %prec IFX
                              | IF '(' condition ')' instruction ELSE instruction
                              | IF '(' error ')' instruction  %prec IFX
                              | IF '(' error ')' instruction ELSE instruction """
        if len(p) >= 6:
            p[0] = ast.ChoiceInstruction()
            p[0].set_condition(p[3])
            p[0].set_instruction_true(p[5])
            p[0].set_instruction_false(None)
        if len(p) == 8:
            p[0].set_instruction_false(p[7])

    def p_while_instruction(self, p):
        """while_instruction : WHILE '(' condition ')' instruction
                             | WHILE '(' error ')' instruction """
        if len(p) == 6:
            p[0] = ast.WhileInstruction()
            p[0].set_condition(p[3])
            p[0].set_instruction(p[5])

    def p_repeat_instruction(self, p):
        """repeat_instruction : REPEAT instructions UNTIL condition ';' """
        if len(p) == 6:
            p[0] = ast.RepeatInstruction()
            p[0].set_condition(p[2])
            p[0].set_instructions(p[4])

    def p_return_instruction(self, p):
        """return_instruction : RETURN expression ';' """
        if len(p) == 4:
            p[0] = ast.ReturnInstruction()
            p[0].set_expression(p[2])

    def p_break_instruction(self, p):
        """break_instruction : BREAK ';' """
        if len(p) == 3:
            p[0] = ast.BreakInstruction()

    def p_continue_instruction(self, p):
        """continue_instruction : CONTINUE ';' """
        if len(p) == 3:
            p[0] = ast.ContinueInstruction()

    def p_compound_instruction(self, p):
        """compound_instruction : '{' compound_segments '}' """
        if len(p) == 4:
            p[0] = ast.CompoundInstruction()
            p[0].set_instructions(p[2])

    def p_compound_segments(self, p):
        """compound_segments : compound_segments compound_segment
                             | """
        if len(p) == 3:
            p[0] = p[1]
            p[0].add_segment(p[2])
        elif len(p) == 1:
            p[0] = ast.CompoundSegments()

    def p_compound_segment(self, p):
        """compound_segment : declaration
                            | instruction """
        if len(p) == 2:
            p[0] = ast.CompoundSegment(p[1])

    def p_condition(self, p):
        """condition : expression"""
        if len(p) == 2:
            p[0] = ast.Condition(p[1])

    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING """
        if len(p) == 2:
            p[0] = ast.Const(p[1])

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
        if len(p) == 2:
            p[0] = ast.Const(str(p[1]).replace("\n", ""))
        elif len(p) == 4:
            if p[1] == '(':
                p[0] = ast.BracketExpression(p[2])
            else:
                p[0] = ast.BinExpr()
                p[0].set_op(p[2])
                p[0].set_left(p[1])
                p[0].set_right(p[3])
        elif len(p) == 5:
            p[0] = ast.FunctionCallExpression()
            p[0].set_identifier(p[1])
            p[0].set_arguments(p[3])
        else:
            raise Exception

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ast.ExpressionList()

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 4:
            p[0] = p[1]
            p[0].add_expression(p[3])
        elif len(p) == 2:
            p[0] = ast.ExpressionList()
            p[0].add_expression(p[1])
        else:
            raise Exception

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instruction """
        if len(p) == 7:
            p[0] = ast.FunctionDefinition()
            p[0].set_type(p[1])
            p[0].set_identifier(p[2])
            p[0].set_arguments(p[4])
            p[0].set_instructions(p[6])
        else:
            raise Exception

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 1:
            p[0] = ast.ArgumentsList()  # empty

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        if len(p) == 4:
            p[0] = p[1]
            p[0].add_argument(p[3])
        elif len(p) == 2:
            p[0] = ast.ArgumentsList()
            p[0].add_argument(p[1])

    def p_arg(self, p):
        """arg : TYPE ID """
        if len(p) == 3:
            p[0] = ast.Argument()
            p[0].set_argument_type(p[1])
            p[0].set_argument_identifier(p[2])
