# app/schemas.py

from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: str

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: float

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    book_id: int

    class Config:
        orm_mode = True
