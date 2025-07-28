from fastapi import APIRouter, HTTPException, Request
from models.tipo_empleado import TipoEmpleado
from controllers.tipo_empleado import get_tipo_empleado_by_id, get_tipo_empleados, create_tipo_empleado, delete_tipo_empleado, update_tipo_empleado
from utils.security import validateadmin

router = APIRouter() # Define un router para agrupar las rutas relacionadas con tipos de empleados

#un router es una forma de agrupar rutas relacionadas en FastAPI, lo que permite organizar mejor el código y reutilizarlo en diferentes partes de la aplicación.

#response_model es un parámetro que se utiliza para especificar el modelo de respuesta que se espera devolver en la respuesta de la API. Esto permite a FastAPI generar automáticamente la documentación de la API y validar las respuestas.
#tags es un parámetro que se utiliza para agrupar las rutas en la documentación de la API. Esto permite organizar mejor la documentación y hacerla más legible.
# Este archivo define las rutas relacionadas con las marcas de vehículos

#el "-> Brand" indica que la función devuelve un objeto de tipo Brand, lo que permite a FastAPI generar automáticamente la documentación de la API y validar las respuestas.

#await es una palabra clave en Python que se utiliza para esperar a que una función asíncrona se complete. En este caso, se utiliza para esperar a que las funciones de la capa de controladores (controllers) se completen antes de devolver la respuesta.

@router.post("/tipos_empleado", response_model=TipoEmpleado, tags=["Tipos Empleado"])

async def create_tipo_empleado_endpoint(request: Request, tipo_empleado: TipoEmpleado) -> TipoEmpleado:
    return await create_tipo_empleado(tipo_empleado)

@router.get("/tipos_empleado", response_model=list[TipoEmpleado], tags=["Tipos Empleado"]) # Obtiene todos los tipos de empleados
async def get_tipos_empleado_endpoint(request: Request, ) -> list[TipoEmpleado]:
    return await get_tipo_empleados()

@router.get("/tipos_empleado/{tipo_empleado_id}", response_model=TipoEmpleado, tags=["Tipos Empleado"]) # Obtiene un tipo de empleado por su ID
async def get_tipo_empleado_by_id_endpoint(request: Request, tipo_empleado_id: str) -> TipoEmpleado:
    return await get_tipo_empleado_by_id(tipo_empleado_id)

@router.put("/tipos_empleado/{tipo_empleado_id}", response_model=TipoEmpleado, tags=["Tipos Empleado"]) # Actualiza un tipo de empleado por su ID
async def update_tipo_empleado_endpoint(request: Request, tipo_empleado_id: str, tipo_empleado: TipoEmpleado) -> TipoEmpleado:
    return await update_tipo_empleado(tipo_empleado_id, tipo_empleado)

@router.delete("/tipos_empleado/{tipo_empleado_id}", tags=["Tipos Empleado"]) # Elimina un tipo de empleado por su ID
async def delete_tipo_empleado_endpoint(request: Request, tipo_empleado_id: str) -> None:
    return await delete_tipo_empleado(tipo_empleado_id)