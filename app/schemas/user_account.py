from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class UserAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    bank_account_id: int
    label: str | None
    is_primary: bool
    status: str
    created_at: datetime
    updated_at: datetime


class UserAccountCreate(BaseModel):
    bank_account_id: int
    label: str | None = None
    is_primary: bool = False


class UserAccountUpdate(BaseModel):
    label: str | None = None
    is_primary: bool | None = None
    status: Literal["active", "inactive"] | None = None
