from sqlalchemy.orm import Session
from app.models.bank_account import BankAccount
from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate

class BankAccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, account_id: int) -> Optional[BankAccount]:
        return self.db.query(BankAccount).filter(BankAccount.id == account_id).first()

    def get_by_account_number(self, account_number: str) -> Optional[BankAccount]:
        return self.db.query(BankAccount).filter(BankAccount.account_number == account_number).first()

    def get_all_by_user(self, user_id: int) -> list[BankAccount]:
        return self.db.query(BankAccount).filter(BankAccount.user_id == user_id).all()

    def create(self, user_id: int, obj_in: BankAccountCreate) -> BankAccount:
        db_obj = BankAccount(
            user_id=user_id,
            account_number=obj_in.account_number,
            account_name=obj_in.account_name,
            bank_name=obj_in.bank_name,
            balance=obj_in.balance
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: BankAccount, obj_in: BankAccountUpdate) -> BankAccount:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: BankAccount) -> None:
        self.db.delete(db_obj)
        self.db.commit()