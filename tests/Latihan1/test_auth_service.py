import pytest

from app.core.exceptions import ConflictError, InvalidCredentialsError, UnauthorizedError
from app.repos.user_repo import UserRepository
from app.services.auth_service import AuthService



#Create DB_Session kosong untuk testing + userRepository yang menggunakan DB_Session tersebut

#decorator fixture = kasih tau kalau code ini tuh bukan test biasa, tapi untuk inject dependency ke test function
@pytest.fixture
def auth_service(db_session):
    return AuthService(UserRepository(db_session))


def test_register_success(auth_service):
    user = auth_service.register(email="test@example.com", password="supersecret")

    assert user.id is not None
    assert user.hashed_password != "supersecret"
    assert user.is_active is True

def test_register_lowercases_email(auth_service):
    user = auth_service.register(email="TeSt@Example.COM", password="supersecret")

    assert user.email == "test@example.com"
    
def test_email_dup_registration(auth_service):
    auth_service.register(email="111@gmail.com", password="rahasia")
    with pytest.raises(ConflictError):
        auth_service.register(email="111@gmail.com", password="rahasia")

def test_authenticate_success(auth_service):
    auth_service.register(email="awikwok@gmail.com", password="rahasia")
    user = auth_service.authenticate(email="awikwok@gmail.com", password="rahasia")

    assert user is not None
    assert user.email == "awikwok@gmail.com"
    
def test_authenticate_invalid_credentials_pass(auth_service):
    auth_service.register(email="awikwok@gmail.com", password="rahasia")
    with pytest.raises(InvalidCredentialsError):
        auth_service.authenticate(email="awikwok@gmail.com", password="wrongpassword")
        
def test_authenticate_invalid_credentials_email(auth_service):
    auth_service.register(email="coffebreak@gmail.com", password="rahasia")
    with pytest.raises(InvalidCredentialsError):
        auth_service.authenticate(email="emailsahaini@gmail.com", password="rahasia")
        
def test_get_issue_token_and_get_user_from_token(auth_service):
    user = auth_service.register(email="valdi@gmail.com", password="rahasia")
    token = auth_service.issue_token(user)  
    retrieved_user = auth_service.get_user_from_token(token)

    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    
def test_get_user_from_token_invalid_token(auth_service):
    with pytest.raises(UnauthorizedError):
        auth_service.get_user_from_token("tokenaosdnajkwnd")