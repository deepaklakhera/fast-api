from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get DB URL from env or fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/fastapi_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

