from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.squemas.predict import PreguntaRequest
from app.db.database import SessionLocal
from app.db import models
from app.model import predecir_categoria

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ping")
def ping():
    return {"message": "API funcionando correctamente"}

@router.get("/prueba")
def prueba():
    return {"message": "Esta es una ruta de prueba"}

@router.post("/predict")
def predict(pregunta: PreguntaRequest, db: Session = Depends(get_db)):
    try:
        categoria = predecir_categoria(pregunta.pregunta)
    #Validacion de errores
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno al predecir la categoría")

    if not categoria:
        raise HTTPException(status_code=400, detail="No se pudo clasificar la pregunta")

    # Guardar en BD
    nueva_prediccion = models.Prediccion(pregunta=pregunta.pregunta, categoria=categoria)
    db.add(nueva_prediccion)
    db.commit()
    db.refresh(nueva_prediccion)

    return {
        "pregunta": pregunta.pregunta,
        "categoria": categoria
    }