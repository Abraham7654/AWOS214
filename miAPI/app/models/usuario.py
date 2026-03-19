from typing import Optional
from pydantic import BaseModel, Field

class UsuarioCreate(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=1)
    edad: int = Field(..., gt=0)

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1)
    edad: Optional[int] = Field(None, gt=0)