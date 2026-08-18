from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


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
    
class BankAccountCreate(BaseModel):
    account_number: str = Field(min_length=1, max_length=50)
    account_name: str = Field(min_length=1, max_length=255)
    bank_name: str = Field(min_length=1, max_length=255)
    balance: Decimal = Field(default=Decimal("0.00"), ge=0)


class BankAccountUpdate(BaseModel):
    account_name: str = Field(min_length=1, max_length=255)
    bank_name: str = Field(min_length=1, max_length=255)
    balance: Decimal = Field(ge=0)
