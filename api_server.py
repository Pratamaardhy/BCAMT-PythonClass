import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import (create_engine, Column, BigInteger, String, Text, DateTime, func, Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_SCHEMA = os.environ.get("DB_SCHEMA", "sultan")

# Support JDBC-style DB URL or separate env vars
jdbc = os.environ.get("DB_URL") or os.environ.get("DATABASE_URL")
db_user = os.environ.get("DB_USERNAME") or os.environ.get("DB_USER") or os.environ.get("DB_USERNAME")
db_pass = os.environ.get("DB_PASSWORD") or os.environ.get("DB_PASS")
db_host = os.environ.get("DB_HOST", "localhost")
db_port = os.environ.get("DB_PORT", "5432")
db_name = os.environ.get("DB_NAME", "postgres")

if jdbc and jdbc.startswith("jdbc:postgresql://"):
    # jdbc:postgresql://host:port/dbname
    url = jdbc.replace("jdbc:", "")
    # if username/password provided in env, add them
    if db_user and db_pass:
        engine_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{url.split('://',1)[1]}"
    else:
        engine_url = f"postgresql+psycopg2://{url.split('://',1)[1]}"
else:
    # construct from components
    user = db_user or "postgres"
    pwd = db_pass or "12345"
    engine_url = f"postgresql+psycopg2://{user}:{pwd}@{db_host}:{db_port}/{db_name}"


engine = create_engine(engine_url, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class SecUser(Base):
    __tablename__ = "sec_users"
    __table_args__ = {"schema": DB_SCHEMA} if DB_SCHEMA else {}

    id = Column(BigInteger, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(150), unique=True)
    phone_number = Column(String(20), unique=True)
    password_hash = Column(String(255), nullable=False)
    user_type = Column(String(30), nullable=False)
    status = Column(String(30), nullable=False, default="ACTIVE")
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp())


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple API for Locust Testing")


class UserIn(BaseModel):
    username: str
    email: str
    phone_number: Optional[str] = None
    password: str
    user_type: Optional[str] = "CUSTOMER"


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    phone_number: Optional[str]
    user_type: str


@app.get("/api/items", response_model=list[UserOut])
def list_users(limit: int = 100):
    db = SessionLocal()
    try:
        rows = db.query(SecUser).limit(limit).all()
        return [UserOut(id=r.id, username=r.username, email=r.email, phone_number=r.phone_number, user_type=r.user_type) for r in rows]
    finally:
        db.close()


@app.get("/api/items/{item_id}", response_model=UserOut)
def get_user(item_id: int):
    db = SessionLocal()
    try:
        r = db.query(SecUser).filter(SecUser.id == item_id).first()
        if not r:
            raise HTTPException(status_code=404, detail="User not found")
        return UserOut(id=r.id, username=r.username, email=r.email, phone_number=r.phone_number, user_type=r.user_type)
    finally:
        db.close()


@app.post("/api/items", response_model=UserOut)
def create_user(payload: UserIn):
    db = SessionLocal()
    try:
        # naive password storage for demo only
        user = SecUser(username=payload.username, email=payload.email, phone_number=payload.phone_number,
                       password_hash=payload.password, user_type=payload.user_type, status="ACTIVE")
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserOut(id=user.id, username=user.username, email=user.email, phone_number=user.phone_number, user_type=user.user_type)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


@app.put("/api/items/{item_id}", response_model=UserOut)
def update_user(item_id: int, payload: UserIn):
    db = SessionLocal()
    try:
        user = db.query(SecUser).filter(SecUser.id == item_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.username = payload.username
        user.email = payload.email
        user.phone_number = payload.phone_number
        user.password_hash = payload.password
        user.user_type = payload.user_type
        db.commit()
        db.refresh(user)
        return UserOut(id=user.id, username=user.username, email=user.email, phone_number=user.phone_number, user_type=user.user_type)
    finally:
        db.close()
