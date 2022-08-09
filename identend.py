from os import stat
from urllib import response
from fastapi import FastAPI, HTTPException, status, Depends, Security, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
import pyrebase

# Conexion

app = FastAPI()

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

securityBasic = HTTPBasic()
securityBearer = HTTPBearer()


@app.get("/")
async def index():
    return {"message": "AUTH"}


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
    status_code=status.HTTP_202_ACCEPTED,
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
