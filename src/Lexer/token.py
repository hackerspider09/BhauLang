class Token:
    def __init__(self, type, value=None) -> None:
        self.TYPE = type
        self.VALUE = value

    def __repr__(self) -> str:
        if self.VALUE:
            return f"{self.TYPE} : {self.VALUE}"
        return f"{self.TYPE}"
