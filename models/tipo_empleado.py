from pydantic import BaseModel, Field
from typing import Optional
import re

class TipoEmpleado(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB id"
    )
    
    descripcion: str = Field(
        description="Descripcion del tipo de empleado",
        pattern=r"^[0-9A-Za-zÁÉÍÓÚÑáéíóúñ' -]+$", #Validación de caracteres permitidos (letras, números, espacios, guiones y acentos
        examples=["Gerente", "Supervisor", "Operario"]
    )
