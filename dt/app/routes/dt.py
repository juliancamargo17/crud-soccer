from database.database import get_db
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.schemas.dt import DTBase
from app.crud.utils import get_dts, create_dt, update_dt, delete_dt

router = APIRouter()

#@router.get("/ping")
#def ping():
#    return {"message": "el servicio DTs está en línea"}

@router.get("/")
def read_dt(db: Session = Depends(get_db)):
    result = get_dts(db)
    return result

@router.post("/")
def add_dt(dt: DTBase, db: Session = Depends(get_db)):
    result = create_dt(db, dt)
    return result

@router.put("/{dt_id}")
def update_dt_route(dt_id: int, dt: DTBase, db: Session = Depends(get_db)):
    result = update_dt(db, dt_id, dt)
    return result

@router.delete("/{dt_id}")
def delete_dt_route(dt_id: int, db: Session = Depends(get_db)):
    result = delete_dt(db, dt_id)
    return result
