from app.schemas.book_schema import BookCreate, BookUpdate
from app.repositories.book_repository import BookRepository


class BookService:
    def __init__(self, repo: BookRepository):
        self.repo = repo

    def create_book(self, data: BookCreate):
        return self.repo.create(data.title, data.author)

    def get_all_books(self):
        return self.repo.list_all()

    def get_book(self, book_id: int):
        return self.repo.get_by_id(book_id)

    def update_book(self, book_id: int, data: BookUpdate):
        return self.repo.update(book_id, data.title, data.author)

    def delete_book(self, book_id: int):
        return self.repo.delete(book_id)
