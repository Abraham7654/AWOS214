from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import List
from datetime import datetime

app = FastAPI(
    title="API Sistema de Tickets de Soporte Técnico",
    description="Gestionar tickets",
    version="1.0.0"
)


class Tickets(BaseModel):
    id: int
    descripcion: str = Field(min_length=20, max_length=200)
    nombre str = Field(min_length=5)



@app.post("/v1/tickets/", tags=['CRUD HTTP'])
async def crear_tickets(tickets: dict):
    for usr in tickets:
        if usr["id"] == ticket.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )

    usuarios.append(ticket)

    return {
        "mensaje": "Ticket Agregado",
        "Ticket": ticket
    }


@app.get("/tickets")
def listar_ticket():
    return Tickets


@app.get("/tickets/{nombre}")
def consultar_ticket(nombre: str):

    for ticket in ticket:
        if ticket["id"].lower() == id.lower():
            return ticket

    raise HTTPException(status_code=404, detail="Ticket no encontrado")

@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_202_ACCEPTED)
async def actualizar_ticket(id: int, ticket_actualizado: TicketUpdate, user: str = Depends(validar_token)):
    for usr in tickets:
        if usr["id"] == id:
            usr["nombre"] = ticket_actualizado.nombre
            return {
                "mensaje": f"Ticket actualizado por {user}",
                "usuario": usr
            }

