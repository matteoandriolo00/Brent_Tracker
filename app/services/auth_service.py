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

from passlib.context import CryptContext
from app.models.user import User
from app.repositories.user_repo import UserRepository

# Configurazione di passlib per l'hashing delle password con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repository: UserRepository):
        """
        L'AuthService ha bisogno del UserRepository per salvare o cercare gli utenti.
        Glielo passiamo al momento della creazione (Dependency Injection).
        """
        self.user_repository = user_repository

    def get_password_hash(self, password: str) -> str:
        """Genera l'hash di una password in chiaro."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica se la password in chiaro corrisponde all'hash salvato."""
        return pwd_context.verify(plain_password, hashed_password)

    def register_user(self, username: str, email: str, password: str) -> User:
        """Logica di business per la registrazione (RF1)."""
        # 1. Controlla se l'email esiste già
        existing_user = self.user_repository.get_user_by_email(email)
        if existing_user:
            raise ValueError("Email già registrata")
        
        # 2. Crea l'hash della password
        hashed_password = self.get_password_hash(password)
        
        # 3. Prepara l'oggetto User
        nuovo_utente = User(
            username=username,
            email=email,
            password=hashed_password
        )
        
        # 4. Salva e ritorna l'utente tramite il repository
        return self.user_repository.create_user(nuovo_utente)

    def authenticate_user(self, email: str, password: str) -> User | None:
        """Logica di business per controllare le credenziali prima del login (RF2)."""
        # 1. Cerca l'utente tramite email
        user = self.user_repository.get_user_by_email(email)
        if not user:
            return None # Utente non trovato
        
        # 2. Verifica che la password sia corretta
        if not self.verify_password(password, user.password):
            return None # Password errata
            
        return user