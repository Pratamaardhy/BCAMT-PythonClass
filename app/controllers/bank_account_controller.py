from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate, BankAccountResponse
from app.services.bank_account_service import BankAccountService

router = APIRouter(prefix="/api/v1/bank-accounts", tags=["Bank Accounts"])

@router.post("", response_model=BankAccountResponse, status_code=status.HTTP_201_CREATED)
def create_bank_account(
    obj_in: BankAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = BankAccountService(db)
    return service.create_account(current_user.id, obj_in)

@router.get("", response_model=list[BankAccountResponse])
def get_bank_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = BankAccountRepository(db)
    return repo.get_all_by_user(current_user.id)

@router.put("/{id}", response_model=BankAccountResponse)
def update_bank_account(
    id: int,
    obj_in: BankAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = BankAccountService(db)
    return service.update_account(current_user.id, id, obj_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank_account(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = BankAccountService(db)
    service.delete_account(current_user.id, id)
    return None