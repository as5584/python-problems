from sqlalchemy.orm import Session

from models import Issue


class IssueRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Issue]:
        return self.session.query(Issue).order_by(Issue.issue_id).all()

    def get_active(self) -> list[Issue]:
        return (
            self.session.query(Issue)
            .filter(Issue.return_date.is_(None))
            .all()
        )

    def get_active_by_issue_id(self, issue_id: str) -> Issue | None:
        return (
            self.session.query(Issue)
            .filter(Issue.return_date.is_(None), Issue.issue_id == issue_id)
            .first()
        )

    def get_active_by_borrower(self, borrower_id: str) -> list[Issue]:
        return (
            self.session.query(Issue)
            .filter(
                Issue.return_date.is_(None),
                Issue.borrower_id == borrower_id,
            )
            .all()
        )

    def next_id(self) -> str:
        issues = self.session.query(Issue).all()
        if not issues:
            return "I001"
        nums = [int(i.issue_id[1:]) for i in issues if i.issue_id.startswith("I")]
        return f"I{max(nums, default=0) + 1:03d}"

    def add(self, issue: Issue) -> Issue:
        self.session.add(issue)
        self.session.commit()
        self.session.refresh(issue)
        return issue

    def update(self, issue: Issue) -> Issue:
        self.session.commit()
        self.session.refresh(issue)
        return issue