'''
register_user: fa un controllo per evitare duplicati
                nasconde la password dietro un hash sicuro,
                impacchetta tutto in un oggetto User 
                e lo consegna al UserRepository 
                che si occuperà di fare la query SQL vera e propria.

authenticate_user: serve per il Login.
                    Cerca l'utente e usa la funzione verify_password
                    per capire se la password inserita dall'utente, una volta hashata, 
                    è uguale a quella che abbiamo nel database.

Questa separazione è essenziale perché permette di isolare la logica dell'applicazione 
dalla gestione del database.
'''

import bcrypt
from app.models.user import User
from app.repositories.user_repo import UserRepository


class AuthService:
    def __init__(self, db_or_repo):
        """Accetta una sessione SQLAlchemy o un repository già istanziato."""
        if isinstance(db_or_repo, UserRepository):
            self.user_repository = db_or_repo
        else:
            self.user_repository = UserRepository(db_or_repo)

    def normalize_password(self, password: str) -> bytes:
        password_bytes = password.encode("utf-8")
        if len(password_bytes) > 12:
            raise ValueError("La password non può superare i 12 caratteri")
        return password_bytes

    def get_password_hash(self, password: str) -> str:
        """Genera l'hash di una password in chiaro."""
        password_bytes = self.normalize_password(password)
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_bytes, salt).decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se la password in chiaro corrisponde all'hash salvato."""
        password_bytes = self.normalize_password(plain_password)
        return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))

    def register_user(self, email: str, password: str, username: str | None = None) -> User:
        """Logica di business per la registrazione."""

        normalized_email = email.strip().lower()

        if not username:
            raise ValueError("Scegliere un username")

        existing_mail = self.user_repository.get_user_by_email(normalized_email)
        if existing_mail:
            raise ValueError("Email già registrata")
        existing_username = self.user_repository.get_user_by_username(username)
        if existing_username:
            raise ValueError("Username già registrato")

        hashed_password = self.get_password_hash(password)
        nuovo_utente = User(username=username, email=normalized_email, password=hashed_password)
        return self.user_repository.create_user(nuovo_utente)

    def authenticate_user(self, username: str, password: str) -> User | None:
        """Logica di business per controllare le credenziali prima del login usando solo lo username."""
        normalized_username = username.strip()
        user = self.user_repository.get_user_by_username(normalized_username)
        if not user:
            return None

        if not self.verify_password(password, user.password):
            return None

        return user