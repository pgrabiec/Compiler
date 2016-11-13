class Node(object):
    def __str__(self):
        return self.printTree()


class Program(Node):
    def __init__(self):
        self.segments = None

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


class Declarations(Node):
    def __init__(self):
        self.declarations = []

    def add_declaration(self, declaration):
        """:arg declaration : AST.Init"""
        self.declarations.append(declaration)


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
    def __init__(self):
        self.variable = None
        self.expression = None

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


class ReturnInstruction(Node):
    def __init__(self):
        self.expression = None

    def set_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expression = expression


class BreakInstruction(Node):
    pass


class ContinueInstruction(Node):
    pass


class ExpressionInstruction(Node):
    """Matches: 'instruction -> expression ;'"""

    def __init__(self):
        self.expression = None

    def set_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expression = expression


class PrintInstruction(Node):
    def __init__(self):
        self.args = None

    def set_args(self, args):
        """:arg args : AST.ExpressionList"""
        self.args = args


class LabeledInstruction(Node):
    def __init__(self):
        self.identifier = None
        self.instruction = None

    def set_identifier(self, identifier):
        """:arg identifier : string"""
        self.identifier = identifier

    def set_instruction(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instruction = instruction


class Assignment(Node):
    def __init__(self):
        self.variable = None
        self.expression = None

    def set_variable(self, variable):
        """:arg variable : AST.Variable"""
        self.variable = variable

    def set_expression(self, expression):
        """:arg expression : AST.Expression"""
        self.expression = expression


class ChoiceInstruction(Node):
    def __init__(self):
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


class WhileInstruction(Node):
    def __init__(self):
        self.condition = None
        self.instruction = None

    def set_condition(self, condition):
        """:arg condition : AST.Expression"""
        self.condition = condition

    def set_instruction(self, instruction):
        """:arg instruction : AST.Instruction"""
        self.instruction = instruction


class RepeatInstruction(Node):
    def __init__(self):
        self.condition = None
        self.instructions = None

    def set_condition(self, condition):
        """:arg condition : AST.Expression"""
        self.condition = condition

    def set_instructions(self, instructions):
        """:arg instructions : AST.Instructions"""
        self.instructions = instructions


class CompoundInstruction(Node):
    def __init__(self):
        self.instructions = None

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


class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Condition(Node):
    def __init__(self, expression):
        self.expression = expression


class Variable(Node):
    """Matches ID terminals when they are associated with a variable
        Also, matches the production: expression -> ID"""

    def __init__(self):
        self.identifier = None

    def set_identifier(self, identifier):
        """:arg identifier : string"""
        self.identifier = identifier


class BinExpr(Node):
    def __init__(self):
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


class BracketExpression(Node):
    """Matches production expression -> ( expression )"""

    def __init__(self, expression):
        self.expression = expression


class FunctionCallExpression(Node):
    def __init__(self):
        self.identifier = None
        self.arguments = None

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


class FunctionDefinitions(Node):
    def __init__(self):
        self.function_definitions = []

    def add_function_definition(self, function_definition):
        """:arg function_definition : AST.FunctionDefinition"""
        self.function_definitions.append(function_definition)


class FunctionDefinition(Node):
    def __init__(self):
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
    def __init__(self):
        self.argument_type = None
        self.argument_identifier = None

    def set_argument_type(self, argument_type):
        """:arg argument_type : string"""
        self.argument_type = argument_type

    def set_argument_identifier(self, argument_identifier):
        """:arg argument_identifier : string"""
        self.argument_identifier = argument_identifier
