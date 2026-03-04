import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
#env lesen
load_dotenv()
#holt DATABASE_URL aus env
DATABASE_URL = os.environ["DATABASE_URL"]
#Verbindung zur DB
engine = create_engine(DATABASE_URL)
#SessionLocal ist ein Arbeitskorb für DB-Sessions, kein autocommit, kein autoflush, bindet an engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

#FastAPI dependency, um DB-Session zu bekommen, wird in API-Endpunkten verwendet
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
