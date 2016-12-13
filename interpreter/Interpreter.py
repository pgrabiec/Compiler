import sys

from interpreter.Exceptions import *
from interpreter.Memory import *

import AST
from interpreter.visit import *

sys.setrecursionlimit(10000)


def integer_represents_true(int_value):
    if int_value == 1:
        return True
    return False


class Interpreter(object):
    def __init__(self):
        super().__init__()
        self.mem = MemoryManager()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        for segment in node.segments:
            self.visit(segment)

    # Mapping for identifier:
    # key: <identifier>
    # value: tuple (<value>, <type>)
    @when(AST.Declaration)
    def visit(self, node):
        variable_type = node.variable_type
        inits = node.inits
        mem = self.mem
        for init in inits:
            identifier = init.identifier
            expression = self.visit(init.expression)
            mem.declare(identifier, (expression, variable_type))

    # @when(AST.Init)
    # def visit(self, node):
    #     pass

    @when(AST.PrintInstruction)
    def visit(self, node):
        args = node.args
        for arg in args:
            expression = self.visit(arg)
            print(expression)

    # Mapping for labeled instruction:
    # key: <identifier>
    # value: <instruction>
    @when(AST.LabeledInstruction)
    def visit(self, node):
        identifier = node.identifier
        instruction = node.instruction
        self.mem.declare(identifier, instruction)
        self.visit(instruction)

    @when(AST.Assignment)
    def visit(self, node):
        identifier = node.identifier.identifier
        expresssion = self.visit(node.expression)
        self.mem.update_value(identifier, expresssion)

    @when(AST.ChoiceInstruction)
    def visit(self, node):
        condition = self.visit(node.expression)
        instruction_true = node.instruction_true
        instruction_false = node.instruction_false
        if integer_represents_true(condition):
            self.visit(instruction_true)
        else:
            if instruction_false is not None:
                self.visit(instruction_false)

    @when(AST.WhileInstruction)
    def visit(self, node):
        condition = node.condition
        instruction = node.instruction
        mem = self.mem
        while integer_represents_true(self.visit(condition)):
            mem.push_loop_scope()
            try:
                self.visit(instruction)
                mem.pop_loop_scopes()
            except BreakException:
                mem.pop_loop_scopes()
                break
            except ContinueException:
                mem.pop_loop_scopes()


    @when(AST.RepeatInstruction)
    def visit(self, node):
        condition = node.condition
        instruction = node.instruction
        

    @when(AST.ReturnInstruction)
    def visit(self, node):
        pass

    @when(AST.BreakInstruction)
    def visit(self, node):
        pass

    @when(AST.ContinueInstruction)
    def visit(self, node):
        pass

    @when(AST.Const)
    def visit(self, node):
        pass

    @when(AST.Integer)
    def visit(selfself, node):
        pass

    @when(AST.Float)
    def visit(self, node):
        pass

    @when(AST.String)
    def visit(self, node):
        pass

    @when(AST.Identifier)
    def visit(self, node):
        pass

    @when(AST.FunctionCallExpression)
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        pass

    @when(AST.FunctionDefinition)
    def visit(self, node):
        pass

    @when(AST.Argument)
    def visit(self, node):
        pass

    @when(AST.Variable)
    def visit(self, node):
        pass
