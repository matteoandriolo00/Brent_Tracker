'''
script "one-off".
Quando Base.metadata.create_all viene chiamata,
SQLAlchemy guarda tutti i modelli che hanno ereditato da Base (User e BrentValue)
e crea le tabelle fisiche in SQLite.
'''

from app.core.database import engine, Base
from app.models.user import User
from app.models.brent import BrentValue


Base.metadata.create_all(bind=engine)