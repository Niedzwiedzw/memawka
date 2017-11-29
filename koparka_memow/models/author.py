class Author:
    def __init__(self, raw_author):
        self.name = raw_author['name']
        self.id = raw_author['id']

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"

    def __repr__(self) -> str:
        return f"[{self.id}] {self.name}"
