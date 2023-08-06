class CopyrightInfo:
    def __init__(self, text: str, prefix: str, suffix: str):
        self.text = text
        self.prefix = prefix
        self.suffix = suffix

        self.full_text = f"{self.prefix}{self.text}{self.suffix}"
