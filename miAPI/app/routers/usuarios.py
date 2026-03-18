from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import verificar_peticion


router = APIRouter(
    |prefix="/v1/usuarios", tags=['CRUD HTTP']
)

@router.get("/")
async def leer_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
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


@router.delete("/{id}", status_code=status.HTTP_200_OK)
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
