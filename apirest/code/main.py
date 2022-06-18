from fastapi import FastAPI
import sqlite3
from typing import List
from pydantic import BaseModel
import requests

class Respuesta(BaseModel):
    message: str

class Clientes(BaseModel):
    id_cliente: int
    nombre: str
    email: str
class ClienteIn(BaseModel):
    nombre : str
    email : str

app = FastAPI()

@app.get("/", response_model=Respuesta)
async def index():
    return {"message": "API REST"}

@app.get("/clientes/",)
async def clientes():
    with sqlite3.connect('code/sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes")
        response = cursor.fetchall()
        return response

@app.get("/clientes/{id_cliente}", response_model=Clientes)
async def clientes_id(id_cliente: int):
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes WHERE id_cliente = {}".format(id_cliente))
        response = cursor.fetchone()
        return response

@app.get("/clientesLista/", response_model=List[ClienteIn])
async def list_cliente(offset:int=1,limit:int=1):
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM clientes LIMIT {} OFFSET {}".format(offset,limit))
        response = cursor.fetchall()
        return response

@app.post("/clientes/",response_model=Respuesta)
async def post_cliente(nombre:str,email:str): #Usar el basemodel Clientes permite verificar que se reciba id,nombre,email
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("INSERT INTO clientes(nombre,email) VALUES ('{nombre}','{email}')".format(nombre=nombre,email=email))
        response = cursor.fetchone()
        payloadResponse = {"message" : "Cliente Agregado"}
        return payloadResponse

@app.put("/clientes/{id_cliente}",response_model=Respuesta)
async def put_cliente(id_cliente:int,nombre:str,email:str):
    with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("UPDATE clientes SET nombre = '{nombre}', email = '{email}' WHERE id_cliente={id_cliente}".format(nombre=nombre,email=email,id_cliente=id_cliente))
        response = cursor.fetchone()
        putResponse = {"message" : "Cliente Actualizado"}
        return putResponse

@app.delete("/clientes/{id_cliente}",response_model=Respuesta)
async def delete_cliente(id_cliente:int):
   with sqlite3.connect("code/sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente={id_cliente}".format(id_cliente=id_cliente))
        response = cursor.fetchone()
        deleteResponse = {"message" : "Cliente Eliminado"}
        return deleteResponse