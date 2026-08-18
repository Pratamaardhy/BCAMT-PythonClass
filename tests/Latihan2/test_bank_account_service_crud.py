
import pytest

from app.core.exceptions import ConflictError, NotFoundError
from app.repos.bank_account_repo import BankAccountRepository
from app.services.bank_account_service import BankAccountService


@pytest.fixture
def service(db_session):
    return BankAccountService(BankAccountRepository(db_session))

def test_create_berhasil(service):
    account = service.create_account(
        user_id=1,
        account_number="1234567890",
        account_name="My Account",
        bank_name="My Bank",
        balance=1000.0,
    )
    assert account.id is not None
    assert account.account_number == "1234567890"
    assert account.account_name == "My Account"
    assert account.bank_name == "My Bank"
    assert account.balance == 1000.0
    
def test_create_dupp_account_number(service):
    service.create_account(
        user_id=1,
        account_number="1234567890",
        account_name="My Account",
        bank_name="My Bank",
        balance=1000.0,
    )
    with pytest.raises(ConflictError):
        service.create_account(
            user_id=1,
            account_number="1234567890",
            account_name="Another Account",
            bank_name="Another Bank",
            balance=500.0,
        )

def test_update_account(service):
    account = service.create_account(
        user_id=1,
        account_number="1234567890",
        account_name="My Account",
        bank_name="My Bank",
        balance=1000.0,
    )
    updated_account = service.update_account(
        account_id=account.id,
        user_id=1,
        account_name="Updated Account",
        bank_name="Updated Bank",
        balance=2000.0,
    )
    assert updated_account.account_name == "Updated Account"
    assert updated_account.bank_name == "Updated Bank"
    assert updated_account.balance == 2000.0
    
def test_update_account_punya_user_lain(service):
    account = service.create_account(
        user_id=1,
        account_number="1234567890",
        account_name="My Account",
        bank_name="My Bank",
        balance=1000.0,
    )
    with pytest.raises(NotFoundError):
        service.update_account(
            account_id=account.id,
            user_id=2,  # User lain
            account_name="Updated Account",
            bank_name="Updated Bank",
            balance=2000.0,
        )

def test_update_id_not_found(service):
    with pytest.raises(NotFoundError):
        service.update_account(
            account_id=999,  # ID yang tidak ada
            user_id=1,
            account_name="Updated Account",
            bank_name="Updated Bank",
            balance=2000.0,
        )

def test_delete_account(service):
    account = service.create_account(
        user_id=1,
        account_number="1234567890",
        account_name="My Account",
        bank_name="My Bank",
        balance=1000.0,
    )
    service.delete_account(account_id=account.id, user_id=1)
    with pytest.raises(NotFoundError):
        service.get_account(account_id=account.id, user_id=1)
        
def test_delete_account_punya_user_lain(service):
    account = service.create_account(
        user_id=1,
        account_number="1234567890",
        account_name="My Account",
        bank_name="My Bank",
        balance=1000.0,
    )
    with pytest.raises(NotFoundError):
        service.delete_account(
            account_id=account.id, 
            user_id=2)  # User lain