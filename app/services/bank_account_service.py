from decimal import Decimal

from app.core.exceptions import ConflictError, NotFoundError
from app.models.bank_account import BankAccount
from app.repos.bank_account_repo import BankAccountRepository


class BankAccountService:
    def __init__(self, repo: BankAccountRepository) -> None:
        self.repo = repo

    def list_accounts(
        self, user_id: int, *, skip: int = 0, limit: int = 100
    ) -> list[BankAccount]:
        return self.repo.list_by_user(user_id, skip=skip, limit=limit)

    def get_account(self, account_id: int, user_id: int) -> BankAccount:
        account = self.repo.get_by_id_for_user(account_id, user_id)
        if not account:
            raise NotFoundError("Bank account not found")
        return account
    
    def create_account(
        self,
        user_id: int,
        *,
        account_number: str,
        account_name: str,
        bank_name: str,
        balance: Decimal,
    ) -> BankAccount:
        if self.repo.get_by_account_number(account_number):
            raise ConflictError("Account number already registered")
        return self.repo.create_account(
            user_id=user_id,
            account_number=account_number,
            account_name=account_name,
            bank_name=bank_name,
            balance=balance,
        )

    def update_account(
        self,
        account_id: int,
        user_id: int,
        *,
        account_name: str,
        bank_name: str,
        balance: Decimal,
    ) -> BankAccount:
        account = self.get_account(account_id, user_id)
        return self.repo.update_account(
            account,
            account_name=account_name,
            bank_name=bank_name,
            balance=balance,
        )

    def delete_account(self, account_id: int, user_id: int) -> None:
        account = self.get_account(account_id, user_id)
        self.repo.delete_account(account)
