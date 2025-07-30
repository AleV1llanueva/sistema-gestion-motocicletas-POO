from fastapi import APIRouter, HTTPException, Request
from models.matenimiento import Mantenimiento
from controllers.users import create_user, login, get_user_by_id, inactivate_user
from models.users import User
from models.login import Login

from utils.security import validateuser, validateadmin

router = APIRouter()

@router.post("/users")
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

@router.post("/login")
async def login_access(l: Login, ):
    return await login(l)

@router.get("/users/{user_id}")
@validateadmin
async def get_user_by_id_endpoint(user_id:str) :
    return await get_user_by_id(user_id)

@router.delete("/users/{user_id}")
#@validateadmin
async def inactivate_user_by_id_endpoint(user_id:str) :
    return await inactivate_user(user_id)

# @router.get("/exampleadmin")
# @validateadmin
# async def example_admin_endpoint(request: Request):
#     return {
#         "message": "Este es un ejemplo de endpoint para administradores",
#         "email": request.state.email
#     }
    
    

# @router.get("/exampleuser")
# @validateuser
# async def example_user_endpoint(request: Request):
#     return {
#         "message": "Este es un ejemplo de endpoint para usuarios"
#         ,"email": request.state.email
#             }