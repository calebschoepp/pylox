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
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    @staticmethod
    def error(line, message):
        Lox.report(line, "", message)

    @staticmethod
    def report(line, where, message):
        print(f'[line {line}] Error {where}: {message}')

if __name__ == "__main__":
    Lox.main(sys.argv)