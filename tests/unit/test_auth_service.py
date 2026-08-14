import pytest
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, InvalidCredentialsError
from app.repos.user_repo import UserRepository
from app.services.auth_service import AuthService


def make_service(db: Session) -> AuthService:
    return AuthService(UserRepository(db))


def test_register_success(db_session):
    service = make_service(db_session)
    user = service.register("user@example.com", "supersecret", "User")

    assert user.id is not None
    assert user.email == "user@example.com"
    assert user.hashed_password != "supersecret"
    assert user.is_active is True


def test_register_lowercases_email(db_session):
    service = make_service(db_session)
    user = service.register("UPPER@Example.com", "supersecret")

    assert user.email == "upper@example.com"


def test_register_duplicate_email_raises(db_session):
    service = make_service(db_session)
    service.register("dup@example.com", "supersecret")

    with pytest.raises(ConflictError):
        service.register("dup@example.com", "anotherpass")


def test_authenticate_success(db_session):
    service = make_service(db_session)
    service.register("auth@example.com", "supersecret")

    user = service.authenticate("auth@example.com", "supersecret")

    assert user.email == "auth@example.com"


def test_authenticate_wrong_password_raises(db_session):
    service = make_service(db_session)
    service.register("auth@example.com", "supersecret")

    with pytest.raises(InvalidCredentialsError):
        service.authenticate("auth@example.com", "wrongpass")


def test_authenticate_unknown_email_raises(db_session):
    service = make_service(db_session)

    with pytest.raises(InvalidCredentialsError):
        service.authenticate("nobody@example.com", "supersecret")


def test_issue_and_validate_token(db_session):
    service = make_service(db_session)
    user = service.register("token@example.com", "supersecret")

    token = service.issue_token(user)
    decoded = service.get_user_from_token(token)

    assert decoded.id == user.id
    assert decoded.email == "token@example.com"


def test_get_user_from_invalid_token_raises(db_session):
    service = make_service(db_session)

    with pytest.raises(Exception):
        service.get_user_from_token("not-a-valid-jwt")
