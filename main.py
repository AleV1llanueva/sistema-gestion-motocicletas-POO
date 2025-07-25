import os #Cargar las variables de entorno
import uvicorn
from fastapi import FastAPI
from typing import Union
from dotenv import load_dotenv
from pymongo import MongoClient

from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

from controllers.users import create_user, login
from models.users import User
from models.login import Login
        


app = FastAPI()
load_dotenv()

URI = os.getenv("URI");

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/users")
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

@app.post("/login") #Este endpoint como verbo se acepta porque es mas de sistema que de recurso
async def login_access(l: Login, ):
    return await login(l)

@app.get("/exampleadmin")
async def example_admin_endpoint():
    return {"message": "Este es un ejemplo de endpoint para administradores"}

@app.get("/exampleuser")
async def example_user_endpoint():
    return {"message": "Este es un ejemplo de endpoint para usuarios"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")