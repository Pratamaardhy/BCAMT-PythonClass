import pytest

from app.core.exceptions import ConflictError, NotFoundError
from app.repos.bank_account_repo import BankAccountRepository
from app.repos.user_account_repo import UserAccountRepository
from app.services.user_account_service import UserAccountService


@pytest.fixture
def bank_account_repo(db_session):
    return BankAccountRepository(db_session)


@pytest.fixture
def service(db_session):
    return UserAccountService(
        UserAccountRepository(db_session), BankAccountRepository(db_session)
    )


def create_bank_account(bank_account_repo, user_id, account_number):
    return bank_account_repo.create_account(
        user_id=user_id,
        account_number=account_number,
        account_name="My Account",
        bank_name="My Bank",
        balance=1000.0,
    )


#TEST

def test_create_berhasil(service, bank_account_repo):
    bank_account = create_bank_account(bank_account_repo, 1, "1111")

    user_account = service.create_account(
        1, bank_account_id=bank_account.id, label="Gaji", is_primary=False
    )

    assert user_account.id is not None
    assert user_account.user_id == 1
    assert user_account.bank_account_id == bank_account.id
    assert user_account.label == "Gaji"
    assert user_account.status == "active"


def test_create_bank_account_milik_user_lain(service, bank_account_repo):
    bank_account = create_bank_account(bank_account_repo, 2, "1111")

    with pytest.raises(NotFoundError):
        service.create_account(
            1, bank_account_id=bank_account.id, label=None, is_primary=False
        )


def test_create_bank_account_tidak_ada(service):
    with pytest.raises(NotFoundError):
        service.create_account(
            1, bank_account_id=999, label=None, is_primary=False
        )


def test_create_duplikat(service, bank_account_repo):
    bank_account = create_bank_account(bank_account_repo, 1, "1111")
    service.create_account(
        1, bank_account_id=bank_account.id, label=None, is_primary=False
    )

    with pytest.raises(ConflictError):
        service.create_account(
            1, bank_account_id=bank_account.id, label=None, is_primary=False
        )


def test_create_is_primary_unset_yang_lama(service, bank_account_repo):
    bank_account1 = create_bank_account(bank_account_repo, 1, "1111")
    bank_account2 = create_bank_account(bank_account_repo, 1, "2222")

    first = service.create_account(
        1, bank_account_id=bank_account1.id, label=None, is_primary=True
    )
    second = service.create_account(
        1, bank_account_id=bank_account2.id, label=None, is_primary=True
    )

    first_after = service.get_account(first.id, 1)
    assert first_after.is_primary is False
    assert second.is_primary is True


def test_list_hanya_milik_user(service, bank_account_repo):
    bank_account1 = create_bank_account(bank_account_repo, 1, "1111")
    bank_account2 = create_bank_account(bank_account_repo, 2, "2222")
    service.create_account(
        1, bank_account_id=bank_account1.id, label=None, is_primary=False
    )
    service.create_account(
        2, bank_account_id=bank_account2.id, label=None, is_primary=False
    )

    result = service.list_accounts(1)

    assert len(result) == 1
    assert result[0].user_id == 1


def test_get_by_id_berhasil(service, bank_account_repo):
    bank_account = create_bank_account(bank_account_repo, 1, "1111")
    created = service.create_account(
        1, bank_account_id=bank_account.id, label=None, is_primary=False
    )

    fetched = service.get_account(created.id, 1)

    assert fetched.id == created.id


def test_get_by_id_milik_user_lain(service, bank_account_repo):
    bank_account = create_bank_account(bank_account_repo, 1, "1111")
    created = service.create_account(
        1, bank_account_id=bank_account.id, label=None, is_primary=False
    )

    with pytest.raises(NotFoundError):
        service.get_account(created.id, 2)


def test_update_berhasil(service, bank_account_repo):
    bank_account = create_bank_account(bank_account_repo, 1, "1111")
    created = service.create_account(
        1, bank_account_id=bank_account.id, label="Lama", is_primary=False
    )

    updated = service.update_account(
        created.id,
        1,
        label="Baru",
        is_primary=True,
        status="inactive",
    )

    assert updated.label == "Baru"
    assert updated.is_primary is True
    assert updated.status == "inactive"


def test_update_milik_user_lain(service, bank_account_repo):
    bank_account = create_bank_account(bank_account_repo, 1, "1111")
    created = service.create_account(
        1, bank_account_id=bank_account.id, label=None, is_primary=False
    )

    with pytest.raises(NotFoundError):
        service.update_account(
            created.id, 2, label="Baru", is_primary=None, status=None
        )


def test_delete_berhasil(service, bank_account_repo):
    bank_account = create_bank_account(bank_account_repo, 1, "1111")
    created = service.create_account(
        1, bank_account_id=bank_account.id, label=None, is_primary=False
    )

    service.delete_account(created.id, 1)

    assert service.list_accounts(1) == []


def test_delete_milik_user_lain(service, bank_account_repo):
    bank_account = create_bank_account(bank_account_repo, 1, "1111")
    created = service.create_account(
        1, bank_account_id=bank_account.id, label=None, is_primary=False
    )

    with pytest.raises(NotFoundError):
        service.delete_account(created.id, 2)
