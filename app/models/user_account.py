from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


if TYPE_CHECKING:
    from app.models.bank_account import BankAccount
    from app.models.user import User


class UserAccount(Base, TimestampMixin):
    __tablename__ = "user_accounts"
__tablename__ = "user_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    label = Column(String(255), nullable=True)
    is_primary = Column(Boolean, default=False)
    status = Column(String(20), default="active")

    __table_args__ = (
        UniqueConstraint("user_id", "bank_account_id", name="uq_user_bank_account"),
    )

    user = relationship("User", back_populates="user_accounts")
    bank_account = relationship("BankAccount", back_populates="user_accounts")