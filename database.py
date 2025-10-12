from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = r"sqlite:///C:\Users\OMEN HP LAPTOP\Documents\Locatel\BackVentas\locatel.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,  # espera hasta 30s si está bloqueada
    },
    pool_pre_ping=True,
    pool_size=3,          # tamaño del pool pequeño
    max_overflow=5        # conexiones extra si hay carga
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
