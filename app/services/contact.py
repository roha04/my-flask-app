from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate
from app.services.company import get_company
from app.services.exceptions import NotFoundError


def list_contacts(
    db: Session,
    company_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Contact]:
    query = db.query(Contact)
    if company_id is not None:
        query = query.filter(Contact.company_id == company_id)
    return query.order_by(Contact.name).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int) -> Contact:
    contact = db.query(Contact).filter(Contact.id == contact_id).one_or_none()
    if contact is None:
        raise NotFoundError("Contact not found")
    return contact


def create_contact(db: Session, payload: ContactCreate) -> Contact:
    get_company(db, payload.company_id)
    contact = Contact(**payload.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def update_contact(db: Session, contact_id: int, payload: ContactUpdate) -> Contact:
    contact = get_contact(db, contact_id)
    data = payload.model_dump(exclude_unset=True)
    if "company_id" in data and data["company_id"] is not None:
        get_company(db, data["company_id"])
    for field, value in data.items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact_id: int) -> None:
    contact = get_contact(db, contact_id)
    db.delete(contact)
    db.commit()
