class Node(object):
    def __str__(self):
        return self.printTree(0)


class Program(Node):
    def set_segments(self, segments):
        """:arg segments : AST.Segments"""
        self.segments = segments


class Segments(Node):
    def __init__(self):
        self.segments = []

    def add_segment(self, segment):
        """:arg segment : AST.Segment"""
        self.segments.append(segment)


class Segment(Node):
    def __init__(self, content):
        self.content = content


class Declaration(Node):
    def __init__(self, variable_type, inits):
        self.variable_type = variable_type
        self.inits = inits


class Inits(Node):
    def __init__(self):
        self.inits = []

    def add_init(self, init):
        self.inits.append(init)


class Init(Node):
    def set_variable(self, variable):
        """:arg variable : AST.Variable"""
        self.variable = variable

    def set_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expression = expression


class Instructions(Node):
    def __init__(self):
        self.instructions = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)


class PrintInstruction(Node):
    def set_args(self, args):
        """:arg args : AST.ExpressionList"""
        self.args = args


class LabeledInstruction(Node):
    def set_identifier(self, identifier):
        """:arg identifier : string"""
        self.identifier = identifier

    def set_instruction(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instruction = instruction


class Assignment(Node):
    def set_variable(self, variable):
        """:arg variable : AST.Variable"""
        self.variable = variable

    def set_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expression = expression


class ChoiceInstruction(Node):
    def set_condition(self, condition):
        """:arg condition : AST.Expression"""
        self.condition = condition

    def set_instruction_true(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instruction_true = instruction

    def set_instruction_false(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instruction_false = instruction


class WhileInstruction(Node):
    def set_condition(self, condition):
        self.condition = condition

    def set_instruction(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instruction = instruction


class RepeatInstruction(Node):
    def set_condition(self, condition):
        self.condition = condition

    def set_instructions(self, instructions):
        """:arg instructions : AST.Instructions"""
        self.instructions = instructions


class ReturnInstruction(Node):
    def set_expression(self, expression):
        self.expression = expression


class BreakInstruction(Node):
    pass


class ContinueInstruction(Node):
    pass


class CompoundInstruction(Node):
    def set_instructions(self, instructions):
        """:arg instructions : AST.CompoundSegments"""
        self.instructions = instructions


class CompoundSegments(Node):
    def __init__(self):
        self.segments = []

    def add_segment(self, segment):
        """:arg segment : AST.CompoundSegment"""
        self.segments.append(segment)


class CompoundSegment(Node):
    def __init__(self, content):
        self.content = content


class Condition(Node):
    def __init__(self, expression):
        self.expression = expression


class Const(Node):
    def __init__(self, value):
        self.value = value


# Terminal
class Integer(Const):
    pass


# Terminal
class Float(Const):
    pass


# Terminal
class String(Const):
    pass


class BinExpr(Node):
    def set_op(self, op):
        """:arg op : string"""
        self.op = op

    def set_left(self, left):
        """:arg left : AST.Expression"""
        self.left = left

    def set_right(self, right):
        """:arg right : AST.Expression"""
        self.right = right


class BracketExpression(Node):
    """Matches production expression -> ( expression )"""

    def __init__(self, expression):
        self.expression = expression


class FunctionCallExpression(Node):
    def set_identifier(self, identifier):
        """:arg identifier : string"""
        self.identifier = identifier

    def set_arguments(self, arguments):
        """:arg arguments : AST.ExpressionList"""
        self.arguments = arguments


class ExpressionList(Node):
    def __init__(self):
        self.expressions = []

    def add_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expressions.append(expression)


class FunctionDefinition(Node):
    def set_type(self, type):
        """:arg type : string"""
        self.type = type

    def set_identifier(self, identifier):
        """:arg identifier : string"""
        self.identifier = identifier

    def set_arguments(self, arguments):
        """:arg arguments : AST.ArgumentsList"""
        self.arguments = arguments

    def set_instructions(self, instrunctions):
        """:arg instrunctions : AST.CompoundInstruction"""
        self.instructions = instrunctions


class ArgumentsList(Node):
    def __init__(self):
        self.arguments = []

    def add_argument(self, argument):
        """:arg argument : AST.Argument"""
        self.arguments.append(argument)


class Argument(Node):
    def set_argument_type(self, argument_type):
        """:arg argument_type : string"""
        self.argument_type = argument_type

    def set_argument_identifier(self, argument_identifier):
        """:arg argument_identifier : string"""
        self.argument_identifier = argument_identifier


class Variable(Node):
    """Matches ID terminals when they are associated with a variable
        Also, matches the production: expression -> ID"""
    def set_identifier(self, identifier):
        """:arg identifier : string"""
        self.identifier = identifier
