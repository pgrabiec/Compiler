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
    pass


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
