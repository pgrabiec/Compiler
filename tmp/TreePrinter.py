import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

def stringify(list):
    return '\n'.join(map(str, list))

def indent(lines, amount=1, token="| "):
    padding = amount * token
    return padding + ('\n' + padding).join(str(lines).split('\n'))

class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self):
        return stringify(self.children)

    @addToClass(AST.Const)
    def printTree(self):
        return "%s : %s" % (self.value, self.name)

    @addToClass(AST.Argument)
    def printTree(self):
        return "ARG %s : %s" % (self.ID, self.type)

    @addToClass(AST.BinExpr)
    def printTree(self):
        return "BIN_EXPR %s \n%s\n%s" % (self.op, indent(self.left), indent(self.right))

    @addToClass(AST.LabeledInstruction)
    def printTree(self):
        return "LABEL %s \n%s" % (self.ID, indent(self.expression))

    @addToClass(AST.InvocationExpression)
    def printTree(self):
        return "FUNCALL %s \n%s" % (self.ID, indent(stringify(self.expression)))

    @addToClass(AST.FunctionDefinition)
    def printTree(self):
        return "FUNDEF %s -> %s\n%s\n%s" % (self.ID, self.type, indent(stringify(self.args)), indent(self.body))

    @addToClass(AST.Declaration)
    def printTree(self):
        return "DECL %s \n%s" % (self.type, indent(stringify(self.inits)))

    @addToClass(AST.PrintInstruction)
    def printTree(self):
        return "PRINT \n%s" % (indent(stringify(self.expression)))

    @addToClass(AST.Assignment)
    def printTree(self):
        return "ASSIGN %s \n%s" % (self.ID.printTree(), indent(self.expression))

    @addToClass(AST.ChoiceInstruction)
    def printTree(self):
        value = "IF \n%s\n%s" % (indent(self.condition), indent(self.instruction))
        if self.alternative is not None:
            value += "\nELSE \n%s" % (indent(self.alternative))
        return value

    @addToClass(AST.WhileInstruction)
    def printTree(self):
        return "WHILE \n%s\n%s" % (indent(self.condition), indent(self.instruction))

    @addToClass(AST.RepeatInstruction)
    def printTree(self):
        return "REPEAT \n%s\nUNTIL\n%s" % (indent(self.instruction), indent(self.condition))

    @addToClass(AST.ReturnInstruction)
    def printTree(self):
        return "RETURN \n%s" % (indent(self.expression))

    @addToClass(AST.BreakInstruction)
    def printTree(self):
        return "BREAK\n"

    @addToClass(AST.ContinueInstruction)
    def printTree(self):
        return "CONTINUE"

    @addToClass(AST.Variable)
    def printTree(self):
        return "VAR %s \n%s" % (self.ID, indent(self.value))

    @addToClass(AST.Identifier)
    def printTree(self):
        return self.name