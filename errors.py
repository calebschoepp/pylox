class RunTimeError(Exception):
    # TODO make more idiomatic to Python
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token