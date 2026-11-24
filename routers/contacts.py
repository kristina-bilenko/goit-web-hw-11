from typing import List

from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session

from db import get_db
from schemas import ContactCreate, ContactUpdate, ContactPatch, ContactResponse
from repository import contacts as repository_contacts


router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactCreate, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts

@router.get("/birthdays", response_model=List[ContactResponse])
async def read_upcoming_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays(db)
    return contacts


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    search: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    contacts = await repository_contacts.search_contacts(search, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сontact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def put_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.put_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сontact not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def patch_contact(body: ContactPatch, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.patch_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сontact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сontact not found")
    return contact
