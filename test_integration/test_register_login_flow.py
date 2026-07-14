import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api import auth as auth_api
from app.api import prices as prices_api
from app.core.database import Base, engine as app_engine, SessionLocal
from main import app


@pytest.fixture
def client():
    """
    Crea un client di test con un database SQLite temporaneo.
    Così l'integration test non dipende dal database reale del progetto.
    """
    connection = app_engine.connect()
    transaction = connection.begin()
    SessionLocal.configure(bind=connection)

    Base.metadata.create_all(bind=connection)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[auth_api.get_db] = override_get_db
    app.dependency_overrides[prices_api.get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    transaction.rollback()
    connection.close()
    SessionLocal.configure(bind=app_engine)
    app.dependency_overrides.clear()


def test_register_login_and_read_price_flow(client, monkeypatch):
    """
    Integration test end-to-end che verifica:
    1. registrazione utente,
    2. login,
    3. lettura del prezzo corrente e salvataggio nello storico.
    """
    # 1. Registrazione dell'utente
    register_payload = {
        "username": "brentfan",
        "email": "brent@example.com",
        "password": "secret123",
    }
    register_response = client.post("/auth/register", json=register_payload)

    assert register_response.status_code == 200
    assert register_response.json()["status"] == "success"

    # 2. Login con le credenziali appena create
    login_payload = {
        "username": "brentfan",
        "password": "secret123",
    }
    login_response = client.post("/auth/login", json=login_payload)

    assert login_response.status_code == 200
    assert login_response.json()["token_type"] == "bearer"
    assert login_response.json()["access_token"].startswith("token_fittizio_per_")

    # 3. Lettura del prezzo corrente
    def fake_fetch_current_price(self):
        return 123.45

    monkeypatch.setattr(
        "app.services.brent_service.BrentService.fetch_current_price",
        fake_fetch_current_price,
    )

    current_price_response = client.get("/prices/current")
    assert current_price_response.status_code == 200

    current_price_payload = current_price_response.json()["data"]
    assert current_price_payload["price"] == 123.45

    # Verifichiamo anche che il prezzo sia stato salvato nello storico
    history_response = client.get("/prices/history")
    assert history_response.status_code == 200

    history_payload = history_response.json()["data"]
    assert history_payload[0]["price"] == 123.45
