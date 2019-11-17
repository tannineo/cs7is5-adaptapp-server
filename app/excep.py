class InputError(Exception):
    def __init__(self, arg):
        self.args = arg
