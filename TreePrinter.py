import AST as AST



def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    # TODO - PG
    @addToClass(AST.Program)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.Segments)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.Segment)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.Declarations)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.Declaration)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.Inits)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.Init)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.Instructions)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.ReturnInstruction)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.BreakInstruction)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.ContinueInstruction)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.ExpressionInstruction)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.PrintInstruction)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.LabeledInstruction)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.Assignment)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.ChoiceInstruction)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.WhileInstruction)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.RepeatInstruction)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.CompoundInstruction)
    def printTree(self, indent):
        pass

    # TODO - PG
    @addToClass(AST.CompoundSegments)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.CompoundSegment)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.Const)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.Integer)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.Float)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.String)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.Condition)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.Variable)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.BinExpr)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.BracketExpression)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.FunctionCallExpression)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.ExpressionList)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.FunctionDefinitions)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.FunctionDefinition)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.ArgumentsList)
    def printTree(self, indent):
        pass

    # TODO - WB
    @addToClass(AST.Argument)
    def printTree(self, indent):
        pass
