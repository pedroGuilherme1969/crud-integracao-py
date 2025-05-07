import pytest
from app.main import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_criar_usuario_valido(client):
    response = client.post("/usuarios", json={
        "nome": "pedro",
        "email": "pedro@gmail.com",
        "senha": "123456",
        "cpf": "12376899911"
    })
    assert response.status_code == 201
    assert response.get_json()["mensagem"] == "Usuário criado com sucesso"

def test_listar_todos_usuarios(client):
    response = client.get("/usuarios")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_buscar_usuario_existente(client):
    cpf = "12376899911"
    client.post("/usuarios", json={
        "nome": "pedro",
        "email": "pedro@gmail.com",
        "senha": "123456",
        "cpf": cpf
    })
    response = client.get(f"/usuarios/{cpf}")
    assert response.status_code == 200
    assert response.get_json()["cpf"] == cpf

def test_buscar_usuario_inexistente(client):
    response = client.get("/usuarios/00000000000")
    assert response.status_code == 404
    assert response.get_json()["erro"] == "Usuário não encontrado"

def test_excluir_usuario_existente(client):
    cpf = "12376899911"
    client.post("/usuarios", json={
        "nome": "pedro",
        "email": "pedro@gmail.com",
        "senha": "123456",
        "cpf": cpf
    })
    response = client.delete(f"/usuarios/{cpf}")
    assert response.status_code == 200
    assert response.get_json()["mensagem"] == "Usuário removido com sucesso"

def test_excluir_usuario_inexistente(client):
    response = client.delete("/usuarios/00000000000")
    assert response.status_code == 404
    assert response.get_json()["erro"] == "Usuário não encontrado"
