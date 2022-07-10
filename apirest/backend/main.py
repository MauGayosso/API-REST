from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

import hashlib
import os
import sqlite3
import requests

# Importar URL DB

DATABASE_URL = os.path.join("backend/sql/usuarios.sqlite")

app = FastAPI()
security = HTTPBasic()

# Origins

origins = [
    "https://8000-maugayosso-apirest-uapi6cjdvxz.ws-us53.gitpod.io",
    "https://8080-maugayosso-apirest-uapi6cjdvxz.ws-us53.gitpod.io"
]

# Permisos 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos


class Respuesta(BaseModel):
    message: str


class Clientes(BaseModel):
    id_cliente: int
    nombre: str
    email: str


class ClienteIn(BaseModel):
    nombre: str
    email: str


def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),
        )
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0]


# Endpoint 3.1
@app.get("/", response_model=Respuesta)
async def index():
    return {"message": "API REST"}


# Endpoint 3.2
@app.get(
    "/clientes/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa una lista de clientes",
    description="Regresa una lista de clientes",
)
async def clientes(level: int = Depends(get_current_level)):
    if level == 1:
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes")
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso",
            headers={"WWW-Authenticate": "Basic"},
        )


# Endpoint 3.3
@app.get(
    "/clientes/{id_cliente}",
    response_model=Clientes,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa un cliente con un id especifico",
    description="Regresa un cliente con un id especifico",
)
async def clientes_id(id_cliente: int, level: int = Depends(get_current_level)):
    if (
        level == 1
    ):  # 0 / 1 - Dependera a que tipo de usuario se le dan permisos en este caso 1 es para brindar los permisos a los usuarios con nivel 1
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM clientes WHERE id_cliente = {}".format(id_cliente)
            )
            response = cursor.fetchone()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso",
            headers={"WWW-Authenticate": "Basic"},
        )


# Limit regresa el numero de datos que se le indican limit:int=1
# Offset indica el numero de la primer columna para hacer el return offset:int=1
@app.get(
    "/clientesLista/",
    response_model=List[ClienteIn],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa una lista con la cantidad de elementos especificos",
    description="Regresa una lista con la cantidad de elementos especificos",
)
async def list_cliente(
    offset: int = 1, limit: int = 1, level: int = Depends(get_current_level)
):
    if level == 1:
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM clientes LIMIT {} OFFSET {}".format(offset, limit)
            )
            response = cursor.fetchall()
            return response


# Enpoint 3.4
@app.post(
    "/clientes/",
    response_model=Respuesta,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Permite insertar un nuevo valor",
    description="Permite insertar un nuevo valor",
)  # Usar el basemodel respuestas permite regresar el mensaje de response al test
# Obtener los datos enviados del test
async def post_cliente(cliente : ClienteIn, level: int = Depends(get_current_level)
):
    if level == 1:
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO clientes(nombre,email) VALUES ('{}','{}')".format(
                    cliente.nombre,cliente.email
                )
            )
            response = cursor.fetchone()
            payloadResponse = {"message": "Cliente Agregado"}
            return payloadResponse
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso",
            headers={"WWW-Authenticate": "Basic"},
        )


# Endpoint 3.5
@app.put(
    "/clientes/{id_cliente}",
    response_model=Respuesta,
    summary="Permite actualizar un registro segun el id obtenido",
    description="Permite actualizar un registro segun el id obtenido",
)
async def put_cliente(
    put_cliente : Clientes, level: int = Depends(get_current_level)
):
    if level == 1:
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE clientes SET nombre = '{}', email = '{}' WHERE id_cliente={}".format(
                    put_cliente.nombre,put_cliente.email,put_cliente.id_cliente
                )
            )
            response = cursor.fetchone()
            putResponse = {"message": "Cliente Actualizado"}
            return putResponse
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso",
            headers={"WWW-Authenticate": "Basic"},
        )


# Endoint 3.6
@app.delete(
    "/clientes/{id_cliente}",
    response_model=Respuesta,
    summary="Permite eliminar un registro por un id obtenido",
    description="Permite eliminar un registro por un id obtenido",
)
async def delete_cliente(id_cliente: int, level: int = Depends(get_current_level)):
    if level == 1:
        with sqlite3.connect("backend/sql/clientes.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM clientes WHERE id_cliente={}".format(id_cliente)
            )
            response = cursor.fetchone()
            deleteResponse = {"message": "Cliente Eliminado"}
            return deleteResponse
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a este recurso",
            headers={"WWW-Authenticate": "Basic"},
        )
