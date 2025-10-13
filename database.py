from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ✅ Usa una ruta compatible con SQLAlchemy (slashes /, no backslashes \)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'locatel.db')}"

# Crea el motor
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,
    },
    pool_pre_ping=True,
    pool_size=3,
    max_overflow=5
)

# Sesión y Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para FastAPI o scripts
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
