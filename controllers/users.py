from bson import ObjectId
import os, logging, firebase_admin, requests

from fastapi import HTTPException
from firebase_admin import credentials, auth as firebase_auth

from models.login import Login
from models.users import User

from utils.security import create_jwt_token
from utils.mongodb import get_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cred = credentials.Certificate("secrets/motocicleta-secret.json")
firebase_admin.initialize_app(cred)

async def create_user(user: User) -> User:
    user_record = {}
    try:
        user_record = firebase_auth.create_user(
            email=user.email,
            password=user.password
        )
    except Exception as e:
        logger.warning(e)
        raise HTTPException(status_code=400, detail="Error al registrar el usuario en firebase")
    
    try:
        coll = get_collection("users")

        # Aunque se manden en el payload igual los excluimos ya que sabes el 
        # state inicial cuando se crea el usuario.

        new_user = User(
            name=user.name
            , lastname=user.lastname
            , email=user.email
            , password=user.password
        )

        user_dict = new_user.model_dump(exclude={"id", "password"})
        inserted = coll.insert_one(user_dict)
        new_user.id = str(inserted.inserted_id)
        new_user.password = "*********"  # Mask the password in the response
        return new_user
        
    except Exception as e:
        firebase_auth.delete_user(user_record.uid)
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def login(user: Login) -> dict:
    api_key = os.getenv("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": user.email,
        "password": user.password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    response_data = response.json()
    
    if "error" in response_data:
        raise HTTPException(
            status_code=400,
            detail="Error al autenticar el usuario"
        )
        
    coll = get_collection("users")
    user_info = coll.find_one({"email": user.email})
    
    if not user_info:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado en la bnase de datos"
        )
        
    return {
        "message": "Usuario autenticado correctamente",
        "idToken": create_jwt_token(
            user_info["name"],
            user_info["lastname"],
            user_info["email"],
            user_info["active"],
            user_info["admin"],
            str(user_info["_id"])
        )
    }
    
async def inactivate_user(user_id:str, user: User) -> User:
    coll = get_collection("users")
    result = coll.find_one({"_id": ObjectId(user_id)})
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # Actualiza el estado del usuario a inactivo
    result = coll.update_one({"_id": ObjectId(user_id)}, {"$set": {"active": False}})
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=400,
            detail="No se pudo actualizar el estado del usuario"
        )

    coll_empleado = get_collection("empleados")  # Obtiene la colección de empleados desde MongoDB
    # Verifica si hay empleados asociados a este usuario
    existing_empleado = coll_empleado.find_one({"id_usuario": user_id})
    if existing_empleado:
        #Si existe un empleado asociado a este usuario, lo inactiva
        coll_empleado.update({"_id": existing_empleado["_id"]}, {"$set": {"activo": False}})
        existing_empleado["activo"] = False
        
    user.id = user_id
    user.active = False
    return user

async def get_user_by_id(user_id: str) -> User:
    coll = get_collection("users")
    user_data = coll.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user_data["id"] = str(user_data["_id"])
    user_data.pop("_id", None)
    user_data["password"] = "*********"
    return User(**user_data)

#Pipelines
#Hacer el get por id
# get de todos que si es admin de todos y que si no solo de la informacion del usuario