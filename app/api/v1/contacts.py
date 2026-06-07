from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactRead, ContactUpdate
from app.services import contact as contact_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("", response_model=list[ContactRead])
def list_contacts(
    company_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> list:
    return contact_service.list_contacts(db, company_id=company_id, skip=skip, limit=limit)


@router.post("", response_model=ContactRead, status_code=201)
def create_contact(
    payload: ContactCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> object:
    return contact_service.create_contact(db, payload)


@router.get("/{contact_id}", response_model=ContactRead)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> object:
    return contact_service.get_contact(db, contact_id)


@router.patch("/{contact_id}", response_model=ContactRead)
def update_contact(
    contact_id: int,
    payload: ContactUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> object:
    return contact_service.update_contact(db, contact_id, payload)


@router.delete("/{contact_id}", status_code=204)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> None:
    contact_service.delete_contact(db, contact_id)
