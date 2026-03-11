from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI(
    title='Mi primer API',
    description='Abraham Ordoñez Moreno',
    version='1.0.0'
)



SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


fake_user = {
    "username": "abraham",
    "password": pwd_context.hash("123456")
}



def crear_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")



@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or \
       not pwd_context.verify(form_data.password, fake_user["password"]):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = crear_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


usuarios = [
    {"id": 1, "nombre": "Juan", "edad": 21},
    {"id": 2, "nombre": "Israel", "edad": 21},
    {"id": 3, "nombre": "Sofi", "edad": 21},
]

class UsuarioCreate(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=1)
    edad: int = Field(..., gt=0)

class UsuarioUpdate(BaseModel):
    nombre: str = Field(..., min_length=1)
    edad: int = Field(..., gt=0)



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

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }



@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioCreate, user: str = Depends(validar_token)):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El id ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": f"Usuario agregado por {user}",
        "usuario": usuario
    }

@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_202_ACCEPTED)
async def actualizar_usuario(id: int, usuario_actualizado: UsuarioUpdate, user: str = Depends(validar_token)):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario_actualizado.nombre
            usr["edad"] = usuario_actualizado.edad
            return {
                "mensaje": f"Usuario actualizado por {user}",
                "usuario": usr
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="El usuario no existe"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, user: str = Depends(validar_token)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "message": f"Usuario eliminado por {user}"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="El usuario no existe, no se pudo eliminar"
    )    
