from sqlalchemy.orm import Session
from app.repos.user_account_repo import UserAccountRepository
from app.repos.bank_account_repo import BankAccountRepository
from app.schemas.user_account import UserAccountCreate, UserAccountUpdate
from app.core.exceptions import ConflictError, NotFoundError

class UserAccountService:
    def __init__(self, db: Session):
        self.repo = UserAccountRepository(db)
        self.bank_repo = BankAccountRepository(db)

    def create(self, user_id: int, obj_in: UserAccountCreate):
        bank_acc = self.bank_repo.get_by_id(obj_in.bank_account_id)
        if not bank_acc or bank_acc.user_id != user_id:
            raise NotFoundError("Bank account not found or does not belong to user")

        existing = self.repo.get_by_user_and_bank(user_id, obj_in.bank_account_id)
        if existing:
            raise ConflictError("User account registration already exists")

        if obj_in.is_primary:
            self.repo.unset_primary_for_user(user_id)

        return self.repo.create(user_id, obj_in)

    def update(self, user_id: int, account_id: int, obj_in: UserAccountUpdate):
        user_acc = self.repo.get_by_id_for_user(account_id, user_id)
        if not user_acc:
            raise NotFoundError("User account registration not found")

        if obj_in.is_primary:
            self.repo.unset_primary_for_user(user_id)

        return self.repo.update(user_acc, obj_in)

    def delete(self, user_id: int, account_id: int):
        user_acc = self.repo.get_by_id_for_user(account_id, user_id)
        if not user_acc:
            raise NotFoundError("User account registration not found")
        self.repo.delete(user_acc)