from compiler.ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def match(self, kind):
        if self.peek()[0] == kind:
            tok = self.tokens[self.pos]
            self.pos += 1
            return tok
        raise RuntimeError(f"Expected {kind}, got {self.peek()[0]}")

    def skip_newlines(self):
        while self.peek()[0] == 'NEWLINE':
            self.pos += 1

    def parse(self):
        self.match('SHURU')
        self.skip_newlines()
        stmts = []
        while self.peek()[0] != 'KHATAM':
            self.skip_newlines()
            if self.peek()[0] == 'KHATAM':
                break
            stmts.append(self.statement())
            self.skip_newlines()
        self.match('KHATAM')
        return Program(stmts)

    def statement(self):
        self.skip_newlines()
        kind = self.peek()[0]

        if kind == 'RAKHO':
            return self.let_statement()
        elif kind == 'SOOCHI':
            return self.array_declaration()
        elif kind == 'DIKHAO':
            return self.print_statement()
        elif kind == 'AGAR':
            return self.if_statement()
        elif kind == 'JABTAK':
            return self.while_statement()
        elif kind == 'KELIYE':
            return self.for_statement()
        elif kind == 'TODO':
            self.match('TODO')
            self.match('ARDHAVIRAM')
            return BreakStmt()
        elif kind == 'CHHODO':
            self.match('CHHODO')
            self.match('ARDHAVIRAM')
            return ContinueStmt()
        elif kind == 'WAPIS':
            self.match('WAPIS')
            expr = self.expr()
            self.match('ARDHAVIRAM')
            return ReturnStmt(expr)
        else:
            # Allow condition-style lines like: i chota hai 3 ardhaviram
            try:
                expr = self.expr()
                self.match('ARDHAVIRAM')
                return ConditionStmt(expr)
            except Exception:
                raise RuntimeError(f"Invalid statement at token {self.peek()}")

    def let_statement(self):
        self.match('RAKHO')
        name = self.match('PEHCHAN')[1]
        self.match('ASSIGN')
        expr = self.expr()
        self.match('ARDHAVIRAM')
        return LetStmt(name, expr)

    def array_declaration(self):
        self.match('SOOCHI')
        name = self.match('PEHCHAN')[1]
        self.match('ASSIGN')
        self.match('LBRACKET')
        elements = []
        if self.peek()[0] != 'RBRACKET':
            elements.append(self.expr())
            while self.peek()[0] == 'COMMA':
                self.match('COMMA')
                elements.append(self.expr())
        self.match('RBRACKET')
        self.match('ARDHAVIRAM')
        return ArrayDecl(name, elements)

    def print_statement(self):
        self.match('DIKHAO')
        self.match('LPAREN')
        expr = self.expr()
        self.match('RPAREN')
        self.match('ARDHAVIRAM')
        return PrintStmt(expr)

    def if_statement(self):
        self.match('AGAR')
        self.match('LPAREN')
        condition = self.expr()
        self.match('RPAREN')
        then_branch = self.block()
        else_branch = None
        if self.peek()[0] == 'NAHITO':
            self.match('NAHITO')
            else_branch = self.block()
        elif self.peek()[0] == 'WARNA':
            self.match('WARNA')
            else_branch = self.block()
        return IfStmt(condition, then_branch, else_branch)

    def while_statement(self):
        self.match('JABTAK')
        self.match('LPAREN')
        condition = self.expr()
        self.match('RPAREN')
        body = self.block()
        return WhileStmt(condition, body)

    def for_statement(self):
        self.match('KELIYE')
        self.match('LPAREN')
        self.skip_newlines()

        init = self.statement()
        self.skip_newlines()

        condition_stmt = self.statement()
        self.skip_newlines()

        increment = self.statement()
        self.skip_newlines()

        self.match('RPAREN')
        self.skip_newlines()

        body = self.block()

        if isinstance(condition_stmt, ConditionStmt):
            condition = condition_stmt.expr
        else:
            raise RuntimeError("For loop middle part must be a conditional expression with ardhaviram.")

        return ForStmt(init, condition, increment, body)

    def block(self):
        self.match('LBRACE')
        self.skip_newlines()
        stmts = []
        while self.peek()[0] != 'RBRACE':
            stmts.append(self.statement())
            self.skip_newlines()
        self.match('RBRACE')
        return stmts

    def expr(self):
        OP_MAP = {
            'LESSTHAN': '<',
            'GREATERTHAN': '>',
            'EQUALTO': '=='
        }
        node = self.term_expr()
        while self.peek()[0] in OP_MAP:
            tok_type = self.peek()[0]
            self.match(tok_type)
            op = OP_MAP[tok_type]
            right = self.term_expr()
            node = BinOp(node, op, right)
        return node

    def term_expr(self):
        OP_MAP = {
            'JODO': '+',
            'GHATAYO': '-'
        }
        node = self.term()
        while self.peek()[0] in OP_MAP:
            tok_type = self.peek()[0]
            self.match(tok_type)
            op = OP_MAP[tok_type]
            right = self.term()
            node = BinOp(node, op, right)
        return node

    def term(self):
        OP_MAP = {
            'GUNA': '*',
            'BHAG': '/'
        }
        node = self.factor()
        while self.peek()[0] in OP_MAP:
            tok_type = self.peek()[0]
            self.match(tok_type)
            op = OP_MAP[tok_type]
            right = self.factor()
            node = BinOp(node, op, right)
        return node

    def factor(self):
        tok = self.peek()
        if tok[0] == 'SANKHYA':
            return Num(self.match('SANKHYA')[1])
        elif tok[0] == 'TANTA':
            return Str(self.match('TANTA')[1])
        elif tok[0] == 'PEHCHAN':
            name = self.match('PEHCHAN')[1]
            node = Var(name)
            while self.peek()[0] == 'LBRACKET':
                self.match('LBRACKET')
                index = self.expr()
                self.match('RBRACKET')
                node = ArrayAccess(node.name, index)
                return node
            return node
        elif tok[0] == 'LPAREN':
            self.match('LPAREN')
            expr = self.expr()
            self.match('RPAREN')
            return expr
        else:
            raise RuntimeError(f"Invalid factor at token {tok}")
