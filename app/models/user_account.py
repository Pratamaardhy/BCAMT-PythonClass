from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.bank_account import BankAccount
    from app.models.user import User


class UserAccount(Base, TimestampMixin):
    __tablename__ = "user_accounts"
    __table_args__ = (
        UniqueConstraint("user_id", "bank_account_id", name="uq_user_bank_account"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    bank_account_id: Mapped[int] = mapped_column(
        ForeignKey("bank_accounts.id", ondelete="CASCADE"), index=True, nullable=False
    )
    label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), default="active", nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="user_accounts")
    bank_account: Mapped["BankAccount"] = relationship(back_populates="user_accounts")
