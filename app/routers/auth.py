from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth.jwt_handler import create_access_token

router = APIRouter()

# Simulación de usuarios (en memoria)
fake_users_db = {
    "admin": "admin123"
}

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(user: UserLogin):
    if user.username in fake_users_db and fake_users_db[user.username] == user.password:
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")
