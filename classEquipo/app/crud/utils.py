from sqlmodel import Session, select
from models.models import Equipo
from app.schemas.equipo import EquipoBase 


def get_equipos(db: Session):                                           #función para obtener todos los equipos (READ)
    try:    
        stmt = select(Equipo)
        equipos = db.exec(stmt).all()
        return {
            "message": "Equipos encontrados correctamente",
            "equipos": [equipo.model_dump() for equipo in equipos]
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al obtener los equipos",
            "error": str(e)
        }

def create_equipos(db: Session, equipo: EquipoBase):                    #función para crear un nuevo equipo (CREATE)
    try:
        new_team = Equipo(**equipo.model_dump())
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        return {
            "message": "Equipo creado correctamente",
            "equipo": new_team.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al crear el equipo",
            "error": str(e)
        }

def update_equipo(db: Session, equipo_id: int, equipo: EquipoBase):     #función para actualizar un equipo (UPDATE)
    try:
        stmt = select(Equipo).where(Equipo.id == equipo_id)
        existing_equipo = db.exec(stmt).first()
        
        if not existing_equipo:
            return {
                "message": "Equipo no encontrado",
                "error": "No existe un equipo con ese ID"
            }
        
        # Actualizar los campos del equipo
        equipo_data = equipo.model_dump(exclude_unset=True)
        for key, value in equipo_data.items():
            setattr(existing_equipo, key, value)
        
        db.add(existing_equipo)
        db.commit()
        db.refresh(existing_equipo)
        
        return {
            "message": "Equipo actualizado correctamente",
            "equipo": existing_equipo.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al actualizar el equipo",
            "error": str(e)
        }

def delete_equipo(db: Session, equipo_id: int):                          #función para eliminar un equipo (DELETE)
    try:
        stmt = select(Equipo).where(Equipo.id == equipo_id)
        existing_equipo = db.exec(stmt).first()
        
        if not existing_equipo:
            return {
                "message": "Equipo no encontrado",
                "error": "No existe un equipo con ese ID"
            }
        
        db.delete(existing_equipo)
        db.commit()
        
        return {
            "message": "Equipo eliminado correctamente",
            "equipo": existing_equipo.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al eliminar el equipo",
            "error": str(e)
        }
    