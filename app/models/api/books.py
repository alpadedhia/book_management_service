from pydantic import BaseModel

from app.models.api.author import AuthorBase
from app.models.api.genre import GenreBase


class BookBase(BaseModel):
    title: str
    year_published: int | None
    summary: str | None
    author: AuthorBase
    genre: GenreBase | None


class Book(BookBase):
    id: int
    author_id: int
    genre_id: int | None
