from app.schemas.book_schema import BookCreate, BookUpdate
from app.repositories.book_repository import BookRepository


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def create_book(self, data: BookCreate):
        try:
            return self.repo.create(data.title, data.author)
        except Exception as e:
            print(f"Service error creating book: {e}")
            raise

    def get_all_books(self):
        try:
            return self.repo.list_all()
        except Exception as e:
            print(f"Service error listing books: {e}")
            raise

    def get_book(self, book_id: int):
        try:
            return self.repo.get_by_id(book_id)
        except Exception as e:
            print(f"Service error getting book: {e}")
            raise

    def update_book(self, book_id: int, data: BookUpdate):
        try:
            return self.repo.update(book_id, data.title, data.author)
        except Exception as e:
            print(f"Service error updating book: {e}")
            raise

    def delete_book(self, book_id: int):
        try:
            return self.repo.delete(book_id)
        except Exception as e:
            print(f"Service error deleting book: {e}")
            raise
