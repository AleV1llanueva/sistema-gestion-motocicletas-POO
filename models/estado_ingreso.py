from pydantic import BaseModel, Field
from typing import Optional
import re

class estado_ingreso(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID del estado de ingreso, generado automáticamente por MongoDB"
    )
    
    id_ingreso_moto: str = Field(
        description="ID del ingreso de la motocicleta al que pertenece el estado"
    )
    
    id_estado: str = Field(
        description="ID del estado al que pertenece el ingreso de la motocicleta"
    )
    
    fecha_estado: str = Field(
        description="Fecha del estado del ingreso en formato ISO 8601",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$",
        examples=["2023-10-01T12:00:00", "2023-10-02T14:30:00"]
    )