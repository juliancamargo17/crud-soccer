from typing import Optional
from sqlmodel import SQLModel

class EstadioBase(SQLModel):
    nombre: str
    ciudad: str
    capacidad: int
