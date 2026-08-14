from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BankAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_number: str
    account_name: str
    bank_name: str
    balance: Decimal
    user_id: int
    created_at: datetime
    updated_at: datetime
