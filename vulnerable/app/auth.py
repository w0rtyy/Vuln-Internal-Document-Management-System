from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import secrets

from vulnerable.app.database import get_db
from vulnerable.app import models, schema

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str):
    return pwd_context.hash(p)

def verify_password(p: str, h: str):
    return pwd_context.verify(p, h)

def create_session_id():
    return secrets.token_hex(32)

def get_current_user(
    session_id: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    if not session_id:
        raise HTTPException(status_code=401)

    session = db.query(models.Session).filter(
        models.Session.session_id == session_id,
        models.Session.expires_at > datetime.now(timezone.utc)
    ).first()

    if not session:
        raise HTTPException(status_code=401)

    user = db.query(models.User).get(session.user_id)
    if not user:
        raise HTTPException(status_code=401)

    return user


@router.post("/register", response_model=schema.UserResponse)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    u = models.User(
        email=user.email,
        password_hash=hash_password(user.password),
        role="user"
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@router.post("/login")
def login(user: schema.UserLogin, response: Response, db: Session = Depends(get_db)):
    u = db.query(models.User).filter(models.User.email == user.email).first()
    if not u or not verify_password(user.password, u.password_hash):
        raise HTTPException(status_code=401)

    sid = create_session_id()
    session = models.Session(
        session_id=sid,
        user_id=u.id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=2)
    )
    db.add(session)
    db.commit()

    response.set_cookie("session_id", sid, httponly=True)
    return {"message": "logged in"}


@router.get("/me", response_model=schema.UserResponse)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user
