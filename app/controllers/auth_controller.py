from fastapi import APIRouter

from app.deps import DbDep
from app.repos.user_repo import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201,
    summary="Register new user",
)
def register(payload: RegisterRequest, db: DbDep):
    service = AuthService(UserRepository(db))
    user = service.register(
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
    )
    return user


@router.post("/login", response_model=TokenResponse, summary="Login and get JWT")
def login(payload: LoginRequest, db: DbDep):
    service = AuthService(UserRepository(db))
    user = service.authenticate(
        email=payload.email, password=payload.password
    )
    return TokenResponse(access_token=service.issue_token(user))
