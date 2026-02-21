from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel,Field

app = FastAPI(
    title='Mi primer API',
    description='Abraham Ordoñez Moreno',
    version='1.0.0'
)

usuarios = [
    {"id": 1, "nombre": "Juan", "edad": 21},
    {"id": 2, "nombre": "Israel", "edad": 21},
    {"id": 3, "nombre": "Sofi", "edad": 21},
]

class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str= Field(...,min_length=3,max_length=50,example="Juanita")
    edad: int= Field(..., ge=1,le=123, description="Edad valida entre 1 y 123")


@app.get("/", tags=['Inicio'])
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API!"}

@app.get("/HolaMundo", tags=['Bienvenida Asincrona'])
async def hola():
    await asyncio.sleep(3)
    return {
        "mensaje": "¡Hola Mundo FastAPI!",
        "estatus": "200"
    }

@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id: int):
    return {"Se encontro usuario": id}

@app.get("/v1/ParametroOp/", tags=['Parametro Opcional'])
async def consultaTodos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuario}
        return {"mensaje": "usuario no encontrado", "usuario": id}
    else:
        return {"mensaje": "No se proporciono id"}

@app.get("/v1/Usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:usuario_create):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return {
        "mensaje": "Usuario Agregado",
        "Usuario": usuario
    }

@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_202_ACCEPTED)
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario_actualizado.get("nombre")
            usr["edad"] = usuario_actualizado.get("edad")
            return {
                "mensaje": "Usuario Actualizado correctamente",
                "usuario": usr
            }
    raise HTTPException(
        status_code=404,
        detail="El usuario no existe"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return
    raise HTTPException(
        status_code=404,
        detail="El usuario no existe, no se pudo eliminar"
    )