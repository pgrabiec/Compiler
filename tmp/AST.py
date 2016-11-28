class Node(object):
    def __str__(self):
        try:
            return self.printTree()
        except NotImplementedError:
            return repr(self)

    def __init__(self):
        self.children = ()

    def accept(self, visitor):
        return visitor.visit(self)

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ','.join('%s= %s' % kv for kv in self.__dict__.items()) )


class BinExpr(Node):
    def __init__(self, line, op, left, right):
        super(BinExpr, self).__init__()
        self.line = line
        self.op = op
        self.left = left
        self.right = right


class Const(Node):
    def __init__(self, line, value):
        super(Const, self).__init__()
        self.line = line
        self.value = value


class Integer(Const):
    def __init__(self, line, value):
        Const.__init__(self, line, value)
        self.name = 'int'


class Float(Const):
    def __init__(self, line, value):
        Const.__init__(self, line, value)
        self.name = 'float'


class String(Const):
    def __init__(self, line, value):
        Const.__init__(self, line, value)
        self.name = 'string'


class Identifier(Node):
    def __init__(self, line, name):
        self.line = line
        self.name = name


class Variable(Node):
    def __init__(self, line, ID, value):
        super(Variable, self).__init__()
        self.line = line
        self.ID = ID
        self.value = value


class Program(Node):
    def __init__(self, line, children, top):
        super(Program, self).__init__()
        self.line = line
        self.children = children
        self.top = top


class Declaration(Node):
    def __init__(self, line, type, inits):
        super(Declaration, self).__init__()
        self.line = line
        self.type = type
        self.inits = inits


class PrintInstruction(Node):
    def __init__(self, line, expression):
        super(PrintInstruction, self).__init__()
        self.line = line
        self.expression = expression


class LabeledInstruction(Node):
    def __init__(self, line, ID, expression):
        super(LabeledInstruction, self).__init__()
        self.line = line
        self.ID = ID
        self.expression = expression


class Assignment(Node):
    def __init__(self, line, ID, expression):
        super(Assignment, self).__init__()
        self.line = line
        self.ID = ID
        self.expression = expression


class ChoiceInstruction(Node):
    def __init__(self, line, condition, instruction, alternative):
        super(ChoiceInstruction, self).__init__()
        self.line = line
        self.condition = condition
        self.instruction = instruction
        self.alternative = alternative


class WhileInstruction(Node):
    def __init__(self, line, condition, instruction):
        super(WhileInstruction, self).__init__()
        self.line = line
        self.condition = condition
        self.instruction = instruction


class RepeatInstruction(Node):
    def __init__(self, line, instruction, condition):
        super(RepeatInstruction, self).__init__()
        self.line = line
        self.instruction = instruction
        self.condition = condition


class ReturnInstruction(Node):
    def __init__(self, line, expression):
        super(ReturnInstruction, self).__init__()
        self.line = line
        self.expression = expression


class ContinueInstruction(Node):
    def __init__(self, line):
        super(ContinueInstruction, self).__init__()
        self.line = line


class BreakInstruction(Node):
    def __init__(self, line):
        super(BreakInstruction, self).__init__()
        self.line = line


class InvocationExpression(Node):
    def __init__(self, line, ID, expression):
        super(InvocationExpression, self).__init__()
        self.line = line
        self.ID = ID
        self.expression = expression


class FunctionDefinition(Node):
    def __init__(self, line, type, ID, args, body):
        super(FunctionDefinition, self).__init__()
        self.line = line
        self.type = type
        self.ID = ID
        self.args = args
        self.body = body


class Argument(Node):
    def __init__(self, line, type, ID):
        super(Argument, self).__init__()
        self.line = line
        self.type = type
        self.ID = ID
