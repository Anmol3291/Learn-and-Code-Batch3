from app.models.book_model import Book


class BookRepository:
    def __init__(self):
        self.books = {}
        self.next_id = 1

    def create(self, title: str, author: str) -> Book:
        book = Book(self.next_id, title, author)
        self.books[self.next_id] = book
        self.next_id += 1
        return book

    def list_all(self) -> list[Book]:
        return list(self.books.values())

    def get_by_id(self, book_id: int) -> Book | None:
        return self.books.get(book_id)

    def update(self, book_id: int, title: str, author: str) -> Book | None:
        if book_id in self.books:
            self.books[book_id].title = title
            self.books[book_id].author = author
            return self.books[book_id]
        return None

    def delete(self, book_id: int) -> bool:
        return self.books.pop(book_id, None) is not None
