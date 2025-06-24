# Abstract Syntax Tree (AST) Node Definitions

# Program Root
class Program:
    def __init__(self, statements):
        self.statements = statements

# Statements
class LetStmt:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class ConditionStmt:
    """Used for condition-only lines (e.g., 'i chota hai 5 ardhaviram') inside loops"""
    def __init__(self, expr):
        self.expr = expr

class ArrayDecl:
    def __init__(self, name, elements):
        self.name = name
        self.elements = elements

class PrintStmt:
    def __init__(self, expr):
        self.expr = expr

class IfStmt:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStmt:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForStmt:
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

class BreakStmt:
    pass

class ContinueStmt:
    pass

class ReturnStmt:
    def __init__(self, expr):
        self.expr = expr

# Expressions
class Num:
    def __init__(self, value):
        self.value = value

class Str:
    def __init__(self, value):
        self.value = value

class Var:
    def __init__(self, name):
        self.name = name

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class ArrayAccess:
    def __init__(self, name, index):
        self.name = name
        self.index = index
