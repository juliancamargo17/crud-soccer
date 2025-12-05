from fastapi import FastAPI
from app.routes import estadio
from database.database import create_db_and_tables

app = FastAPI(root_path="/estadio")

create_db_and_tables()

app.include_router(estadio.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "estadios"}
