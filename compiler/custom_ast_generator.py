from compiler.ast_nodes import *

class ASTBuilder:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def eat(self, expected_type):
        token_type, value = self.current()
        if token_type == expected_type:
            self.pos += 1
            return value
        raise SyntaxError(f"Expected {expected_type}, got {token_type}")

    def parse(self):
        statements = []
        while self.current()[0] != 'EOF':
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        token_type, value = self.current()

        if token_type == 'PEHCHAN':
            # Assignment: x barabar 5;
            name = self.eat('PEHCHAN')
            self.eat('ASSIGN')
            expr = self.parse_expression()
            self.eat('ARDHAVIRAM')
            return LetStmt(name, expr)

        elif token_type == 'CHAP':  # 'print'
            self.eat('CHAP')
            expr = self.parse_expression()
            self.eat('ARDHAVIRAM')
            return PrintStmt(expr)

        elif token_type == 'AGAR':
            self.eat('AGAR')
            self.eat('LPAREN')
            condition = self.parse_expression()
            self.eat('RPAREN')
            self.eat('LBRACE')
            then_branch = self.parse_block()
            self.eat('RBRACE')

            else_branch = None
            if self.current()[0] == 'WARNA':
                self.eat('WARNA')
                self.eat('LBRACE')
                else_branch = self.parse_block()
                self.eat('RBRACE')
            return IfStmt(condition, then_branch, else_branch)

        elif token_type == 'JABTAK':
            self.eat('JABTAK')
            self.eat('LPAREN')
            condition = self.parse_expression()
            self.eat('RPAREN')
            self.eat('LBRACE')
            body = self.parse_block()
            self.eat('RBRACE')
            return WhileStmt(condition, body)

        elif token_type == 'LOTAO':
            self.eat('LOTAO')
            expr = self.parse_expression()
            self.eat('ARDHAVIRAM')
            return ReturnStmt(expr)

        elif token_type == 'TODO':
            self.eat('TODO')
            self.eat('ARDHAVIRAM')
            return BreakStmt()

        elif token_type == 'KE_LIYE':
            self.eat('KE_LIYE')
            self.eat('LPAREN')
            init = self.parse_statement()
            condition = self.parse_expression()
            self.eat('ARDHAVIRAM')
            increment = self.parse_statement()
            self.eat('RPAREN')
            self.eat('LBRACE')
            body = self.parse_block()
            self.eat('RBRACE')
            return ForStmt(init, condition, increment, body)

        else:
            raise SyntaxError(f"Unknown statement starting with {token_type}")

    def parse_block(self):
        statements = []
        while self.current()[0] not in ('RBRACE', 'EOF'):
            statements.append(self.parse_statement())
        return statements

    def parse_expression(self):
        left = self.parse_term()
        while self.current()[0] in ('PLUS', 'MINUS', 'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE'):
            op = self.eat(self.current()[0])
            right = self.parse_term()
            left = BinOp(left, op, right)
        return left

    def parse_term(self):
        token_type, value = self.current()

        if token_type == 'SANKHYA':
            self.eat('SANKHYA')
            return Num(int(value))

        elif token_type == 'PEHCHAN':
            var_name = self.eat('PEHCHAN')
            if self.current()[0] == 'LBRACKET':
                self.eat('LBRACKET')
                index = self.parse_expression()
                self.eat('RBRACKET')
                return ArrayAccess(var_name, index)
            return Var(var_name)

        elif token_type == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expression()
            self.eat('RPAREN')
            return expr

        else:
            raise SyntaxError(f"Unexpected token in expression: {token_type}")
