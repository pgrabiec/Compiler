import sys
import operator

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
        self.operators = {}
        self.init_operators()

    def init_operators(self):
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.floordiv,
            '%': operator.mod,
            '==': operator.eq,
            '!=': operator.ne,
            '>': operator.gt,
            '<': operator.lt,
            '>=': operator.ge,
            '<=': operator.le,
            '<<': operator.lshift,
            '>>': operator.rshift,
            '^': operator.pow,
            '&': operator.and_,
            '|': operator.or_,
            '&&': lambda x, y: x and y,
            '||': lambda x, y: x or y
        }

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        for segment in node.segments:
            self.visit(segment)

    # Mapping for identifier:
    # key: <identifier>
    # value: <value>
    @when(AST.Declaration)
    def visit(self, node):
        inits = node.inits
        mem = self.mem
        for init in inits:
            identifier = init.identifier
            expression = self.visit(init.expression)
            mem.declare(identifier, expression)

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
        expression = self.visit(node.expression)
        self.mem.update_value(identifier, expression)
        return expression

    @when(AST.ChoiceInstruction)
    def visit(self, node):
        instruction_true = node.instruction_true
        instruction_false = node.instruction_false
        if self.visit(node.condition):
            self.visit(instruction_true)
        else:
            if instruction_false is not None:
                self.visit(instruction_false)

    @when(AST.WhileInstruction)
    def visit(self, node):
        mem = self.mem
        while self.visit(node.condition):
            mem.push_loop_scope()
            try:
                self.visit(node.instruction)
                mem.pop_current_loop_scopes()
            except BreakException:
                mem.pop_current_loop_scopes()
                break
            except ContinueException:
                mem.pop_current_loop_scopes()

    @when(AST.RepeatInstruction)
    def visit(self, node):
        mem = self.mem
        while True:
            mem.push_loop_scope()
            try:
                self.visit(node.instruction)
                mem.pop_current_loop_scopes()
            except ContinueException:
                mem.pop_current_loop_scopes()
            except BreakException:
                mem.pop_current_loop_scopes()
                break
            if self.visit(node.condition):
                break

    @when(AST.ReturnInstruction)
    def visit(self, node):
        raise ReturnValueException(self.visit(node.expression))

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(AST.CompoundInstructions)
    def visit(self, node):
        self.mem.push_compound_instructions_scope()
        for instruction in node.instructions:
            self.visit(instruction)
        self.mem.pop_compound_instructions_scope()

    @when(AST.Const)
    def visit(self, node):
        return self.visit(node.value)

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value.strip('"'))

    @when(AST.Identifier)
    def visit(self, node):
        identifier = node.identifier
        return self.mem.get_value(identifier)

    # Mapping for function declaration:
    # key: "fun <identifier>"
    # value: tuple (<arguments>, <instructions>)
    @when(AST.FunctionCallExpression)
    def visit(self, node):
        mem = self.mem
        identifier = node.identifier
        expression_list = node.arguments
        argument_values_given = []
        # Evaluate argument values for function call
        for expression in expression_list:
            argument_values_given.append(self.visit(expression))
        # Get function declaration
        arguments_specified, instructions = mem.get_value("fun %s" % identifier)
        # Push arguments to function scope
        mem.push_function_scope()
        i = 0
        while i < len(arguments_specified):
            argument_specified = arguments_specified[i]
            argument_value = argument_values_given[i]
            arg_identifier = argument_specified.argument_identifier
            mem.declare(arg_identifier, argument_value)
            i += 1
        # Execute function
        try:
            for instruction in instructions.instructions:
                self.visit(instruction)
            raise Exception("Did not return any value from function: line " + str(instruction.lineno))
        except ReturnValueException as exception:
            mem.pop_function_scope()
            return exception.value

    @when(AST.BinExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.operators[node.op]
        return op(left, right)

    @when(AST.FunctionDefinition)
    def visit(self, node):
        identifier = node.identifier
        arguments = node.arguments
        instructions = node.instructions
        self.mem.declare(
            "fun %s" % identifier,
            (arguments, instructions)
        )
