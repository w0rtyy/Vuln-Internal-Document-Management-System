from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)  # user | manager | admin


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    file_path = Column(String)
    is_approved = Column(Boolean, default=False)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime(timezone=True))

