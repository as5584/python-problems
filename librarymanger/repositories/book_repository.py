from sqlalchemy import or_
from sqlalchemy.orm import Session

from models import Book


class BookRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Book]:
        return self.session.query(Book).all()

    def get_by_id(self, book_id: str) -> Book | None:
        return self.session.query(Book).filter(Book.id == book_id).first()

    def find_by_query(self, query: str) -> Book | None:
        query = query.strip().lower()
        return (
            self.session.query(Book)
            .filter(
                or_(
                    Book.id.ilike(query),
                    Book.isbn.ilike(query),
                    Book.title.ilike(query),
                )
            )
            .first()
        )

    def search(self, query: str) -> list[Book]:
        query = query.strip().lower()
        return (
            self.session.query(Book)
            .filter(
                or_(
                    Book.title.ilike(f"%{query}%"),
                    Book.author.ilike(f"%{query}%"),
                    Book.isbn.ilike(f"%{query}%"),
                )
            )
            .all()
        )

    def exists_by_isbn(self, isbn: str) -> bool:
        return (
            self.session.query(Book).filter(Book.isbn.ilike(isbn)).first()
            is not None
        )

    def next_id(self) -> str:
        books = self.get_all()
        if not books:
            return "B001"
        nums = [int(b.id[1:]) for b in books if b.id.startswith("B")]
        return f"B{max(nums, default=0) + 1:03d}"

    def add(self, book: Book) -> Book:
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    def update(self, book: Book) -> Book:
        self.session.commit()
        self.session.refresh(book)
        return book

    def count(self) -> int:
        return self.session.query(Book).count()