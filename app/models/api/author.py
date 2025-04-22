from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Author(AuthorBase):
    id: int
