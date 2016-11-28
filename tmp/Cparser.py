from scanner import Scanner
import AST
import re


class SyntaxError(object):
    def __init__(self, line, column, type, value):
        super(SyntaxError, self).__init__()
        self.line = line
        self.column = column
        self.type = type
        self.value = value

    def __str__(self):
        return "Syntax error at line {0}, column {1}: unexpected {2} '{3}' ".format(
            self.line, self.column, self.type, self.value)

    def arrows(self, skip=0):
        return ' ' * (self.column - 1 - skip) + '^' * len(self.value)

class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()
        self.errors = []

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
            self.errors.append(SyntaxError(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            self.errors.append("Unexpected end of input")

    def p_program(self, p):
        """program : blocks"""
        p[0] = AST.Program(p.lineno(1), p[1], True)

    def p_blocks(self, p):
        """blocks : blocks block """
        p[0] = p[1] + [p[2]]

    def p_blocks_empty(self, p):
        """blocks : """
        p[0] = []

    def p_block(self, p):
        """block : declaration
                 | fundef
                 | instruction"""
        p[0] = p[1]

    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        if len(p) == 4:
            p[0] = AST.Declaration(p.lineno(1), p[1], p[2])

    def p_inits(self, p):
        """inits : inits ',' init """
        p[0] = p[1] + [p[3]]

    def p_inits_single(self, p):
        """inits : init """
        p[0] = [p[1]]

    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = AST.Variable(p.lineno(1), p[1], p[3])

    def p_instructions(self, p):
        """instructions : instructions instruction """
        p[0] = p[1] + [p[2]]

    def p_instruction_single(self, p):
        """instructions : instruction """
        p[0] = [p[1]]

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
        p[0] = p[1]

    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """
        p[0] = AST.PrintInstruction(p.lineno(1), p[2])

    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        p[0] = AST.LabeledInstruction(p.lineno(1), p[1], p[3])

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        id = AST.Identifier(p.lineno(1), p[1])
        p[0] = AST.Assignment(p.lineno(2), id, p[3])

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        if len(p) < 8:
            p[0] = AST.ChoiceInstruction(p.lineno(1), p[3], p[5], None)
        else:
            p[0] = AST.ChoiceInstruction(p.lineno(1), p[3], p[5], p[7])

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.WhileInstruction(p.lineno(1), p[3], p[5])

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = AST.RepeatInstruction(p.lineno(1), p[2], p[4])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.ReturnInstruction(p.lineno(1), p[2])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstruction(p.lineno(1))

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstruction(p.lineno(1))

    def p_compound_instr(self, p):
        """compound_instr : '{' blocks '}' """
        p[0] = AST.Program(p.lineno(1), p[2], False)

    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]

    def p_const_integer(self, p):
        """const : INTEGER """
        p[0] = AST.Integer(p.lineno(1), p[1])

    def p_const_float(self, p):
        """const : FLOAT """
        p[0] = AST.Float(p.lineno(1), p[1])

    def p_const_string(self, p):
        """const : STRING """
        p[0] = AST.String(p.lineno(1), p[1])

    def p_expression(self, p):
        """expression : const """
        p[0] = p[1]

    def p_expression_id(self, p):
        """expression : ID """
        p[0] = AST.Identifier(p.lineno(1), p[1])

    def p_expression_paren(self, p):
        """expression : '(' expression ')'
                      | '(' error ')'"""
        p[0] = p[2]

    def p_expression_bin(self, p):
        """expression : expression '+' expression
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
                      | expression GE expression """
        p[0] = AST.BinExpr(p.lineno(2), p[2], p[1], p[3])

    def p_invocation(self, p):
        """expression : ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        p[0] = AST.InvocationExpression(p.lineno(1), p[1], p[3])

    def p_expr_list_empty(self, p):
        """expr_list_or_empty : """
        p[0] = []

    def p_expr_list_non_empty(self, p):
        """expr_list_or_empty : expr_list """
        p[0] = p[1]

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression """
        p[0] = p[1] + [p[3]]

    def p_expr_list_single(self, p):
        """expr_list : expression """
        p[0] = [p[1]]

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = AST.FunctionDefinition(p.lineno(1), p[1], p[2], p[4], p[6])

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : """
        p[0] = []

    def p_args_list_non_empty(self, p):
        """args_list_or_empty : args_list """
        p[0] = p[1]

    def p_args_list(self, p):
        """args_list : args_list ',' arg """
        p[0] = p[1] + [p[3]]

    def p_args_list_single(self, p):
        """args_list : arg """
        p[0] = [p[1]]

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = AST.Argument(p.lineno(1), p[1], p[2])
