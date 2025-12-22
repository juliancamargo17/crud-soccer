import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import dt
from database.database import create_db_and_tables
from models import models  # Importar modelos para que SQLModel los registre

root_path = "/dt" if os.getenv("RUNNING_IN_DOCKER") == "true" else ""
app = FastAPI(root_path=root_path)

# Configurar CORS para permitir requests desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

create_db_and_tables()

app.include_router(dt.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "dts"}
