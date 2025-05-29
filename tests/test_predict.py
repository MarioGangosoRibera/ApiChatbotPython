import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

def test_predict_success():
    payload = {
        "pregunta": "No puedo conectarme a internet"
    }
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "categoria" in data
    assert "pregunta" in data
    assert data["pregunta"] == payload["pregunta"]

def test_predict_empty():
    payload = {"pregunta": ""}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validación de Pydantic

def test_predict_missing_field():
    payload = {}  # No se envía 'pregunta'
    response = client.post("/predict", json=payload)
    assert response.status_code == 422