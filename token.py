class Token():
    # tipe used in place of type b/c it is a keyword. Similar to klass
    def __init__(self, tipe, lexeme, literal, line):
        self.type = tipe
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

