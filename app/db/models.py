from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Prediccion(Base):
    __tablename__ = "predicciones"

    id = Column(Integer, primary_key=True, index=True)
    pregunta = Column(String, nullable=False)
    categoria = Column(String, nullable=False)