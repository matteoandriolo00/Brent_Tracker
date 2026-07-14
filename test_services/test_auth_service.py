from unittest.mock import MagicMock

import pytest

from app.models.user import User
from app.services.auth_service import AuthService


@pytest.fixture
def service() -> AuthService:
    service = AuthService(db_or_repo=MagicMock())
    service.user_repository = MagicMock()
    return service


def test_get_password_hash_returns_a_hash_that_can_be_verified(service: AuthService) -> None:
    password = "secret123"

    hashed_password = service.get_password_hash(password)

    assert hashed_password != password
    assert service.verify_password(password, hashed_password) is True


def test_register_user_normalizes_data_and_creates_user(service: AuthService) -> None:
    service.user_repository.get_user_by_email.return_value = None
    service.user_repository.get_user_by_username.return_value = None
    service.user_repository.create_user.side_effect = lambda user: user

    created_user = service.register_user(
        email="Test@Example.com",
        password="secret123",
        username="test_username",
    )

    assert created_user.email == "test@example.com"
    assert created_user.username == "test_username"
    assert created_user.password != "secret123"
    assert service.verify_password("secret123", created_user.password) is True
    service.user_repository.get_user_by_email.assert_called_once_with("test@example.com")
    service.user_repository.create_user.assert_called_once()


def test_register_user_raises_when_username_already_exists(service: AuthService) -> None:
    existing_user = User(username="existing", email="exists@example.com", password="hashed")
    service.user_repository.get_user_by_email.return_value = None
    service.user_repository.get_user_by_username.return_value = existing_user

    with pytest.raises(ValueError, match="Username già registrato"):
        service.register_user(email="test@example.com", password="secret123", username="existing")

    service.user_repository.create_user.assert_not_called()


def test_authenticate_user_returns_user_for_valid_credentials(service: AuthService) -> None:
    user = User(username="test", email="test@example.com", password=service.get_password_hash("secret123"))
    service.user_repository.get_user_by_username.return_value = user

    authenticated_user = service.authenticate_user("test", "secret123")

    assert authenticated_user is user


def test_authenticate_user_returns_none_for_invalid_password(service: AuthService) -> None:
    user = User(username="test", email="test@example.com", password=service.get_password_hash("secret123"))
    service.user_repository.get_user_by_username.return_value = user

    authenticated_user = service.authenticate_user("test", "wrongpass")

    assert authenticated_user is None
