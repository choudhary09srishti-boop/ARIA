from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.auth.router import router as auth_router

load_dotenv()

app = FastAPI(
    title="ARIA Backend",
    description="ARIA - Personal AI Assistant API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"status": "ARIA backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}