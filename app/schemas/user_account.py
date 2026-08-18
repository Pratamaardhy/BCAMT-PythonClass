from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class UserAccountResponse(BaseModel):
    bank_account_id: int
    label: Optional[str] = None
    is_primary: Optional[bool] = False

class UserAccountUpdate(BaseModel):
    label: Optional[str] = None
    is_primary: Optional[bool] = None
    status: Optional[Literal["active", "inactive"]] = None

class UserAccountResponse(BaseModel):
    id: int
    user_id: int
    bank_account_id: int
    label: Optional[str]
    is_primary: bool
    status: str

    class Config:
        from_attributes = True
