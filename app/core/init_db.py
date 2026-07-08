from app.core.database import engine, Base
from app.models.user import User
from app.models.brent import BrentValue


Base.metadata.create_all(bind=engine)