from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    isbn: str = Field(..., min_length=1)
    copies: int = Field(..., ge=1)


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    isbn: str
    total_copies: int
    available_copies: int

    model_config = {"from_attributes": True}


class BookSearchResponse(BaseModel):
    count: int
    books: list[BookResponse]


class AvailabilityResponse(BaseModel):
    total_titles: int
    total_copies: int
    available_copies: int
    issued_copies: int
    books: list[BookResponse]