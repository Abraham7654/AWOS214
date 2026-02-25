from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime

app = FastAPI(
    title="API Biblioteca Digital",
    description="Control de libros y préstamos",
    version="1.0.0"
)

libros = []
prestamos = []

anio_actual = datetime.now().year


class Libro(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    autor: str
    año: int = Field(gt=1450, le=año_actual)
    paginas: int = Field(gt=1)
    estado: str = Field(pattern="^(disponible|prestado)$")


class Usuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr


class Prestamo(BaseModel):
    libro: str
    usuario: Usuario


@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):

    for l in libros:
        if l["nombre"].lower() == libro.nombre.lower():
            raise HTTPException(status_code=400, detail="El libro ya existe")

    libros.append(libro.dict())
    return {"mensaje": "Libro registrado correctamente"}


@app.get("/libros")
def listar_libros():
    return libros


@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):

    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():
            return libro

    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):

    for libro in libros:
        if libro["nombre"].lower() == prestamo.libro.lower():

            if libro["estado"] == "prestado":
                raise HTTPException(status_code=409, detail="Libro ya prestado")

            libro["estado"] = "prestado"
            prestamos.append(prestamo.dict())
            return {"mensaje": "Préstamo registrado correctamente"}

    raise HTTPException(status_code=404, detail="Libro no existe")


@app.put("/prestamos/{nombre}")
def devolver_libro(nombre: str):

    for libro in libros:
        if libro["nombre"].lower() == nombre.lower():

            if libro["estado"] == "disponible":
                raise HTTPException(status_code=409, detail="El préstamo no existe")

            libro["estado"] = "disponible"
            return {"mensaje": "Libro devuelto correctamente"}

    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.delete("/prestamos/{nombre}")
def eliminar_prestamo(nombre: str):

    for prestamo in prestamos:
        if prestamo["libro"].lower() == nombre.lower():
            prestamos.remove(prestamo)
            return {"mensaje": "Préstamo eliminado"}

    raise HTTPException(status_code=409, detail="El registro de préstamo ya no existe")