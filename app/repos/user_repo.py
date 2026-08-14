from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repos.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def create(
        self, email: str, hashed_password: str, full_name: str | None = None
    ) -> User:
        user = User(
            email=email, hashed_password=hashed_password, full_name=full_name
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
