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
from routers.modelo import router as modelo_router
from routers.users import router as users_router

from routers.empleado import router as empleados_router

from utils.security import validateuser, validateadmin
        


app = FastAPI()
load_dotenv()

URI = os.getenv("URI");

app.include_router(users_router)
app.include_router(modelo_router)
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

#Al hacer el release de nuestra aplicacion
@app.get("/health") #Para ver la salud de la api en nuestro servidor, normalmente se utiliza en restful api, es un endpoint para el servidor que correra nuestro aplicacion, para ver como esta nuestro apli
def health_check() :
    try:
        return {
            "status" : "healthy",
            "timestamp" : "2025-08-06",
            "service" : "taller-motoicletas-api",
            "environment" : "production"
        }
    except Exception as e:
        return {"status" : "unhealthy", "error" : str(e)}

@app.get("/ready") #Para testear la conexion con mongodb (para pruebas unitarias)
def readiness_check() :
    try:
        from utils.mongodb import test_connection
        db_status = test_connection()
        return {
            "status" : "ready" if db_status else "not_ready",
            "database" : "connected" if db_status else "disconnected",
            "service" : "taller-motocicletas-api"
        }
    except Exception as e:
        return {"status" : "not_ready", "error" : str(e)}



#decorador es una funcion que recibe otra funcion como parametro, y devuelve una nueva funcion que envuelve la original
#El decorador validateuser se utiliza para validar el token JWT y extraer la información del usuario del token.


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")