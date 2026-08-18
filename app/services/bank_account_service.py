from decimal import Decimal

from app.core.exceptions import ConflictError, NotFoundError
from app.models.bank_account import BankAccount
from app.repos.bank_account_repo import BankAccountRepository
from sqlalchemy.orm import Session
from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate


class BankAccountService:
def __init__(self, db: Session):
        self.repo = BankAccountRepository(db)

    def create_account(self, user_id: int, obj_in: BankAccountCreate):
        existing = self.repo.get_by_account_number(obj_in.account_number)
        if existing:
            raise ConflictError("Account number already exists")
        return self.repo.create(user_id, obj_in)

    def update_account(self, user_id: int, account_id: int, obj_in: BankAccountUpdate):
        account = self.repo.get_by_id(account_id)
        if not account or account.user_id != user_id:
            raise NotFoundError("Bank account not found")
        return self.repo.update(account, obj_in)

    def delete_account(self, user_id: int, account_id: int):
        account = self.repo.get_by_id(account_id)
        if not account or account.user_id != user_id:
            raise NotFoundError("Bank account not found")
        self.repo.delete(account)