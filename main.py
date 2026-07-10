from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import prices, auth, alert

# Opzionale ma consigliato: Assicura che le tabelle SQLite vengano create all'avvio 
# se non lo hai già fatto con lo script init_db.py
Base.metadata.create_all(bind=engine)

# Inizializza l'applicazione FastAPI
app = FastAPI(
    title="Brent Tracker API",
    description="API per il monitoraggio del prezzo del petrolio Brent",
    version="1.0.0"
)

# Registriamo il router dei prezzi che hai creato in app/api/prices.py
app.include_router(prices.router)
app.include_router(auth.router)
app.include_router(alert.router)

@app.get("/")
def read_root():
    """
    Endpoint di base per verificare che il server sia acceso e funzionante.
    """
    return {"message": "Benvenuto nell'API di Brent Tracker!"}