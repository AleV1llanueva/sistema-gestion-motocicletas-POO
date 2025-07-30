from fastapi import APIRouter, HTTPException, Request
from models.matenimiento import Mantenimiento
from controllers.mantenimiento import (
    create_mantenimiento,
    get_mantenimiento_by_id,
)
from utils.security import validateuser

router = APIRouter()

@router.post("/mantenimiento", response_model=Mantenimiento, tags=["Mantenimiento"])
@validateuser
async def create_mantenimiento_endpoint(mantenimiento: Mantenimiento):
    return await create_mantenimiento(mantenimiento)

@router.get("/mantenimiento/{mantenimiento_id}", response_model=Mantenimiento, tags=["Mantenimiento"])
@validateuser
async def get_mantenimiento_by_id_endpoint(mantenimiento_id: str):
    return await get_mantenimiento_by_id(mantenimiento_id)





















