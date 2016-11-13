import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.BinExpr)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Const)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Integer)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Float)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.String)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Variable)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Program)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Declarations)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Init)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Inits)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Init)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.InstructionsOpt)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Instructions)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Instruction)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.PrintInstr)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.LabeledInstr)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.Assignment)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.ChoiceInstr)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - PG
    @addToClass(AST.WhileInstr)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.RepeatInstr)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.ReturnInstr)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.ContinueInstr)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.BreakInstr)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.CompoundInstr)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.Condition)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.Expression)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.ExprListOrEmpty)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.ExprList)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.FundefsOpt)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.Fundefs)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.Fundef)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.ArgsListOrEmpty)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.ArgsList)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)

    # TODO - WB
    @addToClass(AST.Arg)
    def printTree(self):
        raise Exception("Print tree not implemented in class " + self.__class__.__name__)
