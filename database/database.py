import os
from sqlmodel import SQLModel, create_engine, Session

DB_HOST = os.environ.get("DB_HOST","postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_PORT = os.environ.get("DB_PORT", "5432")

DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Creación del engine DB
engine = create_engine(DATABASE_URL, echo=True)

# Creación de tablas en DB
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Generador de sesiones DB
def get_db():
    with Session(engine) as session:
        yield session


