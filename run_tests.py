from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Limpar o banco de dados antes dos testes
def clear_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_empresa():
    clear_db()
    response = client.post("/empresas/", json={"nome": "Empresa X", "cnpj": "12345678901234", "endereco": "Rua Y", "email": "email@empresa.com", "telefone": "123456789"})
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa X"
    print("test_create_empresa passed")

def test_create_obrigacao():
    clear_db()
    response = client.post("/empresas/", json={"nome": "Empresa Y", "cnpj": "98765432109876", "endereco": "Rua Z", "email": "email@empresa.com", "telefone": "987654321"})
    assert response.status_code == 200
    empresa_id = response.json()["id"]

    response = client.post("/obrigacoes/", json={"nome": "Obrigacao X", "periodicidade": "mensal", "empresa_id": empresa_id})
    assert response.status_code == 200
    assert response.json()["nome"] == "Obrigacao X"
    print("test_create_obrigacao passed")

if __name__ == "__main__":
    test_create_empresa()
    test_create_obrigacao()
    print("All tests passed")