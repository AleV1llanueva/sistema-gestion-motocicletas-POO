from fastapi import APIRouter, HTTPException, Request
from models.ingreso_moto import IngresoMoto
from controllers.ingreso_moto import (
    create_ingreso_moto,
    get_ingreso_moto_by_id,
)
from utils.mongodb import get_collection
from utils.security import validateuser

router = APIRouter()

@router.post("/ingreso_moto", response_model=IngresoMoto, tags=["Ingreso Moto"])
@validateuser
async def create_ingreso_moto_endpoint(ingreso_moto: IngresoMoto):
    return await create_ingreso_moto(ingreso_moto)

@router.get("/ingreso_moto/{ingreso_moto_id}", response_model=dict, tags=["Ingreso Moto"])
@validateuser
async def get_ingreso_moto_by_id_endpoint( request: Request, ingreso_moto_id: str) -> dict:
    return await get_ingreso_moto_by_id(ingreso_moto_id)
