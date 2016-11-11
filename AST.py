class Node(object):
    def __str__(self):
        return self.printTree()


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


# TODO - PG
class Const(Node):
    pass


# Done
class Integer(Const):
    pass


# Done
class Float(Const):
    pass


# Done
class String(Const):
    pass


# TODO - PG
class Variable(Node):
    pass


# TODO - PG
class Program(Node):
    pass


# TODO - PG
class Declarations(Node):
    pass


# TODO - PG
class Declaration(Node):
    pass


# TODO - PG
class Inits(Node):
    pass


# TODO - PG
class Init(Node):
    pass


# TODO - PG
class InstructionsOpt(Node):
    pass


# TODO - PG
class Instructions(Node):
    pass


# TODO - PG
class Instruction(Node):
    pass


# TODO - PG
class PrintInstr(Node):
    pass


# TODO - PG
class LabeledInstr(Node):
    pass


# TODO - PG
class Assignment(Node):
    pass


# TODO - PG
class ChoiceInstr(Node):
    pass


# TODO - PG
class WhileInstr(Node):
    pass


# TODO - WB
class RepeatInstr(Node):
    pass


# TODO - WB
class ReturnInstr(Node):
    pass


# TODO - WB
class ContinueInstr(Node):
    pass


# TODO - WB
class BreakInstr(Node):
    pass


# TODO - WB
class CompoundInstr(Node):
    pass


# TODO - WB
class Condition(Node):
    pass


# TODO - WB
class Expression(Node):
    pass


# TODO - WB
class ExprListOrEmpty(Node):
    pass


# TODO - WB
class ExprList(Node):
    pass


# TODO - WB
class FundefsOpt(Node):
    pass


# TODO - WB
class Fundefs(Node):
    pass


# TODO - WB
class Fundef(Node):
    pass


# TODO - WB
class ArgsListOrEmpty(Node):
    pass


# TODO - WB
class ArgsList(Node):
    pass


# TODO - WB
class Arg(Node):
    pass
