from dataclasses import dataclass

from sqlalchemy.orm import Session

from models import Book
from repositories.book_repository import BookRepository


@dataclass
class AvailabilitySummary:
    total_titles: int
    total_copies: int
    available_copies: int
    issued_copies: int


class BookService:
    def __init__(self, session: Session) -> None:
        self.repo = BookRepository(session)

    def add_book(
        self,
        title: str,
        author: str,
        isbn: str,
        copies: int,
    ) -> tuple[Book | None, str | None]:
        if not title or not author:
            return None, "Title and author are required."

        if self.repo.exists_by_isbn(isbn):
            return None, "A book with this ISBN already exists."

        if copies < 1:
            return None, "Enter a valid number of copies (1 or more)."

        book = Book(
            id=self.repo.next_id(),
            title=title,
            author=author,
            isbn=isbn,
            total_copies=copies,
            available_copies=copies,
        )
        return self.repo.add(book), None

    def find_book(self, query: str) -> Book | None:
        return self.repo.find_by_query(query)

    def search_books(self, query: str) -> list[Book]:
        if not query.strip():
            return []
        return self.repo.search(query)

    def get_all_books(self) -> list[Book]:
        return self.repo.get_all()

    def get_availability_summary(self) -> AvailabilitySummary | None:
        books = self.repo.get_all()
        if not books:
            return None

        total_copies = sum(b.total_copies for b in books)
        available = sum(b.available_copies for b in books)
        return AvailabilitySummary(
            total_titles=len(books),
            total_copies=total_copies,
            available_copies=available,
            issued_copies=total_copies - available,
        )