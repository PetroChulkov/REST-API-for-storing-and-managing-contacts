from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactBase, ContactResponse, ContactUpdate
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.database.models import User

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse], name='All contacts')
async def show_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.show_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/search/{credentials}", response_model=List[ContactResponse], name='Contacts by credentials')
async def search_contacts(credentials: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.search_contacts(credentials, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/birthday/", response_model=List[ContactResponse], name='Upcoming birthdays')
async def upcoming_birthday(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.upcoming_birthday(db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found")
    return contact