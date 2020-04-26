import sys

class Lox():
    had_error = False

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

        print(AstPrinter().print(expression))
        
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

if __name__ == "__main__":
    Lox.main(sys.argv)