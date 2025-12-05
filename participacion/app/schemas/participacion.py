from typing import Optional
from sqlmodel import SQLModel, Field

class ParticipacionBase(SQLModel):
    año: int = Field()
    puntos: int = Field()
    posicion_final: str = Field()
    etapa: str = Field()
    equipo_id: int = Field()  # FK requerido al equipo
    torneo_id: int = Field()  # FK requerido al torneo

class Config:
    extra = "forbid"