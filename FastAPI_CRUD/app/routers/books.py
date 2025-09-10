"""FastAPI routers & endpoint wiring."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas import book as schemas
from app.business_layer import book as crud
from app.models import book as models
from app.database import async_session
from app.models.book import Book

router = APIRouter(prefix="/books", tags=["books"])

# Dependency
async def get_db():
    async with async_session() as session:
        yield session


@router.post("/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
async def create_book_endpoint(book_in: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        Book.__table__.select().where(Book.title == book_in.title)
    )
    if existing.first():
        raise HTTPException(status_code=400, detail="Title must be unique")
    return await crud.create_book(db, book_in)


@router.get("/", response_model=List[schemas.BookOut])
async def list_books(skip: int = 0, limit: int = 10, title: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    return await crud.get_books(db, skip=skip, limit=limit, title_filter=title)


@router.get("/{book_id}", response_model=schemas.BookOut)
async def get_book_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.put("/{book_id}", response_model=schemas.BookOut)
async def update_book_endpoint(book_id: int, book_in: schemas.BookUpdate, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_in.title and book_in.title != db_book.title:
        existing = await db.execute(
            Book.__table__.select().where(Book.title == book_in.title)
        )
        if existing.first():
            raise HTTPException(status_code=400, detail="Title must be unique")

    return await crud.update_book(db, db_book, book_in)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await crud.delete_book(db, db_book)
    return None


@router.get("/count/", response_model=int)
async def books_count(db: AsyncSession = Depends(get_db)):
    return await crud.count_books(db)