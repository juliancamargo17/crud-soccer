from sqlmodel import Session, select
from models.models import DT
from app.schemas.dt import DTBase


def get_dts(db: Session):                                       #función para obtener todos los DTs (READ)
    try:    
        stmt = select(DT)
        dts = db.exec(stmt).all()
        return {
            "message": "DTs encontrados correctamente",
            "dts": [dt.model_dump() for dt in dts]
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al obtener los DTs",
            "error": str(e)
        }

def create_dt(db: Session, dt: DTBase):                        #función para crear un nuevo DT (CREATE)
    try:
        new_dt = DT(**dt.model_dump())
        db.add(new_dt)
        db.commit()
        db.refresh(new_dt)
        return {
            "message": "DT creado correctamente",
            "dt": new_dt.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al crear el DT",
            "error": str(e)
        }

def update_dt(db: Session, dt_id: int, dt: DTBase):            #función para actualizar un DT (UPDATE)
    try:
        stmt = select(DT).where(DT.id == dt_id)
        existing_dt = db.exec(stmt).first()
        
        if not existing_dt:
            return {
                "message": "DT no encontrado",
                "error": "No existe un DT con ese ID"
            }
        
        # Actualizar los campos del DT
        dt_data = dt.model_dump(exclude_unset=True)
        for key, value in dt_data.items():
            setattr(existing_dt, key, value)
        
        db.add(existing_dt)
        db.commit()
        db.refresh(existing_dt)
        
        return {
            "message": "DT actualizado correctamente",
            "dt": existing_dt.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al actualizar el DT",
            "error": str(e)
        }

def delete_dt(db: Session, dt_id: int):                        #función para eliminar un DT (DELETE)
    try:
        stmt = select(DT).where(DT.id == dt_id)
        existing_dt = db.exec(stmt).first()
        
        if not existing_dt:
            return {
                "message": "DT no encontrado",
                "error": "No existe un DT con ese ID"
            }
        
        db.delete(existing_dt)
        db.commit()
        
        return {
            "message": "DT eliminado correctamente",
            "dt": existing_dt.model_dump()
        }
    except Exception as e:
        db.rollback()
        return {
            "message": "Error al eliminar el DT",
            "error": str(e)
        }
