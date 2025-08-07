import pytest #Investigar para que sirve
from utils.mongodb import get_mongo_client, t_connection, get_collection
import os
from dotenv import load_dotenv

load_dotenv() #Leer la variables de ambiente

def test_env_variables(): #Testear las variables del entorno
    mongodb_uri = os.getenv("MONGODB_URI")
    assert mongodb_uri is not None, "MONGODB_URI no esta configurado"
    print(f"Database: {mongodb_uri}")
    
def test_connect():
    try:
        connection_result = t_connection()
        assert connection_result is True, "La conexion a la base de datos fallo"
    except Exception as e:
        pytest.fail(f"Error en la conexion a MongoDB {str(e)}")
    
    
def test_mongo_client() :
    try:
        client = get_mongo_client() #Esto retorna un objeto por eso ponemos si es None
        assert client is not None, "El cliente de MongoDB is None"
    except Exception as e:
        pytest.fail(f"Error en el llamado del cliente de MongoDB {str(e)}")
        
def test_get_collection() :
    try:
        coll_users = get_collection("users") #Esto retorna un objeto por eso ponemos si es None
        assert coll_users is not None, "Error al obtener la coleccion de users"
    except Exception as e:
        pytest.fail(f"Error en el llamado del cliente de MongoDB {str(e)}")
        
#Hacer todas las prubeas unitarias de las apis ------