from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.schemas.base import TimestampSchema

# Account Schemas
class AccountBase(BaseModel):
    name: str

class AccountCreate(AccountBase):
    pass

class Account(AccountBase, TimestampSchema):
    id: int

    class Config:
        from_attributes = True

# User Schemas
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    owner: bool = False

class UserCreate(UserBase):
    password: str
    account_id: int

class User(UserBase, TimestampSchema):
    id: int
    account_id: int
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Organization Schemas
class OrganizationBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    account_id: int

class Organization(OrganizationBase, TimestampSchema):
    id: int
    account_id: int
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Contact Schemas
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    organization_id: Optional[int] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase, TimestampSchema):
    id: int
    account_id: int

    class Config:
        from_attributes = True
