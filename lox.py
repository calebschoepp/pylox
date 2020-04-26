import sys
from interpreter import Interpreter

class Lox():
    had_error = False
    had_runtime_error = False
    interpreter = Interpreter()

    def __init__(self):
        pass

    @staticmethod
    def main(args):
        if len(args) > 2:
            print("Usage: python3 lox [script]")
            sys.exit(64)
        elif len(args) == 2:
            Lox.run_file(args[1])
        else:
            Lox.run_prompt()

    @staticmethod
    def run_file(path):
        with open(path, 'r') as script:
            Lox.run(script.read())

            if Lox.had_error:
                sys.exit(65)
            if Lox.had_runtime_error:
                sys.exit(70)

    @staticmethod
    def run_prompt():
        while True:
            print("> ", end="")
            Lox.run(input())
            Lox.had_error = False

    @staticmethod
    def run(source):
        from scanner import Scanner
        from parser import Parser
        from ast_printer import AstPrinter
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()

        if Lox.had_error:
            return

        Lox.interpreter.interpret(expression)

    @staticmethod
    def scan_error(line, message):
        Lox.report(line, "", message)

    @staticmethod
    def report(line, where, message):
        print(f'[line {line}] Error {where}: {message}')

    @staticmethod
    def parse_error(token, message):
        from token_type import TT
        if token.type == TT.EOF:
            Lox.report(token.line, " at end", message)
        else:
            Lox.report(token.line, " at '" + token.lexeme + "'", message)

    @staticmethod
    def runtime_error(error):
        if not hasattr(error, 'token'):
            print("Unknown implementation error.")
            Lox.had_runtime_error = True
            return

        print("{}\n[line {}]".format(error, error.token.line))
        Lox.had_runtime_error = True

if __name__ == "__main__":
    Lox.main(sys.argv)