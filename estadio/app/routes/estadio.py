from database.database import get_db
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.estadio import EstadioBase
from app.crud.utils import get_estadios, create_estadio, update_estadio, delete_estadio

router = APIRouter()

#@router.get("/ping")
#def ping():
#    return {"message": "el servicio estadios está en línea"}

@router.get("/")
def read_estadios(db: Session = Depends(get_db)):
    result = get_estadios(db)
    return result

@router.post("/")
def add_estadio(estadio: EstadioBase, db: Session = Depends(get_db)):
    result = create_estadio(db, estadio)
    return result

@router.put("/{estadio_id}")
def update_estadio_route(estadio_id: int, estadio: EstadioBase, db: Session = Depends(get_db)):
    result = update_estadio(db, estadio_id, estadio)
    return result

@router.delete("/{estadio_id}")
def delete_estadio_route(estadio_id: int, db: Session = Depends(get_db)):
    result = delete_estadio(db, estadio_id)
    return result

