from database.database import get_db
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.participacion import ParticipacionBase
from app.crud.utils import get_participaciones, create_participacion, update_participacion, delete_participacion

router = APIRouter()

#@router.get("/ping")
#def ping():
#    return {"message": "el servicio participaciones está en línea"}

@router.get("/")
def read_participaciones(db: Session = Depends(get_db)):
    result = get_participaciones(db)
    return result

@router.post("/")
def add_participacion(participacion: ParticipacionBase, db: Session = Depends(get_db)):
    result = create_participacion(db, participacion)
    return result

@router.put("/{participacion_id}")
def update_participacion_route(participacion_id: int, participacion: ParticipacionBase, db: Session = Depends(get_db)):
    result = update_participacion(db, participacion_id, participacion)
    return result

@router.delete("/{participacion_id}")
def delete_participacion_route(participacion_id: int, db: Session = Depends(get_db)):
    result = delete_participacion(db, participacion_id)
    return result