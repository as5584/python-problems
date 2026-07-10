from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_session
from schemas.issue import IssueCreate, IssueResponse, ReturnBookRequest
from services.issue_service import IssueService

router = APIRouter(prefix="/issues", tags=["issues"])


@router.post("/", response_model=IssueResponse, status_code=201)
def issue_book(payload: IssueCreate, session: Session = Depends(get_session)):
    service = IssueService(session)
    record, error = service.issue_book(
        book_query=payload.book_query,
        borrower_name=payload.borrower_name,
        borrower_id=payload.borrower_id,
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return record


@router.post("/return", response_model=IssueResponse)
def return_book(payload: ReturnBookRequest, session: Session = Depends(get_session)):
    service = IssueService(session)
    record, error, matches = service.return_book(
        issue_id=payload.issue_id,
        borrower_id=payload.borrower_id,
        selection_index=payload.selection_index,
    )

    if matches:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Multiple active issues found. Provide selection_index.",
                "issues": [IssueResponse.model_validate(m) for m in matches],
            },
        )

    if error:
        raise HTTPException(status_code=400, detail=error)
    return record


@router.get("/active", response_model=list[IssueResponse])
def list_active_issues(session: Session = Depends(get_session)):
    return IssueService(session).get_active_issues()