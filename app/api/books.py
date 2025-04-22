from fastapi import APIRouter

from app.models.api.books import Book

router = APIRouter(prefix="/books", tags=["Books APIs"])


@router.post("/", response_model=Book)
async def create_book(book: Book):
    pass
