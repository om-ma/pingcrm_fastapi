from sqlalchemy import Column, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.base import TimestampMixin

class Contact(Base, TimestampMixin):
    __tablename__ = "contacts"

    id = Column(BigInteger, primary_key=True)
    account_id = Column(BigInteger, ForeignKey("accounts.id"), nullable=False)
    organization_id = Column(BigInteger, ForeignKey("organizations.id"))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    region = Column(String)
    country = Column(String)
    postal_code = Column(String)
    deleted_at = Column(DateTime)

    account = relationship("Account", back_populates="contacts")
    organization = relationship("Organization", back_populates="contacts")
