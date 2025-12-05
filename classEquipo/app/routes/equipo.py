from database.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.schemas.equipo import EquipoBase
from app.crud.utils import get_equipos, create_equipos, update_equipo, delete_equipo

router=APIRouter()

@router.get("/")
def read_equipos(db: Session = Depends(get_db)):
    result = get_equipos(db)
    return result

@router.post("/")
def add_equipo(equipo: EquipoBase, db: Session = Depends(get_db)):
    result = create_equipos(db, equipo)
    return result

@router.put("/{equipo_id}")
def update_equipo_route(equipo_id: int, equipo: EquipoBase, db: Session = Depends(get_db)):
    result = update_equipo(db, equipo_id, equipo)
    return result

@router.delete("/{equipo_id}")
def delete_equipo_route(equipo_id: int, db: Session = Depends(get_db)):
    result = delete_equipo(db, equipo_id)
    return result

#@router.get("/ping")
#def ping():
#   return {"message": "el servicio equipos está en línea"}