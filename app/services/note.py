from sqlalchemy.orm import Session

from app.models.enums import NoteEntityType
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate
from app.services.application import get_application
from app.services.company import get_company
from app.services.exceptions import NotFoundError, ValidationError
from app.services.job import get_job


def list_notes(
    db: Session,
    entity_type: NoteEntityType | None = None,
    company_id: int | None = None,
    job_id: int | None = None,
    application_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Note]:
    query = db.query(Note)
    if entity_type is not None:
        query = query.filter(Note.entity_type == entity_type)
    if company_id is not None:
        query = query.filter(Note.company_id == company_id)
    if job_id is not None:
        query = query.filter(Note.job_id == job_id)
    if application_id is not None:
        query = query.filter(Note.application_id == application_id)
    return query.order_by(Note.created_at.desc()).offset(skip).limit(limit).all()


def get_note(db: Session, note_id: int) -> Note:
    note = db.query(Note).filter(Note.id == note_id).one_or_none()
    if note is None:
        raise NotFoundError("Note not found")
    return note


def _validate_note_targets(db: Session, payload: NoteCreate) -> None:
    if payload.entity_type == NoteEntityType.COMPANY:
        if payload.company_id is None:
            raise ValidationError("company_id is required")
        get_company(db, payload.company_id)
    elif payload.entity_type == NoteEntityType.JOB:
        if payload.job_id is None:
            raise ValidationError("job_id is required")
        get_job(db, payload.job_id)
    elif payload.entity_type == NoteEntityType.APPLICATION:
        if payload.application_id is None:
            raise ValidationError("application_id is required")
        get_application(db, payload.application_id)


def create_note(db: Session, payload: NoteCreate) -> Note:
    _validate_note_targets(db, payload)
    note = Note(**payload.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note_id: int, payload: NoteUpdate) -> Note:
    note = get_note(db, note_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int) -> None:
    note = get_note(db, note_id)
    db.delete(note)
    db.commit()
