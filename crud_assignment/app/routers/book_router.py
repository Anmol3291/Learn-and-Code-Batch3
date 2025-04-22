from fastapi import APIRouter, HTTPException, status
from app.schemas.book_schema import BookCreate, BookUpdate, BookResponse
from app.repositories.book_repository import BookRepository
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService(BookRepository())


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(data: BookCreate):
    try:
        return service.create_book(data).to_dict()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create book: {str(e)}",
        )


@router.get("/", response_model=list[BookResponse])
def list_books():
    try:
        return [book.to_dict() for book in service.get_all_books()]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve books: {str(e)}",
        )


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    try:
        book = service.get_book(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        return book.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve book: {str(e)}",
        )


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, data: BookUpdate):
    try:
        updated = service.update_book(book_id, data)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        return updated.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update book: {str(e)}",
        )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    try:
        if not service.delete_book(book_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        return {"message": "Book deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete book: {str(e)}",
        )
