from app.core.exceptions import ConflictError, NotFoundError
from app.models.user_account import UserAccount
from app.repos.bank_account_repo import BankAccountRepository
from app.repos.user_account_repo import UserAccountRepository


class UserAccountService:
    def __init__(
        self,
        repo: UserAccountRepository,
        bank_account_repo: BankAccountRepository,
    ) -> None:
        self.repo = repo
        self.bank_account_repo = bank_account_repo

    def list_accounts(
        self, user_id: int, *, skip: int = 0, limit: int = 100
    ) -> list[UserAccount]:
        return self.repo.list_by_user(user_id, skip=skip, limit=limit)

    def get_account(self, user_account_id: int, user_id: int) -> UserAccount:
        account = self.repo.get_by_id_for_user(user_account_id, user_id)
        if not account:
            raise NotFoundError("User account not found")
        return account

    def create_account(
        self,
        user_id: int,
        *,
        bank_account_id: int,
        label: str | None,
        is_primary: bool,
    ) -> UserAccount:
        bank_account = self.bank_account_repo.get_by_id_for_user(
            bank_account_id, user_id
        )
        if not bank_account:
            raise NotFoundError("Bank account not found")

        if self.repo.get_by_user_and_bank_account(user_id, bank_account_id):
            raise ConflictError("Bank account already registered")

        account = self.repo.create_account(
            user_id=user_id,
            bank_account_id=bank_account_id,
            label=label,
            is_primary=is_primary,
        )
        if is_primary:
            self.repo.unset_other_primaries(user_id, exclude_id=account.id)
        return account

    def update_account(
        self,
        user_account_id: int,
        user_id: int,
        *,
        label: str | None,
        is_primary: bool | None,
        status: str | None,
    ) -> UserAccount:
        account = self.get_account(user_account_id, user_id)
        account = self.repo.update_account(
            account, label=label, is_primary=is_primary, status=status
        )
        if is_primary:
            self.repo.unset_other_primaries(user_id, exclude_id=account.id)
        return account

    def delete_account(self, user_account_id: int, user_id: int) -> None:
        account = self.get_account(user_account_id, user_id)
        self.repo.delete_account(account)
