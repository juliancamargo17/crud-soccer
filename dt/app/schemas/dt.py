from typing import Optional
from sqlmodel import SQLModel, Field

class DTBase(SQLModel):
    nombre: str = Field()
    nacionalidad: str = Field()
    edad: int = Field()
    equipo_id: Optional[int] = Field(default=None)  # FK opcional al equipo

class Config:
    extra = "forbid"
