from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    total_copies: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    available_copies: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    issues: Mapped[list["Issue"]] = relationship(back_populates="book")


class Issue(Base):
    __tablename__ = "issues"

    issue_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    book_id: Mapped[str] = mapped_column(
        String(10), ForeignKey("books.id"), nullable=False
    )
    book_title: Mapped[str] = mapped_column(String(255), nullable=False)
    borrower_name: Mapped[str] = mapped_column(String(255), nullable=False)
    borrower_id: Mapped[str] = mapped_column(String(50), nullable=False)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    return_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    book: Mapped["Book"] = relationship(back_populates="issues")

    __table_args__ = (UniqueConstraint("issue_id", name="uq_issues_issue_id"),)