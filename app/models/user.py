from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.base import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    account_id = Column(BigInteger, ForeignKey("accounts.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    owner = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime)
    encrypted_password = Column(String, nullable=False, default="")
    reset_password_token = Column(String, unique=True)
    reset_password_sent_at = Column(DateTime)
    remember_created_at = Column(DateTime)

    account = relationship("Account", back_populates="users")
