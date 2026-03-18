from pydantic import BaseModel, Field

class UsuarioCreate(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=1)
    edad: int = Field(..., gt=0)