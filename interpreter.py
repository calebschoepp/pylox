from token_type import TT
from errors import RunTimeError
from environment import Environment


class Interpreter():
    def __init__(self):
        self.environment = Environment(None)

    def interpret(self, statements):
        from lox import Lox
        try:
            for stmt in statements:
                self.execute(stmt)
        except RunTimeError as e:
            Lox.runtime_error(e)
        except:
            Lox.runtime_error(RunTimeError(None, "Unknown failure."))

    def visitLiteralExpr(self, expr):
        return expr.value

    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == TT.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right
        elif expr.operator.type == TT.BANG:
            return not self.is_truthy(right)

        return None

    def visitVariableExpr(self, expr):
        return self.environment.get(expr.name)

    def visitGroupingExpr(self, expr):
        return self.evaluate(expr.expression)

    def visitBinaryExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TT.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        elif expr.operator.type == TT.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        elif expr.operator.type == TT.LESS:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        elif expr.operator.type == TT.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        elif expr.operator.type == TT.BANG_EQUAL:
            return self.is_equal(left, right)
        elif expr.operator.type == TT.EQUAL:
            return self.is_equal(left, right)
        elif expr.operator.type == TT.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return left - right
        elif expr.operator.type == TT.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return left / right
        elif expr.operator.type == TT.STAR:
            self.check_number_operands(expr.operator, left, right)
            return left * right
        elif expr.operator.type == TT.PLUS:
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            elif isinstance(left, float) and isinstance(right, float):
                return left + right
            raise RunTimeError(expr.operator, "Operands must be two numbers or two strings.")

        return None

    def visitTernaryExpr(self, expr):
        if self.is_truthy(self.evaluate(expr.expression)):
            return self.evaluate(expr.consequent)
        return self.evaluate(expr.alternative)

    def is_truthy(self, obj):
        if obj is None:
            return False
        elif type(obj) == type(True):
            return obj
        return True

    def is_equal(self, a, b):
        # Nil is only equal to nil
        if a is None and b is None:
            return True
        elif a is None:
            return False
        return a == b
    
    def stringify(self, obj):
        if obj is None:
            return 'nil'
        
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(obj)

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return
        raise RunTimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise RunTimeError(operator, "Operands must be numbers.")

    def evaluate(self, expr):
        return expr.accept(self)

    def execute(self, stmt):
        stmt.accept(self)

    def execute_block(self, statements, environment):
        previous = self.environment

        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visitBlockStmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visitVarStmt(self, stmt):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)

        self.environment.assign(expr.name, value)
        return value
