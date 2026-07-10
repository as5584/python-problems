from datetime import date

from sqlalchemy.orm import Session

from models import Issue
from repositories.book_repository import BookRepository
from repositories.issue_repository import IssueRepository


class IssueService:
    def __init__(self, session: Session) -> None:
        self.issue_repo = IssueRepository(session)
        self.book_repo = BookRepository(session)

    def issue_book(
        self,
        book_query: str,
        borrower_name: str,
        borrower_id: str,
    ) -> tuple[Issue | None, str | None]:
        book = self.book_repo.find_by_query(book_query)
        if not book:
            return None, "Book not found."

        if book.available_copies < 1:
            return None, f"No copies available. ({book.title})"

        if not borrower_name or not borrower_id:
            return None, "Borrower name and ID are required."

        record = Issue(
            issue_id=self.issue_repo.next_id(),
            book_id=book.id,
            book_title=book.title,
            borrower_name=borrower_name,
            borrower_id=borrower_id,
            issue_date=date.today(),
            return_date=None,
        )
        book.available_copies -= 1
        self.issue_repo.add(record)
        self.book_repo.update(book)
        return record, None

    def return_book(
        self,
        issue_id: str | None = None,
        borrower_id: str | None = None,
        selection_index: int | None = None,
    ) -> tuple[Issue | None, str | None, list[Issue] | None]:
        if issue_id:
            record = self.issue_repo.get_active_by_issue_id(issue_id)
            if not record:
                return None, "Issue record not found or already returned.", None
            return self._complete_return(record)

        if not borrower_id:
            return None, "Borrower ID is required when issue ID is not provided.", None

        matches = self.issue_repo.get_active_by_borrower(borrower_id)
        if not matches:
            return None, "No active issues found for this borrower.", None

        if len(matches) == 1:
            return self._complete_return(matches[0])

        if selection_index is None:
            return None, None, matches

        try:
            record = matches[selection_index - 1]
        except IndexError:
            return None, "Invalid selection.", None

        return self._complete_return(record)

    def get_active_issues(self) -> list[Issue]:
        return self.issue_repo.get_active()

    def _complete_return(
        self, record: Issue
    ) -> tuple[Issue | None, str | None, list[Issue] | None]:
        book = self.book_repo.get_by_id(record.book_id)
        if not book:
            return None, "Book record not found.", None

        record.return_date = date.today()
        book.available_copies += 1
        self.issue_repo.update(record)
        self.book_repo.update(book)
        return record, None, None