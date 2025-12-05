from fastapi import FastAPI
from app.routes import torneo
from database.database import create_db_and_tables

app = FastAPI(root_path="/torneo")

create_db_and_tables()

app.include_router(torneo.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "torneos"}
