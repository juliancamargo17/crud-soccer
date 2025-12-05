from sqlmodel import Session, select
from models.models import Torneo
from app.schemas.torneo import TorneoBase


def get_torneos(db: Session):                                           #función para obtener todos los torneos (READ)
    try:    
        stmt = select(Torneo)
        torneos = db.exec(stmt).all()
        return {
            "message": "Torneos encontrados correctamente",
            "torneos": [torneo.model_dump() for torneo in torneos]
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al obtener los torneos",
            "error": str(e)
        }

def create_torneo(db: Session, torneo: TorneoBase):                    #función para crear un nuevo torneo (CREATE)
    try:
        new_torneo = Torneo(**torneo.model_dump())
        db.add(new_torneo)
        db.commit()
        db.refresh(new_torneo)
        return {
            "message": "Torneo creado correctamente",
            "torneo": new_torneo.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al crear el torneo",
            "error": str(e)
        }

def update_torneo(db: Session, torneo_id: int, torneo: TorneoBase):     #función para actualizar un torneo (UPDATE)
    try:
        stmt = select(Torneo).where(Torneo.id == torneo_id)
        existing_torneo = db.exec(stmt).first()
        
        if not existing_torneo:
            return {
                "message": "Torneo no encontrado",
                "error": "No existe un torneo con ese ID"
            }
        
        # Actualizar los campos del torneo
        torneo_data = torneo.model_dump(exclude_unset=True)
        for key, value in torneo_data.items():
            setattr(existing_torneo, key, value)
        
        db.add(existing_torneo)
        db.commit()
        db.refresh(existing_torneo)
        
        return {
            "message": "Torneo actualizado correctamente",
            "torneo": existing_torneo.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al actualizar el torneo",
            "error": str(e)
        }

def delete_torneo(db: Session, torneo_id: int):                          #función para eliminar un torneo (DELETE)
    try:
        stmt = select(Torneo).where(Torneo.id == torneo_id)
        existing_torneo = db.exec(stmt).first()
        
        if not existing_torneo:
            return {
                "message": "Torneo no encontrado",
                "error": "No existe un torneo con ese ID"
            }
        
        db.delete(existing_torneo)
        db.commit()
        
        return {
            "message": "Torneo eliminado correctamente",
            "torneo": existing_torneo.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al eliminar el torneo",
            "error": str(e)
        }
