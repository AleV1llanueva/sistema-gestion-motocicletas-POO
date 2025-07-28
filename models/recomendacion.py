from pydantic import BaseModel, Field
from typing import Optional


class Recomendacion(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID de la recomendación, generado automáticamente por MongoDB"
    )
    
    id_ingreso_moto: str = Field(
        description="ID del ingreso de la motocicleta al que pertenece la recomendación"
    )
    
    texto: str = Field(
        description="Texto de la recomendación",
        examples=["Revisar frenos", "Cambiar aceite", "Ajustar cadena"]
    )
    
    fecha_recomendacion: str = Field(
        description="Fecha de la recomendación en formato ISO 8601",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$",
        examples=["2023-10-01T12:00:00", "2023-10-02T14:30:00"]
    )