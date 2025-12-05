from database.database import get_db
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.jugador import JugadorBase
from app.crud.utils import get_jugadores, create_jugador, update_jugador, delete_jugador

router = APIRouter()

#@router.get("/ping")
#def ping():
#    return {"message": "el servicio jugadores está en línea"}

@router.get("/")
def read_jugadores(db: Session = Depends(get_db)):
    result = get_jugadores(db)
    return result

@router.post("/")
def add_jugador(jugador: JugadorBase, db: Session = Depends(get_db)):
    result = create_jugador(db, jugador)
    return result

@router.put("/{jugador_id}")
def update_jugador_route(jugador_id: int, jugador: JugadorBase, db: Session = Depends(get_db)):
    result = update_jugador(db, jugador_id, jugador)
    return result

@router.delete("/{jugador_id}")
def delete_jugador_route(jugador_id: int, db: Session = Depends(get_db)):
    result = delete_jugador(db, jugador_id)
    return result
