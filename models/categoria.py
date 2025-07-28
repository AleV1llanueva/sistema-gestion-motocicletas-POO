from pydantic import BaseModel, Field
from typing import Optional
import re

class Categoria(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID de la categoría, generado automáticamente por MongoDB"
    )
    
    descripcion: str = Field(
        description="Descripción de la categoría",
        examples=["Deportiva", "Cruiser", "Touring", "Scooter", "Enduro"]
    )