from sqlmodel import Session, select
from models.models import Participacion
from app.schemas.participacion import ParticipacionBase


def get_participaciones(db: Session):                                           #función para obtener todas las participaciones (READ)
    try:    
        stmt = select(Participacion)
        participaciones = db.exec(stmt).all()
        return {
            "message": "Participaciones encontradas correctamente",
            "participaciones": [participacion.model_dump() for participacion in participaciones]
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al obtener las participaciones",
            "error": str(e)
        }

def create_participacion(db: Session, participacion: ParticipacionBase):                    #función para crear una nueva participacion (CREATE)
    try:
        new_participacion = Participacion(**participacion.model_dump())
        db.add(new_participacion)
        db.commit()
        db.refresh(new_participacion)
        return {
            "message": "Participación creada correctamente",
            "participacion": new_participacion.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al crear la participación",
            "error": str(e)
        }

def update_participacion(db: Session, participacion_id: int, participacion: ParticipacionBase):     #función para actualizar una participacion (UPDATE)
    try:
        stmt = select(Participacion).where(Participacion.id == participacion_id)
        existing_participacion = db.exec(stmt).first()
        
        if not existing_participacion:
            return {
                "message": "Participación no encontrada",
                "error": "No existe una participación con ese ID"
            }
        
        # Actualizar los campos de la participacion
        participacion_data = participacion.model_dump(exclude_unset=True)
        for key, value in participacion_data.items():
            setattr(existing_participacion, key, value)
        
        db.add(existing_participacion)
        db.commit()
        db.refresh(existing_participacion)
        
        return {
            "message": "Participación actualizada correctamente",
            "participacion": existing_participacion.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al actualizar la participación",
            "error": str(e)
        }

def delete_participacion(db: Session, participacion_id: int):                         #función para eliminar una participacion (DELETE)
    try:
        stmt = select(Participacion).where(Participacion.id == participacion_id)
        existing_participacion = db.exec(stmt).first()
        
        if not existing_participacion:
            return {
                "message": "Participación no encontrada",
                "error": "No existe una participación con ese ID"
            }
        
        db.delete(existing_participacion)
        db.commit()
        
        return {
            "message": "Participación eliminada correctamente",
            "participacion": existing_participacion.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al eliminar la participación",
            "error": str(e)
        }