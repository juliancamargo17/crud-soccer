from sqlmodel import Session, select
from models.models import Estadio
from app.schemas.estadio import EstadioBase


def get_estadios(db: Session):                                             #función para obtener todos los estadios (READ)  
    try:
        stmt = select(Estadio)
        estadios = db.exec(stmt).all()
        return {
            "message": "Estadios encontrados correctamente",
            "estadios": [estadio.model_dump() for estadio in estadios],
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al obtener los estadios",
            "error": str(e),
        }


def create_estadio(db: Session, estadio: EstadioBase):                      #función para crear un nuevo estadio (CREATE)
    try:
        new_estadio = Estadio(**estadio.model_dump())
        db.add(new_estadio)
        db.commit()
        db.refresh(new_estadio)
        return {
            "message": "Estadio creado correctamente",
            "estadio": new_estadio.model_dump(),
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al crear el estadio",
            "error": str(e),
        }

def update_estadio(db: Session, estadio_id: int, estadio: EstadioBase):     #función para actualizar un estadio (UPDATE)
    try:
        stmt = select(Estadio).where(Estadio.id == estadio_id)
        existing_estadio = db.exec(stmt).first()
        
        if not existing_estadio:
            return {
                "message": "Estadio no encontrado",
                "error": "No existe un estadio con ese ID"
            }
        
        # Actualizar los campos del estadio
        estadio_data = estadio.model_dump(exclude_unset=True)
        for key, value in estadio_data.items():
            setattr(existing_estadio, key, value)
        
        db.add(existing_estadio)
        db.commit()
        db.refresh(existing_estadio)
        
        return {
            "message": "Estadio actualizado correctamente",
            "estadio": existing_estadio.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al actualizar el estadio",
            "error": str(e)
        }

def delete_estadio(db: Session, estadio_id: int):                          #función para eliminar un estadio (DELETE)
    try:
        stmt = select(Estadio).where(Estadio.id == estadio_id)
        existing_estadio = db.exec(stmt).first()
        
        if not existing_estadio:
            return {
                "message": "Estadio no encontrado",
                "error": "No existe un estadio con ese ID"
            }
        
        db.delete(existing_estadio)
        db.commit()
        
        return {
            "message": "Estadio eliminado correctamente",
            "estadio": existing_estadio.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al eliminar el estadio",
            "error": str(e)
        }
