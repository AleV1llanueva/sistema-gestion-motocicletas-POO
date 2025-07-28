import os #Cargar las variables de entorno
import uvicorn
from fastapi import FastAPI, Request
from typing import Union
from dotenv import load_dotenv
from pymongo import MongoClient

from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

from controllers.users import create_user, login
from models.users import User
from models.login import Login

#from routers.users import router as users_router
from routers.brand import router as brands_router
from routers.employee_type import router as employee_types_router
from routers.motorcycle import router as motorcycles_router
from routers.tipo_mantenimiento import router as tipo_mantenimiento_router
from routers.mantenimiento import router as mantenimiento_router
from routers.ingreso_moto import router as ingreso_moto_router 

from routers.empleado import router as empleados_router

from utils.security import validateuser, validateadmin
        


app = FastAPI()
load_dotenv()

URI = os.getenv("URI");

app.include_router(empleados_router)

app.include_router(ingreso_moto_router) # Incluye el router de ingreso de motos en la aplicación FastAPI
app.include_router(tipo_mantenimiento_router) # Incluye el router de tipo de mantenimiento en la aplicación FastAPI
app.include_router(mantenimiento_router) # Incluye el router de mantenimiento en la aplicación FastAPI
app.include_router(brands_router) # Incluye el router de marcas en la aplicación FastAPI
app.include_router(motorcycles_router) # Incluye el router de motocicletas en la aplicación FastAPI
app.include_router(employee_types_router) # Incluye el router de tipos de empleados en la aplicación FastAPI

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
@validateadmin
async def example_admin_endpoint(request: Request):
    return {
        "message": "Este es un ejemplo de endpoint para administradores",
        "email": request.state.email
    }

@app.get("/exampleuser")
@validateuser
async def example_user_endpoint(request: Request):
    return {
        "message": "Este es un ejemplo de endpoint para usuarios"
        ,"email": request.state.email
            }

#decorador es una funcion que recibe otra funcion como parametro, y devuelve una nueva funcion que envuelve la original
#El decorador validateuser se utiliza para validar el token JWT y extraer la información del usuario del token.


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")