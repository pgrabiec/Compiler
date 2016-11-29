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
        self.in_loop = False                    # For detecting errors with break; and continue;
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
            else:   # Symbol already present in scope
                self.error(init.line, "Declaration: id \'%s\' is already defined" % identifier)
            try:    # Verify initialization value
                if self.ttype["="][type, expression] != type:
                    raise KeyError  # return value type is not compatible with 'type'
            except KeyError:    # types mismatch
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
        if self.scope_manager.seek_symbol(identifier) is None:
            self.error(node, "Assignment: variable \'%s\' undeclared" % identifier)
        else: # TODO

    def visit_ChoiceInstruction(self, node):
        pass

    def visit_WhileInstruction(self, node):
        pass

    def visit_RepeatInstruction(self, node):
        pass

    def visit_ReturnInstruction(self, node):
        pass

    def visit_BreakInstruction(self, node):
        pass

    def visit_ContinueInstruction(self, node):
        pass

    def visit_CompoundInstruction(self, node):
        pass

    def visit_CompoundSegments(self, node):
        pass

    def visit_CompoundSegment(self, node):
        pass

    def visit_Condition(self, node):
        pass

    def visit_Const(self, node):
        pass

    def visit_Integer(self, node):
        pass

    def visit_Float(self, node):
        pass

    def visit_String(self, node):
        pass

    def visit_BinExpr(self, node):
        pass

    def visit_FunctionCallExpression(self, node):
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
