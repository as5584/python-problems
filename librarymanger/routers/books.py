from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_session
from schemas.book import (
    AvailabilityResponse,
    BookCreate,
    BookResponse,
    BookSearchResponse,
)
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse, status_code=201)
def add_book(payload: BookCreate, session: Session = Depends(get_session)):
    service = BookService(session)
    book, error = service.add_book(
        title=payload.title,
        author=payload.author,
        isbn=payload.isbn,
        copies=payload.copies,
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return book


@router.get("/", response_model=list[BookResponse])
def list_books(session: Session = Depends(get_session)):
    return BookService(session).get_all_books()


@router.get("/search", response_model=BookSearchResponse)
def search_books(
    q: str = Query(..., min_length=1),
    session: Session = Depends(get_session),
):
    results = BookService(session).search_books(q)
    return BookSearchResponse(count=len(results), books=results)


@router.get("/availability", response_model=AvailabilityResponse)
def availability(session: Session = Depends(get_session)):
    service = BookService(session)
    summary = service.get_availability_summary()
    if not summary:
        raise HTTPException(status_code=404, detail="No books in the library.")

    books = service.get_all_books()
    return AvailabilityResponse(
        total_titles=summary.total_titles,
        total_copies=summary.total_copies,
        available_copies=summary.available_copies,
        issued_copies=summary.issued_copies,
        books=books,
    )


@router.get("/{query}", response_model=BookResponse)
def find_book(query: str, session: Session = Depends(get_session)):
    book = BookService(session).find_book(query)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    return book