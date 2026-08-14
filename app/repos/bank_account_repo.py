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
