from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.enums import NoteEntityType
from app.models.user import User
from app.schemas.note import NoteCreate, NoteRead, NoteUpdate
from app.services import note as note_service

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteRead])
def list_notes(
    entity_type: NoteEntityType | None = None,
    company_id: int | None = None,
    job_id: int | None = None,
    application_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> list:
    return note_service.list_notes(
        db,
        entity_type=entity_type,
        company_id=company_id,
        job_id=job_id,
        application_id=application_id,
        skip=skip,
        limit=limit,
    )


@router.post("", response_model=NoteRead, status_code=201)
def create_note(
    payload: NoteCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> object:
    return note_service.create_note(db, payload)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> object:
    return note_service.get_note(db, note_id)


@router.patch("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int,
    payload: NoteUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> object:
    return note_service.update_note(db, note_id, payload)


@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> None:
    note_service.delete_note(db, note_id)
