from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from os import stat
from urllib import response
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, HTTPException, status, Depends, Security, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
import pyrebase
from fastapi.middleware.cors import CORSMiddleware

import hashlib
import os
import sqlite3
import requests

# Importar URL DB

DATABASE_URL = os.path.join("backend/sql/usuarios.sqlite")

app = FastAPI()
security = HTTPBasic()
securityBasic = HTTPBasic()
securityBearer = HTTPBearer()

# Origins

origins = [
    "https://8080-maugayosso-apirest-uapi6cjdvxz.ws-us59.gitpod.io/",
    "https://8000-maugayosso-apirest-uapi6cjdvxz.ws-us59.gitpod.io/"
]

# Permisos 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase config

firebaseConfig = {
    "apiKey": "AIzaSyC1gT-0_-HcZq3ukC50hPF_20B5voJYzPg",
    "authDomain": "fir-pyrebase-b3338.firebaseapp.com",
    "databaseURL": "https://fir-pyrebase-b3338-default-rtdb.firebaseio.com",
    "projectId": "fir-pyrebase-b3338",
    "storageBucket": "fir-pyrebase-b3338.appspot.com",
    "messagingSenderId": "656691641634",
    "appId": "1:656691641634:web:e7b45375247c5eeac7f97b",
    "measurementId": "G-VFSQ56E7N1",
}

firebase = pyrebase.initialize_app(firebaseConfig)

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

class UserIN(BaseModel):
    username: str
    password: str


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
async def clientes_id(id_cliente: int, credentials : HTTPAuthorizationCredentials = Depends(securityBearer)):
    auth = firebase.auth()
    db = firebase.database()
    user = auth.get_account_info(credentials.credentials)
    uid = user["users"][0]["localId"]
    lvlUser =  db.child("users").child(uid).child("Nivel").get().val()
    print(lvlUser)
    if lvlUser  == 1:
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
async def post_cliente(cliente : ClienteIn, credentials : HTTPAuthorizationCredentials = Depends(securityBearer)
):
    auth = firebase.auth()
    db = firebase.database()
    user = auth.get_account_info(credentials.credentials)
    uid = user["users"][0]["localId"]
    lvlUser =  db.child("users").child(uid).child("Nivel").get().val()
    print(lvlUser)
    if lvlUser  == 1:
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
    put_cliente : Clientes, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    auth = firebase.auth()
    db = firebase.database()
    user = auth.get_account_info(credentials.credentials)
    uid = user["users"][0]["localId"]
    lvlUser =  db.child("users").child(uid).child("Nivel").get().val()
    if lvlUser  == 1:
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
async def delete_cliente(id_cliente: int, credentials: HTTPAuthorizationCredentials = Depends(securityBearer)):
    auth = firebase.auth()
    db = firebase.database()
    user = auth.get_account_info(credentials.credentials)
    uid = user["users"][0]["localId"]
    lvlUser =  db.child("users").child(uid).child("Nivel").get().val()
    if lvlUser  == 1:
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


# ***** FIREBASE ******
@app.get(
    "/user/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Obtener token",
    description="Obtener token mediante firebase",
    tags=["Auth"],
)
async def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
        email = credentials.username
        password = credentials.password
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        response = {"token": user["idToken"]}

        print(user)
        return response
    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.get(
    "/user/",
    status_code=status.HTTP_201_CREATED,
    summary="Obtener datos",
    description="Obtener datos del usuario",
    tags=["Auth"],
)
async def get_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(securityBearer),
):
    try:
        auth = firebase.auth()
        user = auth.get_account_info(credentials.credentials)
        uid = user["users"][0]["localId"]
        db = firebase.database()
        user_data = db.child("users").child(uid).get().val()
        response = {"user_data": user_data}
        return response
    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post(
    "/user/add",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Agregar usuario",
    description="Agregar usuario",
    tags=["Insert"],
)
async def addUser(usuarios: UserIN):
    auth = firebase.auth()
    db = firebase.database()
    emails = usuarios.username
    passwords = usuarios.password
    
    try:
        user_info = auth.create_user_with_email_and_password(emails, passwords)
        idTokenU = user_info["idToken"]
        user = auth.get_account_info(idTokenU)
        print(user)
        uid = user["users"][0]["localId"]
        mail = user["users"][0]["email"]
        print(uid)
        data = {"email" : mail, "Nivel" : 1}
        results = db.child("users").child(uid).set(data)
        #TERMINA DB
        response = {"user_info": user_info}
        return response
    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@app.post(
    "/user/login",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Inciar Sesion",
    description="Iniciar Sesion",
    tags=["Log In"],
)
async def login(
    usuarioL: UserIN):
    auth = firebase.auth()
    db = firebase.database()
    
    emails = usuarioL.username
    password = usuarioL.password
    
    try:
        user_dat = auth.sign_in_with_email_and_password(emails, password)
        idTokenU = user_dat["idToken"]
        #user = auth.get_account_info(idTokenU)
        #print(user)
        #uid = user["users"][0]["localId"]
        #mail = user["users"][0]["email"]
        #print(uid)
        #data = {"email" : mail, "Nivel" : 1}
        #results = db.child("users").push(data)
        response = {f"user_dat": idTokenU}
        return response
    except Exception as error:
        print(f"Error : {error}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)