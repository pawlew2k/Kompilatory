from dataclasses import dataclass
from typing import Any



class Node(object):
    def __init__(self):
        self.lineno = 0


    def accept(self, visitor):
        return visitor.visit(self)


@dataclass
class Program(Node):
    instructions: Any = None


@dataclass
class Instructions(Node):
    instructions: Any


@dataclass
class Instruction(Node):
    instruction: Any


@dataclass
class Block(Node):
    instructions: Any


@dataclass
class If(Node):
    condition: Any
    then_instr: Any
    else_instr: Any = None


@dataclass
class For(Node):
    variable: Any
    range: Any
    instruction: Any


@dataclass
class Range(Node):
    from_value: Any
    to_value: Any


@dataclass
class While(Node):
    condition: Any
    instruction: Any


@dataclass
class Break(Node):
    pass


@dataclass
class Continue(Node):
    pass


@dataclass
class Return(Node):
    value: Any = None


@dataclass
class Print(Node):
    expressions: Any


@dataclass
class Expr(Node):
    expression: Any


@dataclass
class Expressions(Node):
    expressions: Any


@dataclass
class Singleton(Node):
    singleton: Any


@dataclass
class Vector(Node):
    expressions: Any = None


@dataclass
class Assign(Node):
    operator: Any
    variable: Any
    expression: Any


@dataclass
class CalcAssign(Node):
    operator: Any


@dataclass
class Variable(Node):
    name: Any
    index1: Any = None
    index2: Any = None


@dataclass
class Comparator(Node):
    comparator: Any


@dataclass
class Condition(Node):
    comparator: Any
    left: Any
    right: Any


@dataclass
class BinOp(Node):
    operator: Any
    left: Any
    right: Any


@dataclass
class MatrixOp(Node):
    operator: Any
    left: Any
    right: Any


@dataclass
class UMinus(Node):
    expression: Any


@dataclass
class Transpose(Node):
    expression: Any


@dataclass
class MatrixFunc(Node):
    func: Any
    dim1: Any
    dim2: Any = None


@dataclass
class Function(Node):
    func: Any


@dataclass
class Error(Node):
    pass
