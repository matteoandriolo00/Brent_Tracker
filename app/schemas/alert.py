'''
Queste classi dicono a FastAPI come devono essere fatti i JSON in entrata e in uscita.
'''

from pydantic import BaseModel

# Schema per la creazione
class AlertCreate(BaseModel):
    user_id: int
    target_price: float
    direction: str  # "ABOVE" o "BELOW"

# Schema per l'attivazione/disattivazione
class AlertUpdateStatus(BaseModel):
    status: str  # "ACTIVE" o "INACTIVE"

# Schema per la risposta (cosa vede l'utente)
class AlertResponse(BaseModel):
    id: int
    user_id: int
    target_price: float
    direction: str
    status: str

    class ConfigDict:
        from_attributes = True  # Necessario per convertire il modello SQLAlchemy in JSON