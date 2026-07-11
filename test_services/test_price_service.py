from unittest.mock import patch, MagicMock
from app.services.price_service import PriceService
from app.models.brent import BrentValue
from app.services.alert_service import check_and_trigger_alerts

def test_get_price_history():
    # 1. Prepariamo il mock del repository
    mock_repo = MagicMock()
    
    # 2. Definiamo cosa deve restituire il mock quando chiamato
    mock_history = [BrentValue(value=80.0), BrentValue(value=85.0)]
    mock_repo.get_history.return_value = mock_history
    
    # 3. Creiamo il service iniettando il mock (Dependency Injection)
    service = PriceService(db=None)  # Passiamo None perché non useremo il database reale
    service.price_repo = mock_repo  # Sostituiamo il repository reale con il
    
    # 4. Eseguiamo la funzione
    result = service.get_price_history()
    
    # 5. Asserzioni
    # Verifichiamo che il risultato sia quello che abbiamo impostato nel mock
    assert result == mock_history
    # Verifichiamo che il service abbia effettivamente chiamato il metodo del repo
    mock_repo.get_history.assert_called_once()

# Il decoratore passa il mock di check_and_trigger_alerts come primo argomento
@patch('app.services.price_service.check_and_trigger_alerts')
def test_update_and_get_price(mock_check_alerts):
    # 1. Crea il mock per il DB (non serve passarlo come argomento al test)
    mock_db = MagicMock()
    
    # 2. Setup degli altri mock
    mock_brent_service = MagicMock()
    mock_brent_service.fetch_current_price.return_value = 90.0
    
    mock_price_repo = MagicMock()
    expected_value = BrentValue(value=90.0)
    mock_price_repo.save_price.return_value = expected_value
    
    # 3. Setup del servizio con il DB mockato
    service = PriceService(db=mock_db)
    service.brent_service = mock_brent_service
    service.price_repo = mock_price_repo

    # 4. Esecuzione
    result = service.update_and_get_price()

    # 5. Asserzioni
    assert result == expected_value
    
    # Verifica che la funzione patchata sia stata chiamata correttamente
    mock_check_alerts.assert_called_once_with(db=mock_db, current_price=90.0)