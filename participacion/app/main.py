from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import participacion
from database.database import create_db_and_tables

app = FastAPI(root_path="/participacion")

# Configurar CORS para permitir requests desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

create_db_and_tables()

app.include_router(participacion.router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "participaciones"}

