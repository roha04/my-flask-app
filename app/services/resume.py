from sqlalchemy.orm import Session

from app.models.resume_version import ResumeVersion
from app.schemas.resume import ResumeCreate, ResumeUpdate
from app.services.exceptions import NotFoundError


def list_resumes(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[ResumeVersion]:
    return (
        db.query(ResumeVersion)
        .filter(ResumeVersion.user_id == user_id)
        .order_by(ResumeVersion.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_resume(db: Session, resume_id: int, user_id: int | None = None) -> ResumeVersion:
    query = db.query(ResumeVersion).filter(ResumeVersion.id == resume_id)
    if user_id is not None:
        query = query.filter(ResumeVersion.user_id == user_id)
    resume = query.one_or_none()
    if resume is None:
        raise NotFoundError("Resume not found")
    return resume


def create_resume(db: Session, user_id: int, payload: ResumeCreate) -> ResumeVersion:
    if payload.is_active:
        _deactivate_user_resumes(db, user_id)
    resume = ResumeVersion(user_id=user_id, **payload.model_dump())
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def update_resume(
    db: Session, resume_id: int, user_id: int, payload: ResumeUpdate
) -> ResumeVersion:
    resume = get_resume(db, resume_id, user_id=user_id)
    data = payload.model_dump(exclude_unset=True)
    if data.get("is_active"):
        _deactivate_user_resumes(db, user_id, exclude_id=resume_id)
    for field, value in data.items():
        setattr(resume, field, value)
    db.commit()
    db.refresh(resume)
    return resume


def activate_resume(db: Session, resume_id: int, user_id: int) -> ResumeVersion:
    resume = get_resume(db, resume_id, user_id=user_id)
    _deactivate_user_resumes(db, user_id, exclude_id=resume_id)
    resume.is_active = True
    db.commit()
    db.refresh(resume)
    return resume


def delete_resume(db: Session, resume_id: int, user_id: int) -> None:
    resume = get_resume(db, resume_id, user_id=user_id)
    db.delete(resume)
    db.commit()


def _deactivate_user_resumes(db: Session, user_id: int, exclude_id: int | None = None) -> None:
    query = db.query(ResumeVersion).filter(
        ResumeVersion.user_id == user_id,
        ResumeVersion.is_active,
    )
    if exclude_id is not None:
        query = query.filter(ResumeVersion.id != exclude_id)
    for resume in query.all():
        resume.is_active = False
