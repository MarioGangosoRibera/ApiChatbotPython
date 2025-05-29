from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.squemas.predict import PreguntaRequest
from app.db.database import SessionLocal
from app.db import models
from app.model import predecir_categoria
from app.auth.jwt_handler import verify_token

router = APIRouter()

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    user = verify_token(token.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/ping")
def ping():
    return {"message": "API funcionando correctamente"}

@router.get("/prueba")
def prueba():
    return {"message": "Esta es una ruta de prueba"}

@router.post("/predict")
def predict(pregunta: PreguntaRequest, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        categoria = predecir_categoria(pregunta.pregunta)
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al predecir la categoría")

    if not categoria:
        raise HTTPException(status_code=400, detail="No se pudo clasificar la pregunta")

    nueva_prediccion = models.Prediccion(pregunta=pregunta.pregunta, categoria=categoria)
    db.add(nueva_prediccion)
    db.commit()
    db.refresh(nueva_prediccion)

    return {
        "pregunta": pregunta.pregunta,
        "categoria": categoria
    }
