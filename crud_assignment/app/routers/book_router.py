from fastapi import APIRouter, HTTPException
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse
from app.repositories.book_repository import BookRepository
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService(BookRepository())


@router.post("/", response_model=BookResponse)
def create_book(data: BookCreate):
    return service.create_book(data).to_dict()


@router.get("/", response_model=list[BookResponse])
def list_books():
    return [book.to_dict() for book in service.get_all_books()]


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict()


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, data: BookUpdate):
    updated = service.update_book(book_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated.to_dict()


@router.delete("/{book_id}")
def delete_book(book_id: int):
    if not service.delete_book(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}
