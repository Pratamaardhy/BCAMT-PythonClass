from typing import Annotated

from fastapi import APIRouter, Query, Response

from app.deps import CurrentUser, DbDep
from app.repos.bank_account_repo import BankAccountRepository
from app.schemas.bank_account import BankAccountCreate, BankAccountResponse, BankAccountUpdate
from app.services.bank_account_service import BankAccountService

router = APIRouter(prefix="/bank-accounts", tags=["bank-accounts"])


@router.get(
    "",
    response_model=list[BankAccountResponse],
    summary="Get all bank accounts of current user",
)
def list_bank_accounts(
    db: DbDep,
    current_user: CurrentUser,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    service = BankAccountService(BankAccountRepository(db))
    return service.list_accounts(current_user.id, skip=skip, limit=limit)


@router.get(
    "/{account_id}",
    response_model=BankAccountResponse,
    summary="Get bank account by id",
)
def get_bank_account(account_id: int, db: DbDep, current_user: CurrentUser):
    service = BankAccountService(BankAccountRepository(db))
    return service.get_account(account_id, current_user.id)


@router.post(
    "",
    response_model=BankAccountResponse,
    status_code=201,
    summary="Create a new bank account",
)
def create_bank_account(
    payload: BankAccountCreate, db: DbDep, current_user: CurrentUser
):
    service = BankAccountService(BankAccountRepository(db))
    return service.create_account(
        current_user.id,
        account_number=payload.account_number,
        account_name=payload.account_name,
        bank_name=payload.bank_name,
        balance=payload.balance,
    )


@router.put(
    "/{account_id}",
    response_model=BankAccountResponse,
    status_code=200,
    summary="Update a bank account",
)
def update_bank_account(
    account_id: int,
    payload: BankAccountUpdate,
    db: DbDep,
    current_user: CurrentUser,
):
    service = BankAccountService(BankAccountRepository(db))
    return service.update_account(
        account_id,
        current_user.id,
        account_name=payload.account_name,
        bank_name=payload.bank_name,
        balance=payload.balance,
    )


@router.delete(
    "/{account_id}",
    status_code=204,
    summary="Delete a bank account",
)
def delete_bank_account(
    account_id: int, db: DbDep, current_user: CurrentUser
):
    
    service = BankAccountService(BankAccountRepository(db))
    service.delete_account(account_id, current_user.id)
    return Response(status_code=204)