from typing import Any

import jwt

from app.core.exceptions import (
    ConflictError,
    InvalidCredentialsError,
    UnauthorizedError,
)
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repos.user_repo import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def register(
        self, email: str, password: str, full_name: str | None = None
    ) -> User:
        email = email.strip().lower()
        if self.user_repo.get_by_email(email):
            raise ConflictError("Email already registered")
        return self.user_repo.create(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
        )

    def authenticate(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email.strip().lower())
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")
        if not user.is_active:
            raise InvalidCredentialsError("User is inactive")
        return user

    def issue_token(self, user: User) -> str:
        return create_access_token(subject=user.id)

    def get_user_from_token(self, token: str) -> User:
        try:
            payload: dict[str, Any] = decode_access_token(token)
        except jwt.PyJWTError:
            raise UnauthorizedError("Invalid or expired token")
        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedError("Invalid token payload")
        user = self.user_repo.get(int(user_id))
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")
        return user
