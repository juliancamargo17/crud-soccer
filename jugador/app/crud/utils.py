from sqlmodel import Session, select
from models.models import Jugador
from app.schemas.jugador import JugadorBase


def get_jugadores(db: Session):                                           #función para obtener todos los jugadores (READ)
    try:    
        stmt = select(Jugador)
        jugadores = db.exec(stmt).all()
        return {
            "message": "Jugadores encontrados correctamente",
            "jugadores": [jugador.model_dump() for jugador in jugadores]
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al obtener los jugadores",
            "error": str(e)
        }

def create_jugador(db: Session, jugador: JugadorBase):                    #función para crear un nuevo jugador (CREATE)
    try:
        new_jugador = Jugador(**jugador.model_dump())
        db.add(new_jugador)
        db.commit()
        db.refresh(new_jugador)
        return {
            "message": "Jugador creado correctamente",
            "jugador": new_jugador.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al crear el jugador",
            "error": str(e)
        }

def update_jugador(db: Session, jugador_id: int, jugador: JugadorBase):     #función para actualizar un jugador (UPDATE)
    try:
        stmt = select(Jugador).where(Jugador.id == jugador_id)
        existing_jugador = db.exec(stmt).first()
        
        if not existing_jugador:
            return {
                "message": "Jugador no encontrado",
                "error": "No existe un jugador con ese ID"
            }
        
        # Actualizar los campos del jugador
        jugador_data = jugador.model_dump(exclude_unset=True)
        for key, value in jugador_data.items():
            setattr(existing_jugador, key, value)
        
        db.add(existing_jugador)
        db.commit()
        db.refresh(existing_jugador)
        
        return {
            "message": "Jugador actualizado correctamente",
            "jugador": existing_jugador.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al actualizar el jugador",
            "error": str(e)
        }

def delete_jugador(db: Session, jugador_id: int):                          #función para eliminar un jugador (DELETE)
    try:
        stmt = select(Jugador).where(Jugador.id == jugador_id)
        existing_jugador = db.exec(stmt).first()
        
        if not existing_jugador:
            return {
                "message": "Jugador no encontrado",
                "error": "No existe un jugador con ese ID"
            }
        
        db.delete(existing_jugador)
        db.commit()
        
        return {
            "message": "Jugador eliminado correctamente",
            "jugador": existing_jugador.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al eliminar el jugador",
            "error": str(e)
        }
