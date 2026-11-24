from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from datetime import date, timedelta
from models import Contact
from schemas import ContactCreate, ContactUpdate, ContactPatch


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.scalars(select(Contact).offset(skip).limit(limit)).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.scalar(select(Contact).where(Contact.id == contact_id))


async def get_upcoming_birthdays(db: Session) -> list[Contact]:
    today = date.today()
    next_week = today + timedelta(days=7)
    contacts = db.scalars(select(Contact)).all()
    upcoming_birthdays = []
    for contact in contacts:
        birthday = contact.date_of_birth
        try:
            birthday_this_year = birthday.replace(year=today.year)
        except ValueError:
            birthday_this_year = date(today.year, 2, 28)
        if birthday_this_year < today:
            try:
                birthday_this_year = birthday.replace(year=today.year + 1)
            except ValueError:
                birthday_this_year = date(today.year + 1, 2, 28)
        if today <= birthday_this_year <= next_week:
            upcoming_birthdays.append(contact)
    return upcoming_birthdays


async def create_contact(body: ContactCreate, db: Session) -> Contact:
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone_number=body.phone_number, date_of_birth=body.date_of_birth, additional_data=body.additional_data)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def put_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.scalar(select(Contact).where(Contact.id == contact_id))
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.date_of_birth = body.date_of_birth
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def patch_contact(contact_id: int, body: ContactPatch, db: Session) -> Contact | None:
    contact = db.scalar(select(Contact).where(Contact.id == contact_id))
    if contact:
        for key, value in body.model_dump(exclude_unset=True).items():
            setattr(contact, key, value)
            db.commit()
            db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.scalar(select(Contact).where(Contact.id == contact_id))
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def search_contacts(search: str, db: Session) -> list[Contact]:
    stmt = select(Contact).where(
        or_(
            Contact.name.ilike(search),
            Contact.surname.ilike(search),
            Contact.email.ilike(search)
        )
    )

    return db.scalars(stmt).all()