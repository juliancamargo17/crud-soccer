from fastapi import FastAPI
from app.routes import participacion
from database.database import create_db_and_tables

app = FastAPI(root_path="/participacion")

create_db_and_tables()

app.include_router(participacion.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "participaciones"}

