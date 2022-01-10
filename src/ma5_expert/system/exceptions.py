Red = "\x1b[31m"
End = "\x1b[0m"


class InvalidInput(Exception):
    """Invalid Domain Exception"""

    def __init__(self, message="Invalid Input!"):
        super(InvalidInput, self).__init__(Red + message + End)
