from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.bank_account import BankAccount
    from app.models.user_account import UserAccount


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    bank_accounts: Mapped[list["BankAccount"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    user_accounts: Mapped[list["UserAccount"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
