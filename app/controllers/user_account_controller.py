from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user_account import UserAccountCreate, UserAccountUpdate, UserAccountResponse
from app.services.user_account_service import UserAccountService
from app.repos.user_account_repo import UserAccountRepository

router = APIRouter(prefix="/api/v1/user-accounts", tags=["User Accounts"])

@router.post("", response_model=UserAccountResponse, status_code=status.HTTP_201_CREATED)
def create_user_account(
    obj_in: UserAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserAccountService(db)
    return service.create(current_user.id, obj_in)

@router.get("", response_model=list[UserAccountResponse])
def get_user_accounts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = UserAccountRepository(db)
    return repo.list_by_user(current_user.id)

@router.get("/{id}", response_model=UserAccountResponse)
def get_user_account_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = UserAccountRepository(db)
    user_acc = repo.get_by_id_for_user(id, current_user.id)
    if not user_acc:
        raise NotFoundError("User account not found")
    return user_acc

@router.put("/{id}", response_model=UserAccountResponse)
def update_user_account(
    id: int,
    obj_in: UserAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserAccountService(db)
    return service.update(current_user.id, id, obj_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserAccountService(db)
    service.delete(current_user.id, id)
    return None