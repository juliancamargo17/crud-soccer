from typing import Optional
from sqlmodel import SQLModel, Field
from models.models import PosicionJugador

class JugadorBase(SQLModel):
    nombre: str = Field()
    edad: int = Field()
    posicion: PosicionJugador = Field()
    nacionalidad: str = Field()
    equipo_id: Optional[int] = Field()  # FK requerido al equipo

class Config:
    extra = "forbid"
