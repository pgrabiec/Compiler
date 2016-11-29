import AST
from semantics.ScopeManager import ScopeManager


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

                    # simpler version of generic_visit, not so general
                    # def generic_visit(self, node):
                    #    for child in node.children:
                    #        self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.ttype = {}
        self.in_loop = False  # For detecting errors with break; and continue;
        self.return_statement_occurred = False  # For detecting missing return statement
        self.init_ttype()
        self.scope_manager = ScopeManager()
        self.scope_manager.push_scope("GLOBAL SCOPE")

    def error(self, node, description):  # TODO
        pass

    def init_ttype(self):
        for operator in '+-*/':  # c
            self.ttype[operator] = {
                ('int', 'int'): 'int',
                ('int', 'float'): 'float',
                ('float', 'int'): 'float',
                ('float', 'float'): 'float'
            }
        self.ttype['+']['string', 'string'] = 'string'
        self.ttype['*']['string', 'int'] = 'int'

        for operator in ('==', '!=', '<', '<=', '>', '>='):  # ['<', '>', '<=', '>=', '==', '!=']:
            self.ttype[operator] = {
                ('int', 'int'): 'int',
                ('int', 'float'): 'int',
                ('float', 'int'): 'int',
                ('float', 'float'): 'int',
            }
        for operator in ('==', '!='):
            self.ttype[operator] = {
                ('string', 'string'): 'int'
            }

        for operator in ['%', '<<', '>>', '|', '&', '^']:
            self.ttype[operator] = {
                ('int', 'int'): 'int'
            }

        self.ttype['='] = {
            ('int', 'int'): 'int',
            ('float', 'float'): 'float',
            ('float', 'int'): 'float',
            ('int', 'float'): 'float',
            ('string', 'string'): 'string'
        }

    def visit_Program(self, node):
        self.visit(node.segments)

    def visit_Segments(self, node):
        for segment in node.segments:
            self.visit(segment)

    def visit_Segment(self, node):
        self.visit(node.content)

    def visit_Declaration(self, node):
        type = node.variable_type
        inits = node.inits
        for init in inits:
            identifier = init.identifier
            expression = self.visit(init.expression)
            if self.scope_manager.seek_symbol(identifier) is None:  # No symbol in the scope
                self.scope_manager.add_scope_symbol(identifier, AST.Variable(init.line, identifier, type))  # add symbol
            else:  # Symbol already present in scope
                self.error(init.line, "Declaration: id \'%s\' is already defined" % identifier)
            try:  # Verify initialization value
                if self.ttype["="][type, expression] != type:
                    raise KeyError  # return value type is not compatible with 'type'
            except KeyError:  # types mismatch
                self.error(init.line, "Declaration: attempt to initialize \'%s\' variable \'%s\' with \'%s\' value" %
                           (type, identifier, expression))

    # def visit_Inits(self, node): pass

    # def visit_Init(self, node): pass

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_PrintInstruction(self, node):
        self.visit(node.args)

    def visit_LabeledInstruction(self, node):
        self.visit(node.instruction)

    def visit_Assignment(self, node):
        identifier = node.variable.identifier
        expression = self.visit(node.expression)
        variable = self.scope_manager.seek_symbol(identifier)
        if variable is None:
            self.error(node, "Assignment: variable \'%s\' undeclared" % identifier)
        else:
            var_type = variable.type
            try:
                if self.ttype["="][var_type, expression] != var_type:
                    raise KeyError
            except KeyError:
                self.error(node, "Assignment: cannot assign value of type \'%s\' to variable \'%s\' type \'%s\'" %
                           (expression, identifier, var_type))

    def visit_ChoiceInstruction(self, node):
        self.visit(node.condition)
        self.visit(node.instruction_true)
        if node.instruction_false is not None:
            self.visit(node.instruction_false)

    def visit_WhileInstruction(self, node):
        self.in_loop = True
        self.visit(node.condition)
        self.visit(node.instruction)
        self.in_loop = False

    def visit_RepeatInstruction(self, node):
        self.in_loop = True
        self.visit(node.instructions)
        self.visit(node.condition)
        self.in_loop = False

    def visit_BreakInstruction(self, node):
        if not self.in_loop:
            self.error(node, "Break: break instruction not inside a loop")

    def visit_ContinueInstruction(self, node):
        if not self.in_loop:
            self.error(node, "Continue: continue instruction not inside a loop")

    def visit_CompoundInstruction(self, node):
        self.visit(node.instructions)

    def visit_CompoundSegments(self, node):
        for segment in node.segments:
            self.visit(segment)

    def visit_CompoundSegment(self, node):
        self.visit(node.content)

    def visit_Condition(self, node):
        self.visit(node.expression)

    def visit_Const(self, node):
        return self.visit(node.value)

    def visit_Integer(self, node):
        return "int"

    def visit_Float(self, node):
        return "float"

    def visit_String(self, node):
        return "string"

    def visit_BinExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op
        try:
            return self.ttype[op][left, right]
        except KeyError:
            self.error(node, "Binary Expression: cannot apply \'%s\' to \'%s\' and \'%s\'" % (op, left, right))

    # TODO
    # ["fun <fun_id>": (<ret_type>, [<Variable(id, type)>, ...])
    def visit_FunctionCallExpression(self, node):
        identifier = node.identifier
        given_args = node.arguments.expressions
        fun_spec_tuple = self.scope_manager.seek_symbol("fun %s" % identifier)
        if fun_spec_tuple is None:
            self.error(node, "Function Call: no function declared with id \'%s\'" % identifier)
            self.visit(node.arguments)
            return
        return_type, spec_args = fun_spec_tuple
        if len(given_args) != len(spec_args):
            self.error(node, "Function Call: supplied number of arguments not equal to %d" % len(spec_args))
            for arg in given_args:
                self.visit(arg)
            if len(given_args) < len(spec_args):
                return
        for i in range(0, len(spec_args)):
            given_arg = given_args[i]
            spec_arg = spec_args[i]
            if

    def visit_ReturnInstruction(self, node):
        pass

    def visit_ExpressionList(self, node):
        pass

    def visit_FunctionDefinition(self, node):
        pass

    def visit_ArgumentsList(self, node):
        pass

    def visit_Argument(self, node):
        pass

    def visit_VariableReference(self, node):
        pass
