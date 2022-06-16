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

app = FastAPI()

@app.get("/", response_model=Respuesta)
async def index():
    return {"message": "API REST"}

@app.get("/clientes/",)
async def clientes():
    with sqlite3.connect('code/sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM clientes')
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