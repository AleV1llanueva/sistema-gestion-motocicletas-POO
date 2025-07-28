from typing import Optional
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId
import re

class Mantenimiento(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID del mantenimiento, generado automáticamente por MongoDB"
    )
    
    id_ingreso: str = Field(
        description="ID del ingreso asociado al mantenimiento",
        examples=["60c72b2f9b1e8d3f4c8b4567", "60c72b2f9b1e8d3f4c8b4568"]
    )

    id_empleado: Optional[str] = Field(
        default=None,
        description="ID del empleado que realiza el mantenimiento",
        examples=["60c72b2f9b1e8d3f4c8b4569", "60c72b2f9b1e8d3f4c8b4570"]
    )

    id_tipo_mantenimiento: str = Field(
        default=None,
        description="ID del tipo de mantenimiento realizado",
        examples=["60c72b2f9b1e8d3f4c8b4571", "60c72b2f9b1e8d3f4c8b4572"]
    )
    
    description: str = Field(
        description="Descripción del mantenimiento",
        pattern=r"^[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Cambio de aceite", "Revisión de frenos", "Ajuste de cadena"]
    )
    
    costo: float = Field(
        description="Costo del mantenimiento",
        ge=0, # ge significa "greater than or equal to" (mayor o igual que)
        examples=[50.0, 75.5, 100.0]
    )
    