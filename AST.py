class Node(object):
    def __str__(self):
        return self.printTree(0)

    def __init__(self, line):
        self.line = line


class Program(Node):
    def __init__(self, line, segments):
        """:arg segments : AST.Segments"""
        super().__init__(line)
        self.segments = segments


class Segments(Node):
    def __init__(self, line=None, segment=None):
        """:arg segment : AST.Segment"""
        super().__init__(line)
        self.segments = []
        self.segments.append(segment)


class Segment(Node):
    def __init__(self, line, content):
        super().__init__(line)
        self.content = content


class Declaration(Node):
    def __init__(self, line, variable_type, inits):
        super().__init__(line)
        self.variable_type = variable_type
        self.inits = inits


class Inits(Node):
    def __init__(self, line, init):
        super().__init__(line)
        self.inits = []
        self.inits.append(init)


class Init(Node):
    def __init__(self, line, variable, expression):
        """:arg variable : AST.VariableReference
           :arg expression : AST.Expression"""
        super().__init__(line)
        self.variable = variable
        self.expression = expression


class Instructions(Node):
    def __init__(self, line, instruction):
        super().__init__(line)
        self.instructions = []
        self.instructions.append(instruction)


class PrintInstruction(Node):
    def __init__(self, line, args):
        """:arg args : AST.ExpressionList"""
        super().__init__(line)
        self.args = args


class LabeledInstruction(Node):
    def __init__(self, line, identifier, instruction):
        """:arg identifier : string
           :arg instruction : AST.Instruction"""
        super().__init__(line)
        self.identifier = identifier
        self.instruction = instruction


class Assignment(Node):
    def __init__(self, line, variable, expression):
        """:arg variable : AST.VariableReference
           :arg expression : AST.Expression"""
        super().__init__(line)
        self.variable = variable
        self.expression = expression


class ChoiceInstruction(Node):
    def __init__(self, line, condition, instruction_true, instruction_false):
        """:arg instruction_true : AST.Instruction
           :arg instruction_false : AST.Instruction
           :arg condition : AST.Expression"""
        super().__init__(line)
        self.condition = condition
        self.instruction_true = instruction_true
        self.instruction_false = instruction_false


class WhileInstruction(Node):
    def __init__(self, line, condition, instruction):
        """:arg instruction : AST.Instruction"""
        super().__init__(line)
        self.condition = condition
        self.instruction = instruction


class RepeatInstruction(Node):
    def __init__(self, line, instructions, condition):
        """:arg instructions : AST.Instructions"""
        super().__init__(line)
        self.instructions = instructions
        self.condition = condition


class ReturnInstruction(Node):
    def __init__(self, line, expression):
        super().__init__(line)
        self.expression = expression


class BreakInstruction(Node):
    pass


class ContinueInstruction(Node):
    pass


class CompoundInstruction(Node):
    def __init__(self, line, instructions):
        """:arg instructions : AST.CompoundSegments"""
        super().__init__(line)
        self.instructions = instructions


class CompoundSegments(Node):
    def __init__(self, line=None, segment=None):
        """:arg segment : AST.CompoundSegment"""
        super().__init__(line)
        self.segments = []
        self.segments.append(segment)


class CompoundSegment(Node):
    def __init__(self, line, content):
        super().__init__(line)
        self.content = content


class Condition(Node):
    def __init__(self, line, expression):
        super().__init__(line)
        self.expression = expression


class Const(Node):
    def __init__(self, line, value):
        super().__init__(line)
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
    def __init__(self, line, left, op, right):
        """:arg left : AST.Expression
           :arg op : string
           :arg right : AST.Expression"""
        super().__init__(line)
        self.left = left
        self.op = op
        self.right = right


class FunctionCallExpression(Node):
    def __init__(self, line, identifier, arguments):
        """:arg identifier : string
           :arg arguments : AST.ExpressionList"""
        super().__init__(line)
        self.identifier = identifier
        self.arguments = arguments


class ExpressionList(Node):
    def __init__(self, line=None, expression=None):
        """:arg expression : AST.Expression"""
        super().__init__(line)
        self.expressions = []
        self.expressions.append(expression)


class FunctionDefinition(Node):
    def __init__(self, line, type, identifier, arguments, instructions):
        """:arg type : string
           :arg identifier : string
           :arg arguments : AST.ArgumentsList
           :arg instructions : AST.CompoundInstruction"""
        super().__init__(line)
        self.type = type
        self.identifier = identifier
        self.arguments = arguments
        self.instructions = instructions


class ArgumentsList(Node):
    def __init__(self, line=None, argument=None):
        """:arg argument : AST.Argument"""
        super().__init__(line)
        self.arguments = []
        self.arguments.append(argument)


class Argument(Node):
    def __init__(self, line, argument_type, argument_identifier):
        """:arg argument_type : string
           :arg argument_identifier : string"""
        super().__init__(line)
        self.argument_type = argument_type
        self.argument_identifier = argument_identifier


class VariableReference(Node):
    """Matches ID terminals when they are associated with a variable
        Also, matches the production: expression -> ID"""

    def __init__(self, line, identifier):
        """:arg identifier : string"""
        super().__init__(line)
        self.identifier = identifier
