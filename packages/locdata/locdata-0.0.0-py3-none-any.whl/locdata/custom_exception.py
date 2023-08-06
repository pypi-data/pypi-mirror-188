class InvalidNumberException(Exception):
    def __init__(self, message: str = "Invalid Number passed"):
        self.message = message
        super().__init__(self.message)
