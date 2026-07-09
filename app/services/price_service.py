from sqlalchemy.orm import Session
from app.repositories.price_repo import PriceRepository
from app.services.brent_service import BrentService
from app.models.brent import BrentValue

class PriceService:
    """
    Contiene la logica di business principale. Coordina il recupero del prezzo 
    dall'esterno e il salvataggio automatico nel database.
    """
    
    def __init__(self, db: Session):
        """
        Inizializza il servizio creando le istanze del Repository e del BrentService.
        """
        self.price_repo = PriceRepository(db)
        self.brent_service = BrentService()

    def update_and_get_price(self) -> BrentValue:
        """
        Esegue la catena di operazioni:
        1. Interroga l'API esterna per il prezzo attuale.
        2. Salva immediatamente il dato nello storico.
        3. Restituisce il record salvato.
        """
        current_price = self.brent_service.fetch_current_price()
        saved_record = self.price_repo.save_price(price=current_price)
        return saved_record
        
    def get_price_history(self) -> list[BrentValue]:
        """
        Richiede al repository di restituire tutto lo storico salvato.
        """
        return self.price_repo.get_history()