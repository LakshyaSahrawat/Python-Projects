"""CRUD utilities and a small business-logic function used in tests."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
from app import models
from app.schemas import book as schemas
from app.models.book import Book


async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.book.Book).filter(models.book.Book.id == book_id))
    return result.scalar_one_or_none()


async def get_books(db: AsyncSession, skip: int = 0, limit: int = 10, title_filter: str | None = None):
    stmt = select(models.book.Book)
    if title_filter:
        stmt = stmt.filter(models.book.Book.title.ilike(f"%{title_filter}%"))
    result = await db.execute(stmt.offset(skip).limit(limit))
    return result.scalars().all()


async def create_book(db: AsyncSession, book_in: schemas.BookCreate):
    db_book = models.book.Book(title=book_in.title, description=book_in.description)
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def update_book(db: AsyncSession, book: Book, book_in: schemas.BookUpdate):
    if book_in.title is not None:
        book.title = book_in.title
    if book_in.description is not None:
        book.description = book_in.description
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(db: AsyncSession, book: models.book.Book):
    await db.delete(book)
    await db.commit()
    return True


async def count_books(db: AsyncSession) -> int:
    result = await db.execute(text("SELECT COUNT(*) as count FROM books"))
    row = result.mappings().first()
    return int(row["count"]) if row else 0


async def create_book_with_update(db: AsyncSession, book_in: schemas.BookCreate, new_description: str):
    try:
        book = models.book.Book(title=book_in.title, description=book_in.description)
        db.add(book)
        await db.flush()

        book.description = new_description
        db.add(book)

        await db.commit()
        await db.refresh(book)
        return book
    except Exception:
        await db.rollback()
        raise


def summarize_book_title(title: str) -> str:
    if not title:
        return "untitled"
    tokens = title.strip().split()
    return "-".join([t.lower() for t in tokens[:3]])