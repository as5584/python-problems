"""Seed initial book data into PostgreSQL if tables are empty."""

from database import SessionLocal
from models import Book
from repositories.book_repository import BookRepository

INITIAL_BOOKS = [
    {
        "id": "B001",
        "title": "Python Programming",
        "author": "Eric Matthes",
        "isbn": "978-1593279288",
        "total_copies": 3,
        "available_copies": 3,
    },
    {
        "id": "B002",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "978-0132350884",
        "total_copies": 2,
        "available_copies": 2,
    },
    {
        "id": "B003",
        "title": "The Pragmatic Programmer",
        "author": "David Thomas",
        "isbn": "978-0135957059",
        "total_copies": 1,
        "available_copies": 1,
    },
]


def seed_initial_data() -> None:
    session = SessionLocal()
    try:
        if BookRepository(session).count() > 0:
            print("Database already has data. Skipping seed.")
            return

        for book_data in INITIAL_BOOKS:
            session.add(Book(**book_data))

        session.commit()
        print(f"Seeded {len(INITIAL_BOOKS)} books into PostgreSQL.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_initial_data()