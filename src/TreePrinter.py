from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


def printWithIndent(indent, value):
    print(indent*"| " + value)


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)
        self.instruction.printTree(indent)

    @addToClass(AST.Instruction)
    def printTree(self, indent=0):
        self.instruction.printTree(indent)

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        self.instructions.printTree(indent)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        printWithIndent(indent, "IF")
        self.condition.printTree(indent+1)
        printWithIndent(indent, "THEN")
        self.then_instr.printTree(indent+1)
        if self.else_instr is not None:
            printWithIndent(indent, "ELSE")
            self.else_instr.printTree(indent+1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        printWithIndent(indent, self.__class__.__name__.upper())

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        printWithIndent(indent, self.__class__.__name__.upper())

    @addToClass(AST.Type)
    def printTree(self, indent=0):
        if self._type.__class__ == str:
            printWithIndent(indent, self._type)
        else:
            self._type.printTree(indent)

    @addToClass(AST.Number)
    def printTree(self, indent=0):
        printWithIndent(indent, str(self.value))

    @addToClass(AST.Expr)
    def printTree(self, indent=0):
        self.expression.printTree(indent)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        if self.operator == "=":
            printWithIndent(indent, "=")
        else:
            self.operator.printTree(indent)
        self.variable.printTree(indent+1)
        self.expression.printTree(indent+1)

    @addToClass(AST.CalcAssign)
    def printTree(self, indent=0):
        printWithIndent(indent, str(self.operator))

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        if self.index1 is None and self.index2 is None:
            printWithIndent(indent, self.name)
        else:
            printWithIndent(indent, "REF")
            printWithIndent(indent + 1, self.name)
            printWithIndent(indent + 1, str(self.index1))
            if self.index2 is not None:
                printWithIndent(indent + 1, str(self.index2))

    @addToClass(AST.Comparator)
    def printTree(self, indent=0):
        printWithIndent(indent, str(self.comparator))

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        self.comparator.printTree(indent)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
        # fill in the body
