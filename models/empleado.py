from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Empleado(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID del empleado, generado automáticamente por MongoDB"
    )
    
    id_usuario: str = Field(
        description="ID del usuario al que pertenece el empleado"
    )
    
    id_tipo_empleado: str = Field(
        description="ID del tipo de empleado al que pertenece"
    )
    
    telefono: str = Field(
        description="Número de teléfono del empleado",
        pattern=r"^\d{8}$",
        examples=["56234578", "98765434"]
    )
    

    fecha_contratacion: datetime = Field(
    description="Fecha de contratación del empleado en formato ISO 8601",
    examples=["2023-10-01T12:00:00", "2023-10-02T14:30:00"]
    )
    
    active: bool = Field(
        default=True,
        description="Indica si el empleado está activo o no"
    )
    
    
    @field_validator("id_usuario", "id_tipo_empleado")
    def validar_objectid(cls, v):
        if len(v) != 24:
            raise ValueError("El ID debe tener 24 caracteres")
        return v
