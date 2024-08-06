# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas, crud, database
from .dependencies import get_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.init_db()

@app.post("/books/", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_book(db=db, book=book)

@app.get("/books/", response_model=list[schemas.Book])
async def read_books(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    books = await crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/{book_id}", response_model=schemas.Book)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(book_id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return await crud.update_book(db, db_book=db_book, book=book)

@app.delete("/books/{book_id}", response_model=schemas.Book)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    await crud.delete_book(db, book_id=book_id)
    return db_book
