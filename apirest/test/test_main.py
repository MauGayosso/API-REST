from fastapi.testclient import TestClient
from code.main import app
import requests
import json
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

def test_ClientesById():
    response = clientes.get('/clientes/1')
    data = {"id_cliente":1,"nombre":"Juan","email":"juan@gmail.com"}
    assert response.status_code == 200
    assert response.json() == data

def test_payload_Clientes():
    payload = {"nombre":"Lucas", "email": "lucas@gmail.com"}
    response = clientes.post("/clientes/", params=payload)
    payloadResponse = {"message" : "Cliente Agregado"}
    assert response.status_code == 200
    assert response.json() == payloadResponse
def test_put_Clientes():
    payload = {"nombre" : "Anahi", "email" : "anahi@gmail.com"}
    response = clientes.put("/clientes/9",params=payload)
    putResponse = {"message" : "Cliente Actualizado"}
    assert response.status_code == 200
    assert response.json() == putResponse
    
def test_delete_Clientes():
    response = clientes.delete("/clientes/4")
    deleteResponse = {"message" : "Cliente Eliminado"}
    assert response.status_code == 200
    assert response.json() == deleteResponse
