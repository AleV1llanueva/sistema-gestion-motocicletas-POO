from fastapi import APIRouter, Request
from models.empleado import Empleado
from controllers.empleado import create_empleado, get_empleados, delete_empleado
from utils.security import validateadmin

router = APIRouter()

@router.post("/empleados", response_model=dict, tags=["Empleados"])
async def create_empleado_endpoint(request:Request, empleado:Empleado) -> dict:
    return await create_empleado(empleado)

@router.delete("/empleados/{empleado_id}", response_model=Empleado, tags=["Empleados"])
async def create_empleado_endpoint(request:Request, empleado_id:str) -> Empleado:
    return await delete_empleado(empleado_id)

@router.get("/empleados", response_model=dict, tags=["Empleados"])
async def get_empleados_endpoint(request:Request, telefono:str=None) -> dict:
    return await get_empleados(telefono)