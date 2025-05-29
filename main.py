from fastapi import FastAPI
from app.routers import predict
from app.db.database import Base, engine
from app.db import models
import uvicorn
from app.routers import predict, auth

app = FastAPI(
    title="API de Clasificación de Preguntas",
    description="Clasifica preguntas en categorías: OK, AYUDA, SERVICIO_TECNICO",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(predict.router)

# Ruta raíz para evitar 404 en /
@app.get("/")
async def root():
    return {"message": "API de Clasificación de Preguntas está funcionando"}


app.include_router(auth.router)
app.include_router(predict.router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)