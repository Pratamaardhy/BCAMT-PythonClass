from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_account import UserAccount
from app.repos.base import BaseRepository


class UserAccountRepository(BaseRepository[UserAccount]):
    model = UserAccount

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_user(
        self, user_id: int, *, skip: int = 0, limit: int = 100
    ) -> list[UserAccount]:
        stmt = (
            select(UserAccount)
            .where(UserAccount.user_id == user_id)
            .order_by(UserAccount.id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def get_by_id_for_user(
        self, user_account_id: int, user_id: int
    ) -> UserAccount | None:
        stmt = select(UserAccount).where(
            UserAccount.id == user_account_id, UserAccount.user_id == user_id
        )
        return self.db.scalar(stmt)

    def get_by_user_and_bank_account(
        self, user_id: int, bank_account_id: int
    ) -> UserAccount | None:
        stmt = select(UserAccount).where(
            UserAccount.user_id == user_id,
            UserAccount.bank_account_id == bank_account_id,
        )
        return self.db.scalar(stmt)

    def unset_other_primaries(
        self, user_id: int, *, exclude_id: int | None = None
    ) -> None:
        stmt = select(UserAccount).where(
            UserAccount.user_id == user_id, UserAccount.is_primary.is_(True)
        )
        if exclude_id is not None:
            stmt = stmt.where(UserAccount.id != exclude_id)
        for account in self.db.scalars(stmt).all():
            account.is_primary = False
        self.db.flush()

    def create_account(
        self,
        *,
        user_id: int,
        bank_account_id: int,
        label: str | None,
        is_primary: bool,
    ) -> UserAccount:
        account = UserAccount(
            user_id=user_id,
            bank_account_id=bank_account_id,
            label=label,
            is_primary=is_primary,
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def update_account(
        self,
        account: UserAccount,
        *,
        label: str | None,
        is_primary: bool | None,
        status: str | None,
    ) -> UserAccount:
        if label is not None:
            account.label = label
        if is_primary is not None:
            account.is_primary = is_primary
        if status is not None:
            account.status = status
        self.db.commit()
        self.db.refresh(account)
        return account

    def delete_account(self, account: UserAccount) -> None:
        self.db.delete(account)
        self.db.commit()
