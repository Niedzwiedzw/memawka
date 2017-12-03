class Author:
    def __init__(self, raw_author):
        if raw_author is not None:
            self.name = raw_author.get('name', 'BANNED_USER')
            self.facebook_id = str(raw_author.get('id', 'BANNED_USER'))
        else:
            self.name = 'BANNED_USER'
            self.facebook_id = 'BANNED_USER_ID'

    def __str__(self) -> str:
        return f"[{self.id}] {self.name}"

    def __repr__(self) -> str:
        return f"[{self.id}] {self.name}"
