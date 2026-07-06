from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas.user import UserCreate
from app.config.settings import settings
from supabase import create_client

router = APIRouter(prefix="/auth", tags=["auth"])

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
async def signup(user: UserCreate):
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {"data": {"full_name": user.full_name}}
        })
        return {"message": "User created successfully", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: LoginRequest):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return {"access_token": response.session.access_token, "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))