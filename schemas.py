from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr


class ContactBase(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone_number: str
    date_of_birth: date
    additional_data: Optional[str] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass

class ContactPatch(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    additional_data: Optional[str] = None

class ContactResponse(ContactBase):
    id: int