from  fastapi import APIRouter, HTTPException, Request
from models.tipo_mantenimiento import TipoMantenimiento
from controllers.tipo_mantenimiento import (
    create_tipo_mantenimiento,
    get_tipo_mantenimiento_by_id,
)

router = APIRouter()

@router.post("/tipo_mantenimiento", response_model=TipoMantenimiento, tags=["Tipo Mantenimiento"])
async def create_tipo_mantenimiento_endpoint(tipo_mantenimiento: TipoMantenimiento):
    return await create_tipo_mantenimiento(tipo_mantenimiento)

@router.get("/tipo_mantenimiento/{tipo_mantenimiento_id}", response_model=TipoMantenimiento, tags=["Tipo Mantenimiento"])
async def get_tipo_mantenimiento_by_id_endpoint(tipo_mantenimiento_id: str):
    return await get_tipo_mantenimiento_by_id(tipo_mantenimiento_id)
