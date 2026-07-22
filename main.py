from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.api import prices, auth, alert

# assicura che le tabelle SQLite vengano create all'avvio 
Base.metadata.create_all(bind=engine)

# Inizializza l'applicazione FastAPI
app = FastAPI(
    title="Brent Tracker API",
    description="API per il monitoraggio del prezzo del petrolio Brent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra i router creati
app.include_router(prices.router)
app.include_router(auth.router)
app.include_router(alert.router)

# 1. Servi i file statici di React usando il nome corretto della cartella
app.mount("/assets", StaticFiles(directory="brent-tracker-frontend/dist/assets"), name="assets")

# 2. Quando l'utente va sulla root "/", restituisci l'index.html di React
@app.get("/")
async def serve_react_app():
    return FileResponse("brent-tracker-frontend/dist/index.html")

# 3. Catch-all per React Router (gestisce la navigazione interna delle pagine)
@app.get("/{catchall:path}")
async def serve_react_router(catchall: str):
    return FileResponse("brent-tracker-frontend/dist/index.html")