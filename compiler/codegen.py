from compiler.ast_nodes import *

def generate_code(ast):
    code_lines = []
    for stmt in ast.statements:
        code_lines.extend(generate_stmt_code(stmt, indent=0))
    return "\n".join(code_lines)

def generate_stmt_code(stmt, indent=0):
    indent_str = "    " * indent
    lines = []

    if isinstance(stmt, LetStmt):
        lines.append(f"{indent_str}{stmt.name} = {generate_expr_code(stmt.expr)}")

    elif isinstance(stmt, ArrayDecl):
        elements_code = ", ".join(generate_expr_code(el) for el in stmt.elements)
        lines.append(f"{indent_str}{stmt.name} = [{elements_code}]")

    elif isinstance(stmt, PrintStmt):
        lines.append(f"{indent_str}print({generate_expr_code(stmt.expr)})")

    elif isinstance(stmt, IfStmt):
        lines.append(f"{indent_str}if {generate_expr_code(stmt.condition)}:")
        for s in stmt.then_branch:
            lines.extend(generate_stmt_code(s, indent + 1))
        if stmt.else_branch:
            lines.append(f"{indent_str}else:")
            for s in stmt.else_branch:
                lines.extend(generate_stmt_code(s, indent + 1))

    elif isinstance(stmt, WhileStmt):
        lines.append(f"{indent_str}while {generate_expr_code(stmt.condition)}:")
        for s in stmt.body:
            lines.extend(generate_stmt_code(s, indent + 1))

    elif isinstance(stmt, ForStmt):
        lines.extend(generate_stmt_code(stmt.init, indent))
        lines.append(f"{indent_str}while {generate_expr_code(stmt.condition)}:")
        for s in stmt.body:
            lines.extend(generate_stmt_code(s, indent + 1))
        lines.extend(generate_stmt_code(stmt.increment, indent + 1))

    elif isinstance(stmt, ConditionStmt):
        # Comment out pure conditions (used inside for-loops)
        lines.append(f"{indent_str}# Condition: {generate_expr_code(stmt.expr)}")

    elif isinstance(stmt, BreakStmt):
        lines.append(f"{indent_str}break")

    elif isinstance(stmt, ContinueStmt):
        lines.append(f"{indent_str}continue")

    elif isinstance(stmt, ReturnStmt):
        lines.append(f"{indent_str}return {generate_expr_code(stmt.expr)}")

    else:
        raise RuntimeError(f"Unknown statement type: {type(stmt)}")

    return lines

def generate_expr_code(expr):
    if isinstance(expr, Num):
        return str(expr.value)
    elif isinstance(expr, Str):
        return repr(expr.value)
    elif isinstance(expr, Var):
        return expr.name
    elif isinstance(expr, ArrayAccess):
        return f"{expr.name}[{generate_expr_code(expr.index)}]"
    elif isinstance(expr, BinOp):
        left = generate_expr_code(expr.left)
        right = generate_expr_code(expr.right)
        return f"({left} {expr.op} {right})"
    else:
        raise RuntimeError(f"Unknown expression type: {type(expr)}")

def write_python_file(code: str, output_path="output.py"):
    with open(output_path, "w") as f:
        f.write(code)
