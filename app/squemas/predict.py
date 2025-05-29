from pydantic import BaseModel, Field

class PreguntaRequest(BaseModel):
#Minimo 5 caracteres y maximo 200
    pregunta: str = Field(..., min_length=5, max_length=200, description="Pregunta a clasificar")
