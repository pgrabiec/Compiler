import sys

from interpreter.Exceptions import *
from interpreter.Memory import *

import AST
from interpreter.visit import *

sys.setrecursionlimit(10000)


class Interpreter(object):
    @on('node')
    def visit(self, node):
        pass

    @when(AST.Node)
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        pass

    @when(AST.Declaration)
    def visit(self, node):
        pass

    @when(AST.Init)
    def visit(self, node):
        pass

    @when(AST.PrintInstruction)
    def visit(self, node):
        pass

    @when(AST.LabeledInstruction)
    def visit(self, node):
        pass

    @when(AST.Assignment)
    def visit(self, node):
        pass

    @when(AST.ChoiceInstruction)
    def visit(self, node):
        pass

    @when(AST.WhileInstruction)
    def visit(self, node):
        pass

    @when(AST.RepeatInstruction)
    def visit(self, node):
        pass

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
