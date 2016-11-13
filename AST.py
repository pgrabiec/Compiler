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


class VariableInits(Segment):
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

































class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Const(Node):
    def __init__(self, value):
        super().__init__()
        self.value = value


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Node):
    def __init__(self, identifier):
        super().__init__()
        self.identifier = identifier
