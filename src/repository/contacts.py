from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactBase, ContactResponse, ContactUpdate


async def show_notes(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactBase, db: Session) -> Contact:
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone, born_date=body.born_date)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.born_date = body.born_date
        db.commit()
    return contact

async def search_contacts(credentials: str, db: Session) -> Contact:
    request = "%{}%".format(credentials)
    if db.query(Contact).filter(Contact.name.like(request)).all():
        result = db.query(Contact).filter(Contact.name.like(request)).all()
        return result
    if db.query(Contact).filter(Contact.surname.like(request)).all():
        result = db.query(Contact).filter(Contact.surname.like(request)).all()
        return result
    if db.query(Contact).filter(Contact.email.like(request)).all():
        result = db.query(Contact).filter(Contact.email.like(request)).all()
        return result

async def upcoming_birthday(db: Session):
    contacts = db.query(Contact).all()
    result = []
    today = datetime.now()

    for contact in contacts:
        day = today.day
        month = today.month
        year = contact.born_date.year
        try:
            first_day = datetime(year=year, month=month, day=day)
        except:
            first_day = datetime(year=year, month=3, day=1)
        last_day = today + timedelta(days=7)
        if first_day <= contact.born_date <= last_day:
            result.append(contact)

    return result

