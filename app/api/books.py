from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.session_manager import get_db_session as db_session
from app.models.api.books import BookRequest, BookResponse
from app.models.database import Author, Book, Genre

router = APIRouter(prefix="/books", tags=["Books APIs"])


@router.post("/", response_model=BookResponse)
async def create_book(book: BookRequest, db: AsyncSession = Depends(db_session)):
    author = await Author.get_or_create_author(book.author.name, db=db)
    genre = (
        await Genre.get_or_create_genre(book.genre.name, db=db) if book.genre else None
    )

    book = await Book.create(
        db=db,
        title=book.title,
        author_id=author.id,
        genre_id=genre.id if genre else None,
        year_published=book.year_published,
        summary=book.summary,
    )
    return book
