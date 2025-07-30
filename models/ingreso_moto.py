from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
import re

class IngresoMoto(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID del ingreso de la motocicleta, generado automáticamente por MongoDB"
    )

    id_modelo: Optional[str] = Field(
        default=None,
        description="ID del modelo de la motocicleta ingresada",
        examples=["60c72b2f9b1e8d3f4c8b4567", "60c72b2f9b1e8d3f4c8b4568"]
    )

    id_cliente: Optional[str] = Field(
        default=None,
        description="ID del cliente propietario de la motocicleta",
        examples=["60c72b2f9b1e8d3f4c8b4569", "60c72b2f9b1e8d3f4c8b4570"]
    )

    id_empleado: Optional[str] = Field(
        default=None,
        description="ID del empleado que registra el ingreso",
        examples=["60c72b2f9b1e8d3f4c8b4569", "60c72b2f9b1e8d3f4c8b4570"]
    )

    estado: Optional[str] = Field(
        description="Descripción del estado",
        examples=["En espera", "En reparación", "Listo para entrega", "Entregado"]
    )
    
    fecha_ingreso: str = Field(
        description="Fecha y hora del ingreso de la motocicleta",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$",
        examples=["2023-10-01T12:00:00", "2023-10-02T14:30:00"]
    )
    color: str = Field(
        description="Color de la motocicleta",
        examples=["rojo", "azul", "negro"]
    )
    
    placa: str = Field(
        description="Placa de la motocicleta",
        pattern=r"^[A-Z0-9]{1,10}$",
        examples=["ABC123", "XYZ789", "MOTO456"]
    )
    
    descripcion_ingreso: str = Field(
        description="Descripción del ingreso de la motocicleta",
        pattern=r"^[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Rallon en la parte delantera", "Cambio de aceite", "Revisión general"]
    )
    
    vin: str = Field(
        description="Número de identificación del vehículo (VIN)",
        pattern=r"^[A-HJ-NPR-Z0-9]{17}$",
        examples=["1HGCM82633A123456", "1FTRX18W51NA12345"]
    )
    
    es_dueno: bool = Field(
        default=True,
        description="Indica si el cliente es el dueño de la motocicleta"
    )
    
    