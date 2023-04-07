from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class ContactBase(BaseModel):
    name: str = Field(max_length=50, default='Default')
    surname: str = Field(max_length=50, default='Contact')
    email: EmailStr
    phone: str = Field(max_length=50, default='+421000000000')
    born_date: datetime


class ContactResponse(ContactBase):
    name: str
    surname: str
    email: EmailStr
    phone: str
    born_date: datetime

    class Config:
        orm_mode = True


class ContactUpdate(ContactBase):
    done: bool