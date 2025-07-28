from typing import Optional
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId
import re

class TipoMantenimiento(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID del tipo de mantenimiento, generado automáticamente por MongoDB"
    )
    
    description: str = Field(
        description="Descripción del tipo de mantenimiento",
        pattern=r"^[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Cambio de aceite", "Revisión de frenos", "Ajuste de cadena"]
    )
    
    active: bool = Field(
        default=True,
        description="Indica si el tipo de mantenimiento está activo o no"
    )