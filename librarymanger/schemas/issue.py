from datetime import date

from pydantic import BaseModel, Field


class IssueCreate(BaseModel):
    book_query: str = Field(..., min_length=1)
    borrower_name: str = Field(..., min_length=1)
    borrower_id: str = Field(..., min_length=1)


class ReturnBookRequest(BaseModel):
    issue_id: str | None = None
    borrower_id: str | None = None
    selection_index: int | None = Field(None, ge=1)


class IssueResponse(BaseModel):
    issue_id: str
    book_id: str
    book_title: str
    borrower_name: str
    borrower_id: str
    issue_date: date
    return_date: date | None

    model_config = {"from_attributes": True}