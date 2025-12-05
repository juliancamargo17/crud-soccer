from fastapi import FastAPI
from app.routes import dt
from database.database import create_db_and_tables

app = FastAPI(root_path="/dt")

create_db_and_tables()

app.include_router(dt.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "dts"}
