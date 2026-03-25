from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1.definimos la URL de la BD
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql:postgresql://admin:123456@postgres:5432/DB_miapi"
)

#2.Creamos el motor de conexion
engine= create_engine(DATABASE_URL)

#3.Creamos gestionador de sesiones
sessionLocal= sessionmaker(
    autocommit=False,
    autoflush= False,
    bind= engine
)

#4. Base declarativa
Base= declative_base()

#5.Funcion para la sesion en cada peticion
def get_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()
