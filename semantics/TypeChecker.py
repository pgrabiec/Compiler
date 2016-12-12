import AST
from semantics.ScopeManager import ScopeManager


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)


class TypeChecker(NodeVisitor):
    def __init__(self):
        super().__init__()
        self.ttype = {}
        self.in_loop = False  # For detecting errors with break; and continue;
        self.return_statement_occurred = False  # For detecting missing return statement
        self.init_ttype()
        self.scope_manager = ScopeManager()
        self.scope_manager.push_scope("GLOBAL SCOPE")
        self.errors = []

    def error(self, node, description):
        self.errors.append("Line %d: %s" % (node.lineno, description))

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
            self.ttype[operator]['string', 'string'] = 'int'

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

    def visit_list(self, l):
        for item in l:
            self.visit(item)

    def visit_Program(self, node):
        self.visit(node.segments)

    def visit_Segments(self, node):
        for segment in node.segments:
            self.visit(segment)

    def visit_Segment(self, node):
        self.visit(node.content)

    def visit_Declaration(self, node):
        type = node.variable_type
        inits = node.inits.inits
        for init in inits:
            identifier = init.identifier
            expression = self.visit(init.expression)
            if self.scope_manager.seek_symbol(identifier) is None:  # No symbol in the scope
                self.scope_manager.add_scope_symbol(identifier, AST.Variable(init.lineno, identifier, type))  # add symbol
            else:  # Symbol already present in scope
                self.error(init, "Declaration: id \'%s\' is already defined" % identifier)
            try:  # Verify initialization value
                self.ttype["="][type, expression]
            except KeyError:  # types mismatch
                self.error(init, "Declaration: attempt to initialize \'%s\' variable \'%s\' with \'%s\' value" %
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
                self.ttype["="][var_type, expression]
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

    # function mapping in the self.scope_manager:
    # "fun <fun_id>": (<ret_type>, [<Variable(id, type)>, ...])
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
            given_arg = self.visit(given_args[i])  # visit(expression)
            spec_arg = spec_args[i]  # variable
            try:
                self.ttype["="][spec_arg.type, given_arg]
                self.scope_manager.add_scope_symbol(spec_arg.identifier, spec_arg)
            except KeyError:
                self.error(node, "Function Call: argument no. %d type \'%s\' passed to %s is not compliant"
                                 " with the specified arg type \'%s\'" % (i, given_arg, identifier, spec_arg.type))
        return return_type

    # function return type mapping in the self.scope_manager
    # "fun return_type" : <ret_type>
    # meaning that we are inside declaration of a function and it's specified return type is <ret_type>
    def visit_ReturnInstruction(self, node):
        self.return_statement_occurred = True
        ret_declared = self.scope_manager.seek_symbol("fun return_type")
        if ret_declared is None:
            self.error(node, "Return: not in function declaration")
        ret_returning = self.visit(node.expression)
        try:
            self.ttype["="][ret_returning, ret_declared]
        except KeyError:
            self.error(node, "Return: returning incompatible expression type \'%s\' while specified \'%s\'" %
                       (ret_returning, ret_declared))

    def visit_ExpressionList(self, node):
        for expression in node.expressions:
            self.visit(expression)

    def visit_FunctionDefinition(self, node):
        identifier = node.identifier
        return_type = node.type
        arguments = node.arguments.arguments
        instructions = node.instructions.instructions.segments

        arguments_variable_list = []
        for arg in arguments:
            variable = AST.Variable(arg.lineno, arg.argument_identifier, arg.argument_type);
            arguments_variable_list.append(
                variable
            )

        self.scope_manager.add_scope_symbol("fun %s" % identifier, (return_type, arguments_variable_list))

        self.scope_manager.push_scope("function %s" % identifier)
        self.scope_manager.add_scope_symbol("fun return_type", return_type)
        for variable in arguments_variable_list:
            self.scope_manager.add_scope_symbol(variable.identifier, variable)
        self.return_statement_occurred = False

        for instr in instructions:
            self.visit(instr)

        if not self.return_statement_occurred:
            self.error(node, "Function Definition: missing return statement")
        self.scope_manager.pop_scope()

    # def visit_ArgumentsList(self, node): pass

    # def visit_Argument(self, node): pass

    def visit_Identifier(self, node):
        variable = self.scope_manager.seek_symbol(node.identifier)
        if variable is None:
            self.error(node, "Referencing undeclared identifier %s" % node.identifier)
            return
        return variable.type
