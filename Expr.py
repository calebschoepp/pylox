class Expr():
    pass

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)

class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)

class Ternary(Expr):
    def __init__(self, expression, consequent, alternative):
        self.expression = expression
        self.consequent = consequent
        self.alternative = alternative

    def accept(self, visitor):
        return visitor.visitTernaryExpr(self)

