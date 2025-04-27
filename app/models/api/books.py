from pydantic import BaseModel

from app.models.api.author import Author
from app.models.api.genre import Genre


class BookRequest(BaseModel):
    title: str
    year_published: int | None = None
    summary: str | None = None
    authors: list[str]
    genres: list[str] | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    authors: list[Author]
    genres: list[Genre] | None = None
    year_published: int | None = None
    summary: str | None = None
