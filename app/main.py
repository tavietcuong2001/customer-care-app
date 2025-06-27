from fastapi import FastAPI
from app.routers import chat, issue

app = FastAPI(
    title="Customer Care App"
)

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(issue.router, prefix="/issues", tags=["Issues"])