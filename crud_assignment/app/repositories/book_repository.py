from app.models.book_model import Book


class BookRepository:
    def __init__(self):
        self.books = {}
        self.next_id = 1

    def create(self, title: str, author: str) -> Book:
        try:
            book = Book(self.next_id, title, author)
            self.books[self.next_id] = book
            self.next_id += 1
            return book
        except Exception as e:
            print(f"Error creating book: {e}")
            raise

    def list_all(self) -> list[Book]:
        try:
            return list(self.books.values())
        except Exception as e:
            print(f"Error listing books: {e}")
            raise

    def get_by_id(self, book_id: int) -> Book | None:
        try:
            return self.books.get(book_id)
        except Exception as e:
            print(f"Error getting book by ID: {e}")
            raise

    def update(self, book_id: int, title: str, author: str) -> Book | None:
        try:
            if book_id in self.books:
                self.books[book_id].title = title
                self.books[book_id].author = author
                return self.books[book_id]
            return None
        except Exception as e:
            print(f"Error updating book: {e}")
            raise

    def delete(self, book_id: int) -> bool:
        try:
            return self.books.pop(book_id, None) is not None
        except Exception as e:
            print(f"Error deleting book: {e}")
            raise
