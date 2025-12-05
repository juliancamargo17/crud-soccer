from fastapi import FastAPI
from app.routes import equipo 
from database.database import create_db_and_tables

app = FastAPI(root_path="/equipo")

create_db_and_tables()

app.include_router(equipo.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "equipos"}


