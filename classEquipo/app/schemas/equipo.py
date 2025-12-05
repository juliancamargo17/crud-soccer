#crear un esquema para equipo.py
from typing import Optional
from sqlmodel import SQLModel, Field

class EquipoBase(SQLModel):
    nombre: str = Field()
    pais: str = Field()
    ciudad: str = Field()
    fundacion: int = Field()
    estadio_id: Optional[int] = Field(default=None)  # FK opcional al estadio
    #estadio_id: int = None  # FK opcional al estadio

class Config:
    extra = "forbid"