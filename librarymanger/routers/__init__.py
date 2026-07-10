from routers.books import router as books_router
from routers.issues import router as issues_router
from routers.reports import router as reports_router

__all__ = ["books_router", "issues_router", "reports_router"]