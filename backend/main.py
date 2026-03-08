from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.database import create_tables
from .routers import auth, papers, chat

app = FastAPI(title="ResearchHub AI", version="1.0.0")

# Allow React frontend on port 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables on startup
@app.on_event("startup")
def startup():
    create_tables()

# Include routers
app.include_router(auth.router)
app.include_router(papers.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "ResearchHub AI API is running"}
