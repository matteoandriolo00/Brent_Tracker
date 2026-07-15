from unittest.mock import patch, MagicMock
from app.services.brent_service import BrentService
from hypothesis import given, settings, strategies as st

@given(st.floats(min_value=0, max_value=200))
@settings(max_examples=50, deadline=None)
def test_fetch_current_price_success(price):
    # mock per la risposta della richiesta HTTP
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'chart': {
            'result': [{
                'meta': {
                    'regularMarketPrice': 95.0
                }
            }]
        }
    }
    mock_response.raise_for_status.return_value = None  # Simula una risposta OK

    # 2. Patchiamo requests.get per restituire il nostro mock
    with patch('app.services.brent_service.requests.get', return_value=mock_response):
        brent_service = BrentService()
        price = brent_service.fetch_current_price()

        # 3. Asserzioni
        assert price == 95.0
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()