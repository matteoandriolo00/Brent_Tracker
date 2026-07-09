from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin, Token

# Creiamo il router raggruppando gli endpoint sotto il tag "Autenticazione"
router = APIRouter(prefix="/auth", tags=["Autenticazione"])

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Endpoint per registrare un nuovo utente."""
    try:
        auth_service = AuthService(db)
        nuovo_utente = auth_service.register_user(
            email=user_data.email,
            password=user_data.password,
            username=user_data.username,
        )

        return {
            "status": "success",
            "message": "Utente registrato con successo",
            "user_id": nuovo_utente.id,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Errore interno del server durante la registrazione.")

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint per effettuare il login.
    Verifica l'esistenza dell'utente e la correttezza della password tramite
    l'AuthService. Se i dati sono corretti, restituisce un token di accesso.
    """
    auth_service = AuthService(db)
    
    # Questo metodo dovrebbe restituire l'utente se la password è corretta, altrimenti lancia un'eccezione o restituisce None
    user = auth_service.authenticate_user(email=user_data.email, password=user_data.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Email o password non corretti")
    
    # In una vera app qui genereresti un token JWT usando una libreria apposita (es. python-jose).
    # Per ora simuliamo un token base per soddisfare RF2 senza complicare troppo il codice.
    fake_token = f"token_fittizio_per_{user.id}"
    
    return {"access_token": fake_token, "token_type": "bearer"}