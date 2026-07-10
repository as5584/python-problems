from fastapi import FastAPI

from routers import books_router, issues_router, reports_router

app = FastAPI(title="Library Management System", version="1.0.0")

app.include_router(books_router)
app.include_router(issues_router)
app.include_router(reports_router)


@app.get("/")
def root():
    return {"message": "Library Management System API", "docs": "/docs"}