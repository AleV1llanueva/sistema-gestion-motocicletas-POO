from fastapi import APIRouter, HTTPException, Request
from models.brand import Brand
from controllers.brand import create_brand, get_brands, get_brand_by_id, update_brand, delete_brand
from utils.security import validateadmin

router = APIRouter() # Define un router para agrupar las rutas relacionadas con marcas

#un router es una forma de agrupar rutas relacionadas en FastAPI, lo que permite organizar mejor el código y reutilizarlo en diferentes partes de la aplicación.

#response_model es un parámetro que se utiliza para especificar el modelo de respuesta que se espera devolver en la respuesta de la API. Esto permite a FastAPI generar automáticamente la documentación de la API y validar las respuestas.
#tags es un parámetro que se utiliza para agrupar las rutas en la documentación de la API. Esto permite organizar mejor la documentación y hacerla más legible.
# Este archivo define las rutas relacionadas con las marcas de vehículos

#el "-> Brand" indica que la función devuelve un objeto de tipo Brand, lo que permite a FastAPI generar automáticamente la documentación de la API y validar las respuestas.

#await es una palabra clave en Python que se utiliza para esperar a que una función asíncrona se complete. En este caso, se utiliza para esperar a que las funciones de la capa de controladores (controllers) se completen antes de devolver la respuesta.

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