from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        """
        Il repository riceve la sessione del database al momento della creazione.
        Così non deve preoccuparsi di aprire o chiudere le connessioni.
        """
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        """Cerca un utente tramite la sua email in modo case-insensitive."""
        normalized_email = email.strip().lower()
        return self.db.query(User).filter(func.lower(User.email) == normalized_email).first()

    def get_user_by_username(self, username: str) -> User | None:
        """Cerca un utente tramite il suo username."""
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: User) -> User:
        """Salva un nuovo utente nel database."""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user) # Ricarica l'oggetto per ottenere l'ID generato da SQLite
        return user