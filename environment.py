from errors import RunTimeError

class Environment():
    def __init__(self, enclosing):
        self.enclosing = enclosing
        self.values = {}

    def get(self, name):
        if name.lexeme in self.values.keys():
            return self.values.get(name.lexeme)

        if self.enclosing:
            return self.enclosing.get(name)
        
        raise RunTimeError(name, "Undefined variable '{}'.".format(name.lexeme))

    def assign(self, name, value):
        if name.lexeme in self.values.keys():
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(name, "Undefined variable '{}'.".format(name.lexeme))

    def define(self, name, value):
        self.values[name] = value
