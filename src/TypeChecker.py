import AST
from SymbolTable import *
from OperationTypes import ttype


class NodeVisitor(object):

    def __init__(self):
        # na true w każdym błędzie przed PRINT
        self.error = False

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


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.actual_scope = SymbolTable(None, 'main')
        self.loop_depth = 0

    def visit_Program(self, node):
        if node.instructions is not None:
            self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_Instruction(self, node):
        self.visit(node.instruction)

    def visit_Block(self, node):
        self.actual_scope = self.actual_scope.pushScope("block")
        self.visit(node.instructions)
        self.actual_scope = self.actual_scope.popScope()

    def visit_If(self, node):
        self.actual_scope = self.actual_scope.pushScope('if')
        self.visit(node.condition)
        self.visit(node.then_instr)
        self.actual_scope = self.actual_scope.popScope()
        if node.else_instr is not None:
            self.actual_scope = self.actual_scope.pushScope('else')
            self.visit(node.else_instr)
            self.actual_scope = self.actual_scope.popScope()

    def visit_For(self, node):
        self.actual_scope = self.actual_scope.pushScope('for')
        self.loop_depth += 1
        result_type = self.visit(node.range)
        if result_type != 'unknown':
            symbol = VariableSymbol(node.variable, result_type)
            self.actual_scope.put(node.variable, symbol)
        self.visit(node.instruction)
        self.loop_depth -= 1
        self.actual_scope = self.actual_scope.popScope()

    def visit_Range(self, node):
        left = self.visit(node.from_value)
        right = self.visit(node.to_value)
        if left != 'int' or right != 'int':
            print("Line {}: Incompatible range types {} and {} for instruction for".format(node.lineno, left, right))
            return 'unknown'
        return 'int'

    def visit_While(self, node):
        self.actual_scope = self.actual_scope.pushScope('while')
        self.loop_depth += 1
        self.visit(node.condition)
        self.visit(node.instruction)
        self.loop_depth -= 1
        self.actual_scope = self.actual_scope.popScope()

    def visit_Break(self, node):
        if self.loop_depth == 0:
            print("Line {}: Break outside the loop".format(node.lineno))

    def visit_Continue(self, node):
        if self.loop_depth == 0:
            print("Line {}: Continue outside the loop".format(node.lineno))

    def visit_Return(self, node):
        if node.value is not None:
            result_type = self.visit(node.value)
            if result_type == 'unknown':
                print("Line {}: Cannot return unknown type".format(node.lineno))

    def visit_Print(self, node): #pozbyć się wężyka
        for expression in node.expressions.expressions:
            result_type = self.visit(expression)
            if result_type == 'unknown':
                print("Line {}: Cannot print unknown type".format(node.lineno))

    def visit_Expr(self, node):
        return self.visit(node.expression)

    def visit_Expressions(self, node):
        for expression in node.expressions:
            self.visit(expression)

    def visit_Singleton(self, node):
        if type(node.singleton) == str:
            return 'str'
        elif type(node.singleton) == int:
            return 'int'
        elif type(node.singleton) == float:
            return 'float'
        return 'unknown'

    def visit_Vector(self, node): # przekaż wart do assign
        # print("IN")
        # print(node)
        # print(node.expressions.expressions[0].expression)
        # print(len(node.expressions.expressions))
        expressions = node.expressions.expressions if node.expressions is not None else []
        types_inside_vector = set()
        for expr in expressions:
            result_type = self.visit(expr)
            result_type = 'float' if result_type == 'int' else result_type
            types_inside_vector.add(result_type)
        flag = False
        if len(types_inside_vector) > 1:
            if 'vector' in types_inside_vector:
                print("Line {}: Matrix should contain one type, but contains {}".format(node.lineno, types_inside_vector))
            else:
                print(
                    "Line {}: Vector should contain one type, but contains {}".format(node.lineno, types_inside_vector))
            flag = True
        if 'matrix' in types_inside_vector:
            print("Line {}: Matrix must be 2 dimensional".format(node.lineno))
            flag = True
        if 'str' in types_inside_vector:
            if 'vector' in types_inside_vector:
                print("Line {}: Matrix cannot have str type inside".format(node.lineno))
            else:
                print("Line {}: Vector cannot have str type inside".format(node.lineno))
            flag = True
        if 'unknown' in types_inside_vector:
            if 'vector' in types_inside_vector:
                print("Line {}: Matrix cannot have unknown type inside".format(node.lineno))
            else:
                print("Line {}: Vector cannot have unknown type inside".format(node.lineno))
            flag = True
        if flag:
            return 'unknown'
        if 'vector' in types_inside_vector:
            vector_len = set()
            for node in node.expressions.expressions:
                vector_len.add(len(node.expression.expressions.expressions))
                if len(vector_len) > 1:
                    print("Line {}: Matrix should have vectors equal sizes, but has {}".format(node.lineno, vector_len))
                    return 'unknown'
            return 'matrix'
        return 'vector'

    def visit_Assign(self, node): # matrix #referencje!!!!
        if node.operator == "=":
            right = self.visit(node.expression)
            if right == 'unknown':
                print("Line {}: Cannot assign unknown type to variable".format(node.lineno))
            elif right == 'vector':
                # -------------------------------------------------------------------------------------
                # Jak wyciągnąć vector type i vector length
                symbol = VariableSymbol(node.variable.name, vector_type, dim1=vector_length)
                self.actual_scope.put(node.variable.name, symbol)
            elif right == 'matrix':
                pass # zrobić matrix ---------------------------------------------------------------------
            else: # singleton
                symbol = VariableSymbol(node.variable.name, right)
                self.actual_scope.put(node.variable.name, symbol)

        else: # calc_assign
            operator = self.visit(node.operator)
            if self.visit(node.variable) is None:
                print("Line {}: Variable {} not defined".format(node.lineno, node.variable.name))
                return 'unknown'
            left = self.visit(node.variable)
            right = self.visit(node.expression)
            if right == 'unknown':
                print("Line {}: Cannot assign unknown type to variable".format(node.lineno))
            elif ttype[operator][left][right] == 'unknown':
                print("Line {}: Incompatible assign operation types {} and {} for operator {}".format(node.lineno, left, right, operator))

    def visit_CalcAssign(self, node):
        return node.operator

    def visit_Variable(self, node):
        if node.name not in self.actual_scope.symbols.keys():
            print("Line {}: Reference to not defined object {}".format(node.lineno, node.name))
            return 'unknown'
        if self.actual_scope.symbols[node.name].dim2 is not None:
            return 'matrix'
        elif self.actual_scope.symbols[node.name].dim1 is not None:
            return 'vector'
        else:
            singleton_type = self.actual_scope.symbols[node.name].type
            return singleton_type

    def visit_Comparator(self, node):
        return node.comparator

    def visit_Condition(self, node): # czy przekazać do if / while
        left = self.visit(node.left)
        right = self.visit(node.right)
        comparator = self.visit(node.comparator)
        result_type = ttype[comparator][left][right]
        if result_type == 'unknown':
            print('Line {}: Incompatible types {} and {} for operation {}'.format(node.lineno, left, right, comparator))

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        operator = node.operator

        result_type = ttype[operator][left][right]
        if result_type == 'unknown':
            print('Line {}: Incompatible types {} and {} for operation {}'.format(node.lineno, left, right, operator))

        return result_type

    def visit_MatrixOp(self, node):
        pass # sprawdzanie rozmiaru macierzy

    def visit_UMinus(self, node):
        expr_type = self.visit(node.expression)
        if ttype['unary'][expr_type][None] == 'unknown':
            print("Line {}: Unary minus cannot be before type {}".format(node.lineno, expr_type))
            return 'unknown'
        return ttype

    def visit_Transpose(self, node):
        result_type = self.visit(node.expression)
        if ttype['transpose'][result_type][None] == 'unknown':
            print("Line {}: Cannot transpose {} type".format(node.lineno, result_type))
            return 'unknown'
        return result_type

    def visit_MatrixFunc(self, node):
        func = self.visit(node.func)
        dim1 = node.dim1
        dim2 = node.dim2
        flag = False
        if func == 'eye':
            if dim2 is not None:
                print("Line {}: Too many arguments for function eye".format(node.lineno))
                flag = True
            if dim1 <= 0:
                print("Line {}: Dimension for function eye should be positive, but got {}".format(node.lineno, dim1))
                flag = True
            if type(dim1) != int:
                print("Line {}: Function eye takes int parameter, but got type {}".format(node.lineno, type(dim1)))
                flag = True
            if flag == False:
                return 'matrix'
        else:
            if dim2 is None: # vector
                if dim1 <= 0:
                    print("Line {}: Dimension for function eye should be positive, but got {}".format(node.lineno, dim1))
                    flag = True
                if type(dim1) != int:
                    print("Line {}: Function eye takes int parameter, but got type {}".format(node.lineno, type(dim1)))
                    flag = True
                if flag == False:
                    return 'vector'
            else: #matrix
                if dim1 <= 0 or dim2 <= 0:
                    print("Line {}: Dimension for function eye should be positive, but got {}".format(node.lineno, dim1))
                    flag = True
                if type(dim1) != int or type(dim2) != int:
                    print("Line {}: Function eye takes int parameter, but got type {}".format(node.lineno, type(dim1)))
                    flag = True
                if flag == False:
                    return 'matrix'

        return 'unknown'

    def visit_Function(self, node):
        return node.func
