from pydantic import BaseModel, Field
from typing import Optional
import re

class Estado(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID del estado, generado automáticamente por MongoDB"
    )
    
    descripcion: str = Field(
        description="Descripción del estado",
        examples=["En espera", "En reparación", "Listo para entrega", "Entregado"]
    )