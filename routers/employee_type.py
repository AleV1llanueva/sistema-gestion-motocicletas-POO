from fastapi import APIRouter, HTTPException, Request
from models.tipo_empleado import TipoEmpleado
from controllers.tipo_empleado import get_tipo_empleado_by_id, get_tipo_empleados, create_tipo_empleado, delete_tipo_empleado, update_tipo_empleado
from utils.security import validateadmin

router = APIRouter() 

@router.post("/tipos_empleado", response_model=TipoEmpleado, tags=["Tipos Empleado"])
@validateadmin
async def create_tipo_empleado_endpoint(request: Request, tipo_empleado: TipoEmpleado) -> TipoEmpleado:
    return await create_tipo_empleado(tipo_empleado)

@router.get("/tipos_empleado", response_model=list[TipoEmpleado], tags=["Tipos Empleado"]) # Obtiene todos los tipos de empleados
async def get_tipos_empleado_endpoint(request: Request, ) -> list[TipoEmpleado]:
    return await get_tipo_empleados()

@router.get("/tipos_empleado/{tipo_empleado_id}", response_model=TipoEmpleado, tags=["Tipos Empleado"]) # Obtiene un tipo de empleado por su ID
async def get_tipo_empleado_by_id_endpoint(request: Request, tipo_empleado_id: str) -> TipoEmpleado:
    return await get_tipo_empleado_by_id(tipo_empleado_id)

@router.put("/tipos_empleado/{tipo_empleado_id}", response_model=TipoEmpleado, tags=["Tipos Empleado"]) # Actualiza un tipo de empleado por su ID
@validateadmin
async def update_tipo_empleado_endpoint(request: Request, tipo_empleado_id: str, tipo_empleado: TipoEmpleado) -> TipoEmpleado:
    return await update_tipo_empleado(tipo_empleado_id, tipo_empleado)

@router.delete("/tipos_empleado/{tipo_empleado_id}", tags=["Tipos Empleado"]) # Elimina un tipo de empleado por su ID
@validateadmin
async def delete_tipo_empleado_endpoint(request: Request, tipo_empleado_id: str) -> None:
    return await delete_tipo_empleado(tipo_empleado_id)