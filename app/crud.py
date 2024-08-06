# app/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Book).filter(models.Book.id == book_id))
    return result.scalar_one_or_none()

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Book).offset(skip).limit(limit))
    return result.scalars().all()

async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def update_book(db: AsyncSession, db_book: models.Book, book: schemas.BookUpdate):
    for var, value in vars(book).items():
        setattr(db_book, var, value) if value else None
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    await db.delete(db_book)
    await db.commit()
    return db_book
