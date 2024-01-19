from utils.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import Generator

config = Config()

SQLALCHEMY_DATABASE_URL = config._g.get("DATABASE", "URI")


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
# metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db() -> Generator:   #new
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()