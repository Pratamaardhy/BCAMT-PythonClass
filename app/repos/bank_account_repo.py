from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bank_account import BankAccount
from app.repos.base import BaseRepository


class BankAccountRepository(BaseRepository[BankAccount]):
    model = BankAccount

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_user(
        self, user_id: int, *, skip: int = 0, limit: int = 100
    ) -> list[BankAccount]:
        stmt = (
            select(BankAccount)
            .where(BankAccount.user_id == user_id)
            .order_by(BankAccount.id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def get_by_id_for_user(
        self, account_id: int, user_id: int
    ) -> BankAccount | None:
        stmt = select(BankAccount).where(
            BankAccount.id == account_id, BankAccount.user_id == user_id
        )
        return self.db.scalar(stmt)
    
    def get_by_account_number(self, account_number: str) -> BankAccount | None:
        stmt = select(BankAccount).where(
            BankAccount.account_number == account_number
        )
        return self.db.scalar(stmt)

    def create_account(
        self,
        *,
        user_id: int,
        account_number: str,
        account_name: str,
        bank_name: str,
        balance: Decimal,
    ) -> BankAccount:
        account = BankAccount(
            user_id=user_id,
            account_number=account_number,
            account_name=account_name,
            bank_name=bank_name,
            balance=balance,
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update_account(
        self,
        account: BankAccount,
        *,
        account_name: str,
        bank_name: str,
        balance: Decimal,
    ) -> BankAccount:
        account.account_name = account_name
        account.bank_name = bank_name
        account.balance = balance
        self.db.commit()
        self.db.refresh(account)
        return account

    def delete_account(self, account: BankAccount) -> None:
        self.db.delete(account)
        self.db.commit()
