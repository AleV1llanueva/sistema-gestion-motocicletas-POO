from fastapi import APIRouter, HTTPException, Request
from models.modelo import Modelo
from controllers.modelo import get_modelo_by_id, get_modelos, update_modelo, create_modelo, delete_modelo
from utils.security import validateadmin

router = APIRouter() 

@router.post("/modelos", response_model=Modelo, tags=["Modelos"])
@validateadmin
async def create_modelo_endpoint(request: Request, modelo: Modelo) -> Modelo:
    return await create_modelo(modelo)

@router.get("/modelos", response_model=list[Modelo], tags=["Modelos"]) # Obtiene todas las modelos
async def get_modelos_endpoint(request: Request, ) -> list[Modelo]:
    return await get_modelos()

@router.get("/modelos/{modelo_id}", response_model=Modelo, tags=["Modelos"]) # Obtiene una modelo por su ID
async def get_modelo_by_id_endpoint(request: Request, modelo_id: str) -> Modelo:
    return await get_modelo_by_id(modelo_id)

@router.put("/modelos/{modelo_id}", response_model=Modelo, tags=["Modelos"]) # Actualiza una modelo por su ID
@validateadmin
async def update_modelo_endpoint(request: Request, modelo_id: str, modelo: Modelo) -> Modelo:
    return await update_modelo(modelo_id, modelo)

@router.delete("/modelos/{modelo_id}", tags=["Modelos"]) # Elimina una modelo por su ID
@validateadmin
async def delete_modelo_endpoint(request: Request, modelo_id: str) -> None:
    return await delete_modelo(modelo_id)