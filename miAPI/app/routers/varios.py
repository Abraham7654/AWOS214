from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

router= APIRouter(tags=[''])

@router.get("/")
async def bienvenida():
    return {"mensaje": "¡Bienvenido a mi API!"}


@router.get("/HolaMundo")
async def hola():
    await asyncio.sleep(3)
    return {
        "mensaje": "¡Hola Mundo FastAPI!",
        "estatus": "200"
    }


@router.get("/v1/parametroOb/{id}")
async def consulta_uno(id: int):
    return {"Se encontro usuario": id}


@router.get("/v1/ParametroOp/")
async def consulta_todos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuario}
        return {"mensaje": "usuario no encontrado", "usuario": id}
    else:
        return {"mensaje": "No se proporciono id"}

