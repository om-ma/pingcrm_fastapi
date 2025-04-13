from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.base import TimestampMixin

class Account(Base, TimestampMixin):
    __tablename__ = "accounts"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="account")
    organizations = relationship("Organization", back_populates="account")
    contacts = relationship("Contact", back_populates="account")
