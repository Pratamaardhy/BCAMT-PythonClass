from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field
from pydantic import BaseModel, Field
from typing import Optional


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

class BankAccountBase(BaseModel):
    account_number: str
    account_name: str
    bank_name: str
    balance: float = Field(default=0.0, ge=0)

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountUpdate(BaseModel):
    account_name: Optional[str] = None
    bank_name: Optional[str] = None
    balance: Optional[float] = Field(default=None, ge=0)

class BankAccountResponse(BankAccountBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True