from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema utilizzato per validare i dati in ingresso durante la registrazione."""
    email: EmailStr
    password: str
    username: str | None = None


class UserLogin(BaseModel):
    """Schema utilizzato per validare i dati in ingresso durante il login."""
    email: str
    password: str


class Token(BaseModel):
    """Schema per definire la struttura della risposta dopo un login con successo."""
    access_token: str
    token_type: str