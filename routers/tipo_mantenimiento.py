from  fastapi import APIRouter, HTTPException, Request
from models.tipo_mantenimiento import TipoMantenimiento
from controllers.tipo_mantenimiento import (
    create_tipo_mantenimiento,
    get_tipo_mantenimiento_by_id,
    get_tipo_mantenimiento,
    update_tipo_mantenimiento,
    delete_tipo_mantenimiento
)

router = APIRouter()

@router.post("/tipo_mantenimiento", response_model=TipoMantenimiento, tags=["Tipo Mantenimiento"])
async def create_tipo_mantenimiento_endpoint(tipo_mantenimiento: TipoMantenimiento):
    return await create_tipo_mantenimiento(tipo_mantenimiento)

@router.get("/tipo_mantenimiento", response_model=list[TipoMantenimiento], tags=["Tipo Mantenimiento"]) 
async def get_tipos_mantenimiento_endpoint(request: Request, ) -> list[TipoMantenimiento]:
    return await get_tipo_mantenimiento()

@router.get("/tipo_mantenimiento/{tipo_mantenimiento_id}", response_model=TipoMantenimiento, tags=["Tipo Mantenimiento"])
async def get_tipo_mantenimiento_by_id_endpoint(tipo_mantenimiento_id: str):
    return await get_tipo_mantenimiento_by_id(tipo_mantenimiento_id)

@router.put("/tipo_mantenimiento/{tipo_mantenimiento_id}", response_model=TipoMantenimiento, tags=["Tipo Mantenimiento"]) 
async def update_tipo_mantenimiento_endpoint(request: Request, tipo_mantenimiento_id: str, tipo_mantenimiento: TipoMantenimiento) -> TipoMantenimiento:
    return await update_tipo_mantenimiento(tipo_mantenimiento_id, tipo_mantenimiento)

@router.delete("/tipo_mantenimiento/{tipo_mantenimiento_id}", tags=["Tipo Mantenimiento"])
async def delete_tipo_mantenimiento_endpoint(request: Request, tipo_mantenimiento_id: str) -> None:
    return await delete_tipo_mantenimiento(tipo_mantenimiento_id)
