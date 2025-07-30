from pydantic import BaseModel, Field
from typing import Optional
import re

class Modelo(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB id"
    )
    
    id_motocicleta: str = Field(
        description="Id de la motocicleta a la que pertenece el modelo"
    )
    
    id_categoria: str = Field(
        description="Id de la categoria a la que pertence el modelo de la motocicleta"
    )
    
    nombre: str = Field (
        description="Nombre del modelo de motocicleta",
        examples=["250F", "450R"]
    )