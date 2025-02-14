from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_empresa():
    response = client.post("/empresas/", json={"nome": "Empresa X", "cnpj": "12345678901234", "endereco": "Rua Y", "email": "email@empresa.com", "telefone": "123456789"})
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa X"

def test_create_obrigacao():
    response = client.post("/obrigacoes/", json={"nome": "Obrigacao X", "periodicidade": "mensal", "empresa_id": 1})
    assert response.status_code == 200
    assert response.json()["nome"] == "Obrigacao X"