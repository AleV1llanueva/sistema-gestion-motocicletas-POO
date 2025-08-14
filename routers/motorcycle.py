from fastapi import APIRouter, HTTPException, Request
from models.motorcycle import Motorcycle
from controllers.motorcycle import create_motorcycle, get_motorcycles, get_motorcycle_by_id, update_motorcycle, delete_motorcycle
from utils.security import validateadmin, validateuser

router = APIRouter() # Define un router para agrupar las rutas relacionadas con motocicletas

@router.post("/motorcycles", response_model=Motorcycle, tags=["Motorcycles"])
@validateadmin
async def create_motorcycle_endpoint(request: Request, motorcycle: Motorcycle) -> Motorcycle:
    return await create_motorcycle(motorcycle)

@router.get("/motorcycles", response_model=dict, tags=["Motorcycles"]) # Obtiene todas las motocicletas
@validateuser
async def get_motorcycles_endpoint() -> dict:
    motorcycles = await get_motorcycles()
    return {"motorcycles": motorcycles}

@router.get("/motorcycles/{motorcycle_id}", response_model=Motorcycle, tags=["Motorcycles"]) # Obtiene una motocicleta por su ID
@validateuser
async def get_motorcycle_by_id_endpoint(request: Request, motorcycle_id: str) -> Motorcycle:
    return await get_motorcycle_by_id(motorcycle_id)

@router.put("/motorcycles/{motorcycle_id}", response_model=Motorcycle, tags=["Motorcycles"]) # Actualiza una motocicleta por su ID
@validateadmin
async def update_motorcycle_endpoint(request: Request, motorcycle_id: str, motorcycle: Motorcycle) -> Motorcycle:
    return await update_motorcycle(motorcycle_id, motorcycle)

@router.delete("/motorcycles/{motorcycle_id}", tags=["Motorcycles"]) # Elimina una motocicleta por su ID
@validateadmin
async def delete_motorcycle_endpoint(request: Request, motorcycle_id: str) -> None:
    return await delete_motorcycle(motorcycle_id)