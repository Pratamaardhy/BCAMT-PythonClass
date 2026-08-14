from typing import Annotated

from fastapi import APIRouter, Query

from app.deps import CurrentUser, DbDep
from app.repos.bank_account_repo import BankAccountRepository
from app.schemas.bank_account import BankAccountResponse
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
