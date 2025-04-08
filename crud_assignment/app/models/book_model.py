class Book:
    def __init__(self, id: int, title: str, author: str):
        self.id = id
        self.title = title
        self.author = author

    def to_dict(self):
        return {"id": self.id, "title": self.title, "author": self.author}
