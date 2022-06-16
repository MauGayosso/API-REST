from fastapi.testclient import TestClient
from code.main import app
import requests

clientes = TestClient(app)

def test_index():
    response = clientes.get("/") #Genera un request a la direccion raiz "/"
    data = {"message" : "API REST"} #Lo que se espera recibir
    assert response.status_code == 200
    assert response.json() == data

def test_clientes():
    response = clientes.get("/clientes")
    data = [{"id_cliente":1,"nombre":"Juan","email":"juan@gmail.com"},
    {"id_cliente":2,"nombre":"Roberto","email":"roberto@gmail.com"},
    {"id_cliente":3,"nombre":"Pepe","email":"pepe@gmail.com"}]
    assert response.status_code == 200
    assert response.json() == data
