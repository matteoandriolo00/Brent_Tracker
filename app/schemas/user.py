import re

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    """Schema utilizzato per validare i dati in ingresso durante la registrazione."""
    email: EmailStr
    password: str
    username: str | None = None
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        if not 6 <= len(password) <= 12:
            raise ValueError(
                "La password deve essere compresa tra 6 e 12 caratteri"
            )

        if not re.fullmatch(r"[A-Za-z0-9]+", password):
            raise ValueError(
                "La password può contenere solo lettere e numeri"
            )
    
        return password
    


class UserLogin(BaseModel):
    """Schema utilizzato per validare i dati in ingresso durante il login."""
    username: str
    password: str


class Token(BaseModel):
    """Schema per definire la struttura della risposta dopo un login con successo."""
    access_token: str
    token_type: str