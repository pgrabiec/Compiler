from collections import namedtuple

import AST

ttype = {}

for operator in '+-*/':  # ['+', '-', '*', '/']:
    ttype[operator] = {
        ('int', 'int'): 'int',
        ('int', 'float'): 'float',
        ('float', 'int'): 'float',
        ('float', 'float'): 'float'
    }

for operator in ('==', '!=', '<', '<=', '>', '>='):  # ['<', '>', '<=', '>=', '==', '!=']:
    ttype[operator] = {
        ('int', 'int'): 'int',
        ('int', 'float'): 'int',
        ('float', 'int'): 'int',
        ('float', 'float'): 'int',
        ('string', 'string'): 'int'
    }

for operator in ['%', '<<', '>>', '|', '&', '^']:
    ttype[operator] = {
        ('int', 'int'): 'int'
    }

ttype['='] = {
    ('int', 'int'): 'int',
    ('float', 'float'): 'int',
    ('float', 'int'): 'int',
    ('string', 'string'): 'int'
}

ttype['+']['string', 'string'] = 'string'
ttype['*']['string', 'int'] = 'int'

FuncType = namedtuple('FuncType', 'args ret_type')


class SemanticError(Exception):
    def __init__(self, message, node):
        super(SemanticError, self).__init__(message)
        self.line = node.line

    def __str__(self):
        return "Line %s: %s" % (self.line, self.message)


class NodeVisitor(object):
    def visit(self, node, scope):
        method = 'visit_' + node.__class__.__name__
        #print method
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, scope)

    def generic_visit(self, node, scope):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem, scope)
        elif hasattr(node, 'children'):
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item, scope)
                elif isinstance(child, AST.Node):
                    self.visit(child, scope)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.errors = []
        self.insideLoop = False
        self.returned = False

    def visit_Integer(self, node, scope):
        return 'int'

    def visit_Float(self, node, scope):
        return 'float'

    def visit_String(self, node, scope):
        return 'string'

    def visit_Identifier(self, node, scope):
        try:
            return scope.get(node.name)
        except KeyError:
            self.errors.append(SemanticError(
                "Identifier: Using undeclared variable \"%s\"." %
                node.name, node)
            )

    def visit_Program(self, node, scope):
        if not node.top:
            if '<func>' not in scope.entries:
                scope = scope.newChild(name='<local %s>' % id(node))
        self.generic_visit(node, scope)

    def visit_FunctionDefinition(self, node, scope):
        if node.ID not in scope.entries:
            scope.put(node.ID, FuncType(
                tuple(a.type for a in node.args),
                node.type))
            local_scope = scope.newChild(name='<func %s>' % node.ID)
            for arg in node.args:
                local_scope.put(arg.ID, arg.type)
            local_scope.put('<func>', None)
            local_scope.put('?RETURN', node.type)
            self.visit(node.body, local_scope)
        else:
            self.errors.append(SemanticError(
                "Function: Redefining \"%s\" which is already defined in scope \"%s\"." %
                (node.ID, scope.name), node))
        if not self.returned:
            self.errors.append(SemanticError(
                "Function: Missing return statement in \"%s\" function returning %s." %
                (node.ID, node.type), node))
        self.returned = False

    def visit_Declaration(self, node, scope):
        for init in node.inits:
            if init.ID not in scope.entries:
                if 'func {0}'.format(init.ID) in scope.name:
                    self.errors.append(SemanticError(
                        "Declaration: Redefining \"%s\" which is already defined as function name \"%s\"." %
                        (init.ID, scope.name), init))
                scope.put(init.ID, node.type)
            else:
                self.errors.append(SemanticError(
                    "Declaration: Redefining \"%s\" which is already defined in scope \"%s\"." %
                    (init.ID, scope.name), init))
            init_type = self.visit(init.value, scope)
            if (node.type, init_type) not in ttype['=']:
                self.errors.append(SemanticError(
                    "Declaration: Invalid declaration type for \"%s\": expected %s, found %s." %
                    (init.ID, node.type, init_type), init))

    def visit_BinExpr(self, node, scope):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        op = node.op
        try:
            return ttype[op][left, right]
        except KeyError:
            self.errors.append(SemanticError(
                "BinExpr: Wrong operands for \"%s\": %s and %s." %
                (op, left, right), node))

    def visit_ChoiceInstruction(self, node, scope):
        self.visit(node.condition, scope)
        self.visit(node.instruction, scope)
        if node.alternative is not None:
            self.visit(node.alternative, scope)

    def visit_WhileInstruction(self, node, scope):
        self.visit(node.condition, scope)
        self.insideLoop = True
        self.visit(node.instruction, scope)
        self.insideLoop = False

    def visit_RepeatInstruction(self, node, scope):
        self.insideLoop = True
        self.visit(node.instruction, scope)
        self.insideLoop = False
        self.visit(node.condition, scope)

    def visit_Assignment(self, node, scope):
        left = self.visit(node.ID, scope)
        right = self.visit(node.expression, scope)
        try:
            return ttype['='][left, right]
        except KeyError:
            self.errors.append(SemanticError(
                "Assignment: Invalid assignment type for \"%s\": expected %s, found %s." %
                (node.ID, left, right), node))

    def visit_InvocationExpression(self, node, scope):
        try:
            fun_type = scope.get(node.ID)
            if len(fun_type.args) != len(node.expression):
                self.errors.append(SemanticError(
                    "Invocation: Incorrect number of arguments for \"%s\" function: expected %d, found %d." %
                    (node.ID, len(fun_type.args), len(node.expression)), node))
            for arg_type, arg in zip(fun_type.args, node.expression):
                val_type = self.visit(arg, scope)
                if (arg_type, val_type) not in ttype['=']:
                    self.errors.append(SemanticError(
                        "Invocation: Invalid argument type for \"%s\" function: expected %s, found %s." %
                        (node.ID, arg_type, val_type), arg))
            return fun_type.ret_type
        except KeyError:
            self.errors.append(SemanticError(
                "Invocation: Invoking undeclared function \"%s\"." %
                node.ID, node))

    def visit_ReturnInstruction(self, node, scope):
        self.returned = True
        value_type = self.visit(node.expression, scope)
        try:
            returned_type = scope.get('?RETURN')
            if (returned_type, value_type) not in ttype['=']:
                self.errors.append(SemanticError(
                    "Return: Invalid return statement type: expected %s, found %s." %
                    (returned_type, value_type), node))
        except KeyError:
            self.errors.append(SemanticError(
                "Return: Return statement found outside function scope", node))

    def visit_PrintInstruction(self, node, scope):
        self.visit(node.expression, scope)

    def visit_LabeledInstruction(self, node, scope):
        self.visit(node.expression, scope)

    def visit_ContinueInstruction(self, node, scope):
        if not self.insideLoop:
            self.errors.append(SemanticError(
                "Return: Continue instruction found outside loop body.", node))

    def visit_BreakInstruction(self, node, scope):
        if not self.insideLoop:
            self.errors.append(SemanticError(
                "Return: Break instruction found outside loop body.", node))
