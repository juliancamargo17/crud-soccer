from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

class TorneoBase(SQLModel):
    nombre: str = Field()
    tipo: str = Field()  # "liga", "eliminatoria", etc.
    region: str = Field()
    fecha_inicio: date = Field()
    fecha_fin: date = Field()

class Config:
    extra = "forbid"
