from pydantic import BaseModel, Field
from typing import Optional
import re

class Brand(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB id"
    )
    
    description: str = Field(
        description="Descripcion de la marca",
        pattern=r"^[0-9A-Za-zÁÉÍÓÚÑáéíóúñ' -]+$", #Validación de caracteres permitidos (letras, números, espacios, guiones y acentos
        examples=["Yamaha", "Honda", "Suzuki", "Kawasaki", "BMW", "Ducati", "Harley-Davidson", "Triumph", "KTM", "Aprilia"]
    )
    
    active: bool = Field (
        default=True,
        description="Estado activo de la marca"
    )
