from pydantic import BaseModel, Field
from typing import Optional
import re

class Motorcycle(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB id"
    )
    
    id_marca: str = Field(
        description="MongoDB id de la marca",
    )
    
    name: str = Field(
        description="Nombre de la motocicleta",
        pattern=r"^[0-9A-Za-zÁÉÍÓÚÑáéíóúñ' -]+$", #Validación de caracteres permitidos (letras, números, espacios, guiones y acentos
        examples=["YZ", "WR", "CBR", "Ninja", "XTZ"] # Ejemplos de nombres válidos
    )
    
    active: bool = Field(
        default=True,
        description="Estado activo de la motocicleta"
    )
