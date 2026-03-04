from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(
    title='Mi primer API',
    description='Abraham Ordoñez Moreno',
    version='1.0.0'
)

# Base de datos simulada
usuarios = [
    {"id": 1, "nombre": "Juan", "edad": 21},
    {"id": 2, "nombre": "Israel", "edad": 21},
    {"id": 3, "nombre": "Sofi", "edad": 21},
]

# MODELOS
class UsuarioCreate(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=1)
    edad: int = Field(..., gt=0)


class UsuarioUpdate(BaseModel):
    nombre: str = Field(..., min_length=1)
    edad: int = Field(..., gt=0)


# SEGURIDAD
security = HTTPBasic()

def verificar_peticion(credenciales: HTTPBasicCredentials = Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "abraham")
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no autorizadas",
            headers={"WWW-Authenticate": "Basic"}
        )

    return credenciales.username


# RUTAS
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
async def consulta_uno(id: int):
    return {"Se encontro usuario": id}


@app.get("/v1/ParametroOp/", tags=['Parametro Opcional'])
async def consulta_todos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"mensaje": "usuario encontrado", "usuario": usuario}
        return {"mensaje": "usuario no encontrado", "usuario": id}
    else:
        return {"mensaje": "No se proporciono id"}


@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }


@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioCreate):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El id ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado",
        "usuario": usuario
    }


@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_202_ACCEPTED)
async def actualizar_usuario(id: int, usuario_actualizado: UsuarioUpdate):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario_actualizado.nombre
            usr["edad"] = usuario_actualizado.edad
            return {
                "mensaje": "Usuario actualizado correctamente",
                "usuario": usr
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="El usuario no existe"
    )


@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, userAuth: str = Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "message": f"Usuario elimido por: {userAuth}" 
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="El usuario no existe, no se pudo eliminar"
    )
