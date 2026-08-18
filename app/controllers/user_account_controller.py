from typing import Annotated

from fastapi import APIRouter, Query, Response

from app.deps import CurrentUser, DbDep
from app.repos.bank_account_repo import BankAccountRepository
from app.repos.user_account_repo import UserAccountRepository
from app.schemas.user_account import (
    UserAccountCreate,
    UserAccountResponse,
    UserAccountUpdate,
)
from app.services.user_account_service import UserAccountService

router = APIRouter(prefix="/user-accounts", tags=["user-accounts"])


def _service(db: DbDep) -> UserAccountService:
    return UserAccountService(UserAccountRepository(db), BankAccountRepository(db))


@router.get(
    "",
    response_model=list[UserAccountResponse],
    summary="Get all registered bank accounts of current user",
)
def list_user_accounts(
    db: DbDep,
    current_user: CurrentUser,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return _service(db).list_accounts(current_user.id, skip=skip, limit=limit)


@router.get(
    "/{user_account_id}",
    response_model=UserAccountResponse,
    summary="Get a registered bank account by id",
)
def get_user_account(user_account_id: int, db: DbDep, current_user: CurrentUser):
    return _service(db).get_account(user_account_id, current_user.id)


@router.post(
    "",
    response_model=UserAccountResponse,
    status_code=201,
    summary="Register a bank account to current user",
)
def create_user_account(
    payload: UserAccountCreate, db: DbDep, current_user: CurrentUser
):
    return _service(db).create_account(
        current_user.id,
        bank_account_id=payload.bank_account_id,
        label=payload.label,
        is_primary=payload.is_primary,
    )


@router.put(
    "/{user_account_id}",
    response_model=UserAccountResponse,
    status_code=200,
    summary="Update a registered bank account",
)
def update_user_account(
    user_account_id: int,
    payload: UserAccountUpdate,
    db: DbDep,
    current_user: CurrentUser,
):
    return _service(db).update_account(
        user_account_id,
        current_user.id,
        label=payload.label,
        is_primary=payload.is_primary,
        status=payload.status,
    )


@router.delete(
    "/{user_account_id}",
    status_code=204,
    summary="Delete a registered bank account",
)
def delete_user_account(
    user_account_id: int, db: DbDep, current_user: CurrentUser
):
    _service(db).delete_account(user_account_id, current_user.id)
    return Response(status_code=204)
