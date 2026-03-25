from pydantic import BaseModel, Field

class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=3,max_length=50,example="Juan")
    edad: int = Field(..., ge=1,le=0,)
