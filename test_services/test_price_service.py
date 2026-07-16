from unittest.mock import patch, MagicMock
from app.services.price_service import PriceService
from app.models.brent import BrentValue
from app.services.alert_service import check_and_trigger_alerts
from hypothesis import given, strategies as st
from datetime import datetime

@given(
    history=st.lists(
        st.builds(
            BrentValue,
            value=st.floats(
                min_value=0.01,
                max_value=1000.0,
                allow_nan=False,
                allow_infinity=False,
            ),
            timestamp=st.datetimes(
                min_value=datetime(2020, 1, 1),
                max_value=datetime(2030, 1, 1),
            ),
        ),
        max_size=100,
    )
)
def test_get_price_history(history):
    mock_repo = MagicMock()
    mock_repo.get_history.return_value = history

    service = PriceService(db=None)
    service.price_repo = mock_repo

    result = service.get_price_history()

    assert result == sorted(
        history,
        key=lambda x: x.timestamp,
    )

    mock_repo.get_history.assert_called_once()

# Il decoratore passa il mock di check_and_trigger_alerts come primo argomento
@patch('app.services.price_service.check_and_trigger_alerts')
def test_update_and_get_price(mock_check_alerts):

    mock_db = MagicMock()
    mock_brent_service = MagicMock()
    mock_brent_service.fetch_current_price.return_value = 90.0
    
    mock_price_repo = MagicMock()
    expected_value = BrentValue(value=90.0)
    mock_price_repo.save_price.return_value = expected_value
    
    # setup del servizio con il DB mockato
    service = PriceService(db=mock_db)
    service.brent_service = mock_brent_service
    service.price_repo = mock_price_repo

    result = service.update_and_get_price()

    assert result == expected_value
    
    # Verifica che la funzione patchata sia stata chiamata correttamente
    mock_check_alerts.assert_called_once_with(db=mock_db, current_price=90.0)