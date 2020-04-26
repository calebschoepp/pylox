from Expr import *
from token import Token
from token_type import TT

class AstPrinter():
    def __init__(self):
        pass

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

    def visitTernaryExpr(self, expr):
        return self.parenthesize("Ternary", expr.expression, expr.consequent, expr.alternative)

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
