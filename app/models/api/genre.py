from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Genre(GenreBase):
    id: int
