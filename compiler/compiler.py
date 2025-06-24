from compiler.ast_nodes import *

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.symbols = {}

    def interpret(self, ast):
        try:
            self.exec_stmt_list(ast.statements)
        except ReturnException as e:
            print(f"Returned: {e.value}")

    def exec_stmt_list(self, stmts):
        for stmt in stmts:
            self.exec_stmt(stmt)

    def exec_stmt(self, stmt):
        if isinstance(stmt, LetStmt):
            val = self.eval_expr(stmt.expr)
            self.symbols[stmt.name] = val

        elif isinstance(stmt, ArrayDecl):
            values = [self.eval_expr(el) for el in stmt.elements]
            self.symbols[stmt.name] = values

        elif isinstance(stmt, PrintStmt):
            val = self.eval_expr(stmt.expr)
            print(val)

        elif isinstance(stmt, IfStmt):
            cond = self.eval_expr(stmt.condition)
            if cond:
                self.exec_stmt_list(stmt.then_branch)
            elif stmt.else_branch is not None:
                self.exec_stmt_list(stmt.else_branch)

        elif isinstance(stmt, WhileStmt):
            try:
                while self.eval_expr(stmt.condition):
                    try:
                        self.exec_stmt_list(stmt.body)
                    except ContinueException:
                        continue
            except BreakException:
                pass

        elif isinstance(stmt, ForStmt):
            try:
                self.exec_stmt(stmt.init)
                while self.eval_expr(stmt.condition):
                    try:
                        self.exec_stmt_list(stmt.body)
                    except ContinueException:
                        pass
                    self.exec_stmt(stmt.increment)
            except BreakException:
                pass

        elif isinstance(stmt, ConditionStmt):
            # Just evaluate the expression to allow for-loop-style condition
            self.eval_expr(stmt.expr)

        elif isinstance(stmt, BreakStmt):
            raise BreakException()

        elif isinstance(stmt, ContinueStmt):
            raise ContinueException()

        elif isinstance(stmt, ReturnStmt):
            value = self.eval_expr(stmt.expr)
            raise ReturnException(value)

        else:
            raise RuntimeError(f"Unknown statement type: {type(stmt).__name__}")

    def eval_expr(self, expr):
        if isinstance(expr, Num):
            return expr.value

        elif isinstance(expr, Str):
            return expr.value

        elif isinstance(expr, Var):
            if expr.name in self.symbols:
                return self.symbols[expr.name]
            else:
                raise RuntimeError(f"Undefined variable: {expr.name}")

        elif isinstance(expr, ArrayAccess):
            if expr.name not in self.symbols:
                raise RuntimeError(f"Undefined array: {expr.name}")
            arr = self.symbols[expr.name]
            index = self.eval_expr(expr.index)
            if not isinstance(arr, list):
                raise RuntimeError(f"{expr.name} is not an array")
            if not (0 <= index < len(arr)):
                raise RuntimeError(f"Index {index} out of bounds for array '{expr.name}'")
            return arr[index]

        elif isinstance(expr, BinOp):
            left = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            return self.eval_binop(left, expr.op, right)

        else:
            raise RuntimeError(f"Unknown expression type: {type(expr).__name__}")

    def eval_binop(self, left, op, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        elif op == '<':
            return int(left < right)
        elif op == '>':
            return int(left > right)
        elif op == '<=':
            return int(left <= right)
        elif op == '>=':
            return int(left >= right)
        elif op == '==':
            return int(left == right)
        elif op == '!=':
            return int(left != right)
        else:
            raise RuntimeError(f"Unsupported operator: {op}")
