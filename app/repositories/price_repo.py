from sqlalchemy.orm import Session
from app.models.brent import BrentValue

class PriceRepository:
    """
    Gestisce le operazioni di lettura e scrittura sul database per lo storico dei prezzi del Brent.
    Isola la logica di persistenza dal resto dell'applicazione.
    """
    
    def __init__(self, db: Session):
        """
        Inizializza il repository assegnandogli la sessione del database corrente.
        """
        self.db = db

    def save_price(self, price: float) -> BrentValue:
        """
        Crea un nuovo snapshot del prezzo e lo salva fisicamente nello storico (database SQLite).
        Restituisce l'oggetto BrentValue appena salvato (che includerà il timestamp generato).
        """
        nuovo_valore = BrentValue(value=price)
        self.db.add(nuovo_valore)
        self.db.commit()
        self.db.refresh(nuovo_valore)
        return nuovo_valore

    def get_history(self) -> list[BrentValue]:
        """
        Recupera l'intero storico dei prezzi dal database, ordinato dal più recente al più vecchio.
        """
        return self.db.query(BrentValue).order_by(BrentValue.timestamp.desc()).all()