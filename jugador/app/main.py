from fastapi import FastAPI
from app.routes import jugador
from database.database import create_db_and_tables

app = FastAPI(root_path="/jugador")

create_db_and_tables()

app.include_router(jugador.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "jugadores"}
