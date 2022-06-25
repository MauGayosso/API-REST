import hashlib  # importa la libreria hashlib
import sqlite3
import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = os.path.join("backend/sql/proyecto.db")

security = HTTPBasic()

"""
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios(
    username TEXT,
    password varchar(32),
    level INTEGER
);

CREATE UNIQUE INDEX index_usuario ON usuarios(username);

INSERT INTO usuarios(username, password, level) VALUES('admin','21232f297a57a5a743894a0e4a801fc3',0);
INSERT INTO usuarios(username, password, level) VALUES('user','ee11cbb19052e40b07aac0ca060c23ee',1);

SELECT * FROM usuarios;
"""


class Usuarios(BaseModel):
    username: str
    level: int


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

@app.get(
    "/usuarios/",
    response_model=List[Usuarios],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Regresa una lista de usuarios",
    description="Regresa una lista de usuarios",
)
async def get_usuarios(level: int = Depends(get_current_level)):
    if level == 0:  # Administrador
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT username, level FROM usuarios")
            usuarios = cursor.fetchall()
            return usuarios
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

# pip3 install black
# pip3 install flakes
# pip3 install isort
# pip3 install mypy
#curl -u username:password URLSERVER