from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Login(BaseModel):
    email: str = Field(
        description="La dirección de correo electrónico del usuario",
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",  # Validación de formato de correo electrónico
    )
    
    password: str = Field(
        min_length=8,  # La contraseña debe tener al menos 8 caracteres
        max_length=64,  # La contraseña no debe exceder los 64 caracteres
        description="La contraseña del usuario",
    )
    
    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe contener al menos un dígito.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("La contraseña debe contener al menos un carácter especial.")
        return value