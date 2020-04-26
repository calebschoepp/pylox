from token_type import TT
import Expr

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            return self.expression()
        except ParseError:
            return None

    def expression(self):
        return self.ternary()

    def ternary(self):
        expr = self.equality()
        if not self.match(TT.QUESTION):
            return expr
        
        consequent = self.ternary()
        self.consume(TT.COLON, "Expect : before alternative of ternary.")
        alternative = self.ternary()
        return Expr.Ternary(expr, consequent, alternative)

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
