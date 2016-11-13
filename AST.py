class Node(object):
    def __str__(self):
        return self.printTree()


class Program(Node):
    def __init__(self):
        super().__init__()
        self.segments = None

    def set_segments(self, segments):
        """:arg segments : AST.Segments"""
        self.segments = segments


class Segments(Node):
    def __init__(self):
        super().__init__()
        self.segments = []

    def add_segment(self, segment):
        """:arg segment : AST.Segment"""
        self.segments.append(segment)


class Segment(Node):
    def __init__(self, content):
        self.content = content


class CompoundSegment(Node):
    pass


class VariableInits(Segment, CompoundSegment):
    def __init__(self):
        super().__init__()
        self.variable_inits = []

    def add_variable_init(self, variable_init):
        """:arg variable_init : AST.VariableInit"""
        self.variable_inits.append(variable_init)


class VariableInit(Node):
    def __init__(self):
        super().__init__()
        self.variable = None
        self.expression = None

    def set_variable(self, variable):
        """:arg variable : AST.Variable"""
        self.variable = variable

    def set_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expression = expression
#
# -----------------------------------
#


class FunctionDefinitions(Segment):
    def __init__(self):
        super().__init__()
        self.function_definitions = []

    def add_function_definition(self, function_definition):
        """:arg function_definition : AST.FunctionDefinition"""
        self.function_definitions.append(function_definition)


class FunctionDefinition(Node):
    def __init__(self):
        super().__init__()
        self.type = None
        self.identifier = None
        self.arguments = None
        self.instructions = None

    def set_type(self, type):
        """:arg type : string"""
        self.type = type

    def set_identifier(self, identifier):
        """:arg identifier : string"""
        self.identifier = identifier

    def set_arguments(self, arguments):
        """:arg arguments : AST.FunctionArguments"""
        self.arguments = arguments

    def set_instructions(self, instrunctions):
        """:arg instrunctions : AST.CompoundInstruction"""
        self.instructions = instrunctions


class FunctionArguments(Node):
    def __init__(self):
        super().__init__()
        self.arguments = []

    def add_function_argument(self, argument):
        """:arg argument : AST.FunctionArgument"""
        self.arguments.append(argument)


class FunctionArgument(Node):
    def __init__(self):
        super().__init__()
        self.argument_type = None
        self.argument_identifier = None

    def set_argument_type(self, argument_type):
        """:arg argument_type : string"""
        self.argument_type = argument_type

    def set_argument_identifier(self, argument_identifier):
        """:arg argument_identifier : string"""
        self.argument_identifier = argument_identifier


class CompoundSegments(Node):
    def __init__(self):
        super().__init__()
        self.segments = []

    def add_segment(self, segment):
        """:arg segment : AST.CompoundSegment"""
        self.segments.append(segment)


class InstructionsList(Segment, CompoundSegment):
    def __init__(self):
        super().__init__()
        self.instructions = []

    def add_instruction(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instructions.append(instruction)


class Instruction(Node):
    pass


class CompoundInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self.instructions = None

    def set_instructions(self, instructions):
        """:arg instructions : AST.CompoundSegments"""
        self.instructions = instructions


class ReturnInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self.expression = None

    def set_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expression = expression


class BreakInstruction(Instruction):
    pass


class ContinueInstruction(Instruction):
    pass


class ExpressionInstruction(Instruction):
    """Matches: 'instruction -> expression ;'"""
    def __init__(self):
        super().__init__()
        self.expression = None

    def set_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expression = expression


class ExpressionList(Node):
    def __init__(self):
        super().__init__()
        self.expressions = []

    def add_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expressions.append(expression)


class PrintInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self.args = None

    def set_args(self, args):
        """:arg args : AST.ExpressionList"""
        self.args = args


class LabeledInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self.identifier = None
        self.instruction = None

    def set_identifier(self, identifier):
        """:arg identifier : string"""
        self.identifier = identifier

    def set_instruction(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instruction = instruction


class Assignment(Instruction):
    def __init__(self):
        super().__init__()
        self.variable = None
        self.expression = None

    def set_variable(self, variable):
        """:arg variable : AST.Variable"""
        self.variable = variable

    def set_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expression = expression


class IfInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self.condition = None
        self.instruction_true = None
        self.instruction_false = None

    def set_condition(self, condition):
        """:arg condition : AST.Expression"""
        self.condition = condition

    def set_instruction_true(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instruction_true = instruction

    def set_instruction_false(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instruction_false = instruction


class WhileInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self.condition = None
        self.instruction = None

    def set_condition(self, condition):
        """:arg condition : AST.Expression"""
        self.condition = condition

    def set_instruction(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instruction = instruction


class RepeatInstruction(Instruction):
    def __init__(self):
        super().__init__()
        self.condition = None
        self.instructions = None

    def set_condition(self, condition):
        """:arg condition : AST.Expression"""
        self.condition = condition

    def set_instructions(self, instructions):
        """:arg instructions : AST.InstructionsList"""
        self.instructions = instructions


class Expression(Node):
    pass


class Const(Expression):
    def __init__(self):
        super().__init__()
        self.value = None

    def set_value(self, value):
        """:arg value : string"""
        self.value = value


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Expression):
    """Matches ID terminals when they are associated with a variable"""
    def __init__(self):
        super().__init__()
        self.identifier = None

    def set_identifier(self, identifier):
        """:arg identifier : string"""
        self.identifier = identifier


class BinExpr(Node):
    def __init__(self):
        super().__init__()
        self.op = None
        self.left = None
        self.right = None

    def set_op(self, op):
        """:arg op : string"""
        self.op = op

    def set_left(self, left):
        """:arg left : AST.Expression"""
        self.left = left

    def set_reght(self, right):
        """:arg right : AST.Expression"""
        self.left = right


class FunctionCall(Expression):
    def __init__(self):
        super().__init__()
        self.identifier = None
        self.arguments = None

    def set_identifier(self, identifier):
        """:arg identifier : string"""
        self.identifier = identifier

    def set_arguments(self, arguments):
        """:arg arguments : AST.ExpressionList"""
        self.arguments = arguments
