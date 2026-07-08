'''
Crea l'engine (il motore che si connette a app.db)  e prepara get_db.
Questa funzione genera una nuova "Session" per ogni richiesta API
e si assicura di chiuderla alla fine.
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()