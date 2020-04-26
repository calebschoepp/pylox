from Expr import *
from token import Token
from token_type import TT

class AstPrinter():
    def __init__(self):
        # expr = Binary(
        #     Unary(
        #         Token(TT.MINUS, "-", None, 1),
        #         Literal(123)
        #     ),
        #     Token(TT.STAR, "*", None, 1),
        #     Grouping(
        #         Literal(45.67)
        #     )
        # )
        expr = Binary(
            Grouping(
                Binary(
                    Literal(1),
                    Token(TT.PLUS, "+", None, 1),
                    Literal(2)
                )
            ),
            Token(TT.STAR, "*", None, 1),
            Grouping(
                Binary(
                    Literal(4),
                    Token(TT.MINUS, "-", None, 1),
                    Literal(3)
                )
            )
        )
        print(self.print(expr))

    def print(self, expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, *args):
        # TODO improve error handling here
        out = "("
        out += args[0]
        for expr in args[1:]:
            out += " "
            out += expr.accept(self)
        out += ")"

        return out


ast_printer = AstPrinter()
