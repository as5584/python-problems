from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_session
from services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/generate")
def generate_reports(session: Session = Depends(get_session)):
    result = ReportService(session).generate_reports()
    if not result:
        raise HTTPException(status_code=404, detail="No data to report. Add books first.")

    xlsx_path, pdf_path = result
    return {
        "message": "Reports generated successfully.",
        "xlsx": str(xlsx_path),
        "pdf": str(pdf_path),
    }