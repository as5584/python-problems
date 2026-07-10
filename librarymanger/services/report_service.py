from pathlib import Path

from sqlalchemy.orm import Session

from reports import generate_pdf_report, generate_xlsx_report
from repositories.book_repository import BookRepository
from repositories.issue_repository import IssueRepository


class ReportService:
    def __init__(self, session: Session) -> None:
        self.book_repo = BookRepository(session)
        self.issue_repo = IssueRepository(session)

    def generate_reports(self) -> tuple[Path, Path] | None:
        books = self.book_repo.get_all()
        if not books:
            return None

        issues = self.issue_repo.get_all()
        xlsx_path = generate_xlsx_report(books, issues)
        pdf_path = generate_pdf_report(books, issues)
        return xlsx_path, pdf_path