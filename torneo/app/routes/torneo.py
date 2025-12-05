from database.database import get_db
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.torneo import TorneoBase
from app.crud.utils import get_torneos, create_torneo, update_torneo, delete_torneo

router = APIRouter()

#@router.get("/ping")
#def ping():
#    return {"message": "el servicio torneos está en línea"}

@router.get("/")
def read_torneos(db: Session = Depends(get_db)):
    result = get_torneos(db)
    return result

@router.post("/")
def add_torneo(torneo: TorneoBase, db: Session = Depends(get_db)):
    result = create_torneo(db, torneo)
    return result

@router.put("/{torneo_id}")
def update_torneo_route(torneo_id: int, torneo: TorneoBase, db: Session = Depends(get_db)):
    result = update_torneo(db, torneo_id, torneo)
    return result

@router.delete("/{torneo_id}")
def delete_torneo_route(torneo_id: int, db: Session = Depends(get_db)):
    result = delete_torneo(db, torneo_id)
    return result
