from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from enum import Enum


# ENUMERACION

class PosicionJugador(str, Enum):
    PORTERO = "portero"
    DEFENSA = "defensa"
    MEDIOCAMPISTA = "mediocampista"
    DELANTERO = "delantero"


# MODELOS (tablas)


class Estadio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field()
    ciudad: str = Field()
    capacidad: int = Field()

    # Relación inversa: un estadio puede tener muchos equipos (agregación).
    # Los equipos pueden existir independientemente del estadio.
    # Al borrar un estadio, los equipos se mantienen (sin cascade delete=Composición *ver UML*).
    equipos: List["Equipo"] = Relationship(back_populates="estadio")


class DT(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field()
    nacionalidad: str = Field()
    edad: int = Field()

    # FK opcional al equipo (un DT puede no estar asignado)
    equipo_id: Optional[int] = Field(default=None, foreign_key="equipo.id")
    equipo: Optional["Equipo"] = Relationship(back_populates="dt")


class Equipo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field()
    pais: str = Field()
    ciudad: str = Field()
    fundacion: int = Field()

    # FK: equipo usa un estadio (varios equipos pueden compartir un estadio)
    estadio_id: Optional[int] = Field(default=None, foreign_key="estadio.id")
    estadio: Optional["Estadio"] = Relationship(back_populates="equipos")

    # Relación 1:1 con DT (uselist=False para indicar que no es lista)
    dt: Optional["DT"] = Relationship(back_populates="equipo", sa_relationship_kwargs={"uselist": False})

    # Jugadores (1:N - agregación)
    jugadores: List["Jugador"] = Relationship(back_populates="equipo")

    # Participaciones (1:N hacia la entidad intermedia - composición fuerte)
    # Si se borra un Equipo, sus Participaciones también se borran (cascade delete)
    participaciones: List["Participacion"] = Relationship(
        back_populates="equipo",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Jugador(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field()
    edad: int = Field()
    posicion: PosicionJugador = Field()
    nacionalidad: str = Field()

    equipo_id: int= Field(default=None, foreign_key="equipo.id")
    equipo: Optional["Equipo"] = Relationship(back_populates="jugadores")


class Torneo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field()
    tipo: str = Field()   # "liga", "eliminatoria", ...
    region: str = Field()
    fecha_inicio: date = Field()
    fecha_fin: date = Field()

    # Participaciones (1:N - composición fuerte)
    # Si se borra un Torneo, sus Participaciones también se borran (cascade delete)
    participaciones: List["Participacion"] = Relationship(
        back_populates="torneo",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Participacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    año: int = Field()
    puntos: int = Field()
    posicion_final: str = Field()
    etapa: str = Field()

    equipo_id: int = Field(foreign_key="equipo.id")
    torneo_id: int = Field(foreign_key="torneo.id")

    equipo: Optional["Equipo"] = Relationship(back_populates="participaciones")
    torneo: Optional["Torneo"] = Relationship(back_populates="participaciones")