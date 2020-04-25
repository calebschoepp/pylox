from token_type import TT
from token import Token
import lox

keywords = {                                
    "and":    TT.AND,
    "class":  TT.CLASS,
    "else":   TT.ELSE,
    "false":  TT.FALSE,
    "for":    TT.FOR,
    "fun":    TT.FUN,
    "if":     TT.IF,
    "nil":    TT.NIL,
    "or":     TT.OR,
    "print":  TT.PRINT,
    "return": TT.RETURN,
    "super":  TT.SUPER,
    "this":   TT.THIS,
    "true":   TT.TRUE,
    "var":    TT.VAR,
    "while":  TT.WHILE,
}

class Scanner():
    def __init__(self, source):
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = []

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TT.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()

        if c == '(':
            self.add_token(TT.LEFT_PAREN, None)
        elif c == ')':
            self.add_token(TT.RIGHT_PAREN, None)
        elif c == '{':
            self.add_token(TT.LEFT_BRACE, None)
        elif c == '}':
            self.add_token(TT.RIGHT_BRACE, None)
        elif c == ',':
            self.add_token(TT.COMMA, None)
        elif c == '.':
            self.add_token(TT.DOT, None)
        elif c == '-':
            self.add_token(TT.MINUS, None)
        elif c == '+':
            self.add_token(TT.PLUS, None)
        elif c == ';':
            self.add_token(TT.SEMICOLON, None)
        elif c == '*':
            self.add_token(TT.STAR, None)
        elif c == '!':
            self.add_token(TT.BANG_EQUAL if self.match('=') else TT.BANG, None)
        elif c == '=':
            self.add_token(TT.EQUAL_EQUAL if self.match('=') else TT.EQUAL, None)
        elif c == '<':
            self.add_token(TT.LESS_EQUAL if self.match('=') else TT.LESS, None)
        elif c == '>':
            self.add_token(TT.GREATER_EQUAL if self.match('=') else TT.GREATER, None)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TT.SLASH, None)
        elif c in [' ', '\r', '\t']:
            pass # Ignore whitespace
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        elif self.is_digit(c):
            self.number()
        elif self.is_alpha(c):
            self.identifier()
        else:
            lox.Lox.error(self.line, "Unexpected character.")

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]

        tipe = keywords.get(text)
        if tipe == None:
            tipe = TT.IDENTIFIER

        self.add_token(tipe, None)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # Search for a fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # Consume the point
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TT.NUMBER, float(self.source[self.start:self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        # Unterminated string
        if self.is_at_end():
            lox.Lox.error(self.line, "Unterminated string.")
            return
        
        # Closing "
        self.advance()

        # Trim the surrounding quotes off
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TT.STRING, value)

    def match(self, expected):
        if self.is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_alpha(self, c):
        return c.isalpha()

    def is_alpha_numeric(self, c):
        return c.isalnum()

    def is_digit(self, c):
        return c.isdigit()

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, tipe, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(tipe, text, literal, self.line))