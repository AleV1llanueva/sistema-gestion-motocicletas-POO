from pydantic import BaseModel, Field, field_validator # para hacer validaciones de tipo de datos para cada atributo
from typing import Optional
import re

class User(BaseModel):
    
    id: Optional[str] = Field(
        default=None,  # El ID es opcional y puede ser None si no se proporciona
        description="MongoDB ObjectId del usuario",
    )
    
    name: str = Field(
        description="El nombre del usuario",
        pattern=r"^[A-zA-zÁáÉéÍíÓóÚúÑñ' -]+$",  # Permite solo letras y espacios en blanco
        examples=["Juan", "María José"] # Ejemplo de un nombre de usuario
    )
    
    lastname: str = Field(
        description="El apellido del usuario",
        pattern=r"^[A-zA-zÁáÉéÍíÓóÚúÑñ' -]+$",  # Permite solo letras y espacios en blanco
        examples=["Pérez", "García López"]  # Ejemplo de un apellido de usuario
    )
    
    email: str = Field(
        description="La dirección de correo electrónico del usuario",
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", #Ayuda a validar de que lo que se ingrese sea un correo electrónico válido
        examples=["usuario@example.com"]
    )
    
    active: bool = Field(
        default=True,  # Por defecto, el usuario está activo
        description="Indica si el usuario está activo o no"
    )
    
    admin: bool = Field(
        default=False,  # Por defecto, el usuario no es administrador
        description="Indica si el usuario es administrador o no"
    )
    
    password: str = Field(
        description="La contraseña del usuario",
        min_length=8,  # La contraseña debe tener al menos 8 caracteres
        max_length=64,  # La contraseña no debe exceder los 64 caracteres
        example="Mipassword123!"  # Ejemplo de una contraseña válida
        
    )
        
    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, value: str):
        if not re.search(r"[A-Z]", value):
                raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"\d", value):
                raise ValueError("La contraseña debe contener al menos un número.")
        if not re.search(r"[!@$!%*?&]", value):
                raise ValueError("La contraseña debe contener al menos un carácter especial.")

        return value
