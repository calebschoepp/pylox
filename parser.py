from token_type import TT
import Expr
import Stmt

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def declaration(self):
        try:
            if self.match(TT.VAR):
                return self.var_declaration()

            return self.statement()
        except ParseError as e:
            self.synchronize()
            return None

    def var_declaration(self):
        name = self.consume(TT.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TT.EQUAL):
            initializer = self.expression()

        self.consume(TT.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    def statement(self):
        if self.match(TT.IF):
            return self.if_statement()
        elif self.match(TT.WHILE):
            return self.while_statement()
        elif self.match(TT.FOR):
            return self.for_statement()
        elif self.match(TT.PRINT):
            return self.print_statement()
        elif self.match(TT.LEFT_BRACE):
            return Stmt.Block(self.block())

        return self.expression_statement()

    def while_statement(self):
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()

        return Stmt.While(condition, body)

    def for_statement(self):
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer = None
        if self.match(TT.SEMICOLON):
            # Re-done for clarity
            initializer = None
        elif self.match(TT.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(TT.SEMICOLON):
            condition = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after loop condition")

        increment = None
        if not self.check(TT.RIGHT_PAREN):
            increment = self.expression()
        consume(TT.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.statement()

        if increment:
            body = Stmt.Block([
                body,
                Stmt.Expression(increment)
            ])
        if not condition:
           condition = Expr.Literal(True)
        body = Stmt.While(condition, body)

        if initializer:
            body = Stmt.Block([initializer, body]) 

        return body

    def if_statement(self):
        self.consume(TT.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TT.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TT.ELSE):
            else_branch = self.statement()

        return Stmt.If(condition, then_branch, else_branch)

    def print_statement(self):
        value = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TT.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)

    def block(self):
        statements = []

        while not self.check(TT.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TT.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.ternary()

        if self.match(TT.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Expr.Variable):
                name = expr.name
                return Expr.Assign(name, value)
            
            self.error(equals, "Invalid assignment target.")

        return expr

    def ternary(self):
        expr = self._or()
        if not self.match(TT.QUESTION):
            return expr
        
        consequent = self.ternary()
        self.consume(TT.COLON, "Expect : before alternative of ternary.")
        alternative = self.ternary()
        return Expr.Ternary(expr, consequent, alternative)

    def _or(self):
        expr = self._and()

        while self.match(TT.OR):
            operator = self.previous()
            right = self._and()
            expr = Expr.Logical(expr, operator, right)
        
        return expr

    def _and(self):
        expr = self.equality()

        while self.match(TT.AND):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)

        return expr

    def equality(self):
        expr = self.comparison()

        while (self.match(TT.BANG_EQUAL, TT.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.addition()

        while self.match(TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL):
            operator = self.previous()
            right = self.addition()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def addition(self):
        expr = self.multiplication()

        while self.match(TT.MINUS, TT.PLUS):
            operator = self.previous()
            right = self.multiplication()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def multiplication(self):
        expr = self.unary()

        while self.match(TT.SLASH, TT.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TT.BANG, TT.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TT.FALSE):
            return Expr.Literal(False)
        elif self.match(TT.TRUE):
            return Expr.Literal(True)
        elif self.match(TT.NIL):
            return Expr.Literal(None)
        elif self.match(TT.NUMBER, TT.STRING):
            return Expr.Literal(self.previous().literal)
        elif self.match(TT.IDENTIFIER):
            return Expr.Variable(self.previous())
        elif self.match(TT.LEFT_PAREN):
            expr = self.expression()
            self.consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def match(self, *types):
        for tipe in types:
            if self.check(tipe):
                self.advance()
                return True
        return False

    def consume(self, tipe, message):
        if self.check(tipe):
            return self.advance()
        
        raise self.error(self.peek(), message)

    def check(self, tipe):
        if self.is_at_end():
            return False
        return self.peek().type == tipe

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TT.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        from lox import Lox
        Lox.parse_error(token, message)
        return ParseError()

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TT.SEMICOLON:
                return
            elif self.peek().type == TT.CLASS:
                return
            elif self.peek().type == TT.FUN:
                return
            elif self.peek().type == TT.VAR:
                return
            elif self.peek().type == TT.FOR:
                return
            elif self.peek().type == TT.IF:
                return
            elif self.peek().type == TT.WHILE:
                return
            elif self.peek().type == TT.PRINT:
                return
            elif self.peek().type == TT.RETURN:
                return

            self.advance()

class ParseError(Exception):
    pass
