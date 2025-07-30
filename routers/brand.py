from fastapi import APIRouter, HTTPException, Request
from models.brand import Brand
from controllers.brand import create_brand, get_brands, get_brand_by_id, update_brand, delete_brand
from utils.security import validateadmin

router = APIRouter() 

@router.post("/brands", response_model=Brand, tags=["Brands"])
@validateadmin
async def create_brand_endpoint(request: Request, brand: Brand) -> Brand:
    return await create_brand(brand)

@router.get("/brands", response_model=list[Brand], tags=["Brands"]) # Obtiene todas las marcas
async def get_brands_endpoint(request: Request, ) -> list[Brand]:
    return await get_brands()

@router.get("/brands/{brand_id}", response_model=Brand, tags=["Brands"]) # Obtiene una marca por su ID
async def get_brand_by_id_endpoint(request: Request, brand_id: str) -> Brand:
    return await get_brand_by_id(brand_id)

@router.put("/brands/{brand_id}", response_model=Brand, tags=["Brands"]) # Actualiza una marca por su ID
@validateadmin
async def update_brand_endpoint(request: Request, brand_id: str, brand: Brand) -> Brand:
    return await update_brand(brand_id, brand)

@router.delete("/brands/{brand_id}", tags=["Brands"]) # Elimina una marca por su ID
@validateadmin
async def delete_brand_endpoint(request: Request, brand_id: str) -> None:
    return await delete_brand(brand_id)