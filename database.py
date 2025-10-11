
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#DATABASE_URL = "sqlite:///./locatel.db"
#DATABASE_URL = "C:\Users\OMEN HP LAPTOP\Documents\Locatel\backend\locatel.db"
DATABASE_URL = r"sqlite:///C:\Users\OMEN HP LAPTOP\Documents\Locatel\backend\locatel.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
