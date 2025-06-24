from compiler.ast_nodes import *

def analyze(ast):
    symbols = {}
    semantic_check_stmt_list(ast.statements, symbols)
    return symbols

def semantic_check_stmt_list(statements, symbols):
    for stmt in statements:
        semantic_check_stmt(stmt, symbols)

def semantic_check_stmt(stmt, symbols):
    if isinstance(stmt, LetStmt):
        value = eval_expr(stmt.expr, symbols)
        symbols[stmt.name] = value

    elif isinstance(stmt, ArrayDecl):
        evaluated_elements = [eval_expr(el, symbols) for el in stmt.elements]
        symbols[stmt.name] = evaluated_elements

    elif isinstance(stmt, PrintStmt):
        eval_expr(stmt.expr, symbols)

    elif isinstance(stmt, IfStmt):
        cond_val = eval_expr(stmt.condition, symbols)
        if cond_val:
            semantic_check_stmt_list(stmt.then_branch, symbols)
        elif stmt.else_branch:
            semantic_check_stmt_list(stmt.else_branch, symbols)

    elif isinstance(stmt, WhileStmt):
        cond_val = eval_expr(stmt.condition, symbols)
        if cond_val:
            semantic_check_stmt_list(stmt.body, symbols)

    elif isinstance(stmt, ForStmt):
        semantic_check_stmt(stmt.init, symbols)
        cond_val = eval_expr(stmt.condition, symbols)
        if cond_val:
            semantic_check_stmt_list(stmt.body, symbols)
            semantic_check_stmt(stmt.increment, symbols)

    elif isinstance(stmt, ConditionStmt):
        eval_expr(stmt.expr, symbols)

    elif isinstance(stmt, BreakStmt) or isinstance(stmt, ContinueStmt):
        pass

    elif isinstance(stmt, ReturnStmt):
        eval_expr(stmt.expr, symbols)

    else:
        raise RuntimeError(f"Unknown statement type: {type(stmt)}")

def eval_expr(expr, symbols):
    if expr is None:
        raise RuntimeError("Expression is None — parser likely failed to construct an AST node")

    if isinstance(expr, Num):
        return expr.value

    elif isinstance(expr, Str):
        return expr.value

    elif isinstance(expr, Var):
        if expr.name in symbols:
            return symbols[expr.name]
        else:
            raise RuntimeError(f"Undefined variable: {expr.name}")

    elif isinstance(expr, ArrayAccess):
        if expr.name not in symbols:
            raise RuntimeError(f"Undefined array: {expr.name}")
        array = symbols[expr.name]
        index = eval_expr(expr.index, symbols)
        if not isinstance(array, list):
            raise RuntimeError(f"{expr.name} is not an array")
        if not isinstance(index, int):
            raise RuntimeError(f"Index must be an integer, got {type(index).__name__}")
        if index < 0 or index >= len(array):
            raise RuntimeError(f"Index {index} out of bounds for array '{expr.name}'")
        return array[index]

    elif isinstance(expr, BinOp):
        left = eval_expr(expr.left, symbols)
        right = eval_expr(expr.right, symbols)
        return eval_binop(left, expr.op, right)

    else:
        raise RuntimeError(f"Unknown expression type: {type(expr)}")

def eval_binop(left, op, right):
    if op == '+': return left + right
    elif op == '-': return left - right
    elif op == '*': return left * right
    elif op == '/':
        if right == 0:
            raise RuntimeError("Division by zero")
        return left / right
    elif op == '<': return int(left < right)
    elif op == '>': return int(left > right)
    elif op == '<=': return int(left <= right)
    elif op == '>=': return int(left >= right)
    elif op == '==': return int(left == right)
    elif op == '!=': return int(left != right)
    else:
        raise RuntimeError(f"Unsupported operator: {op}")
