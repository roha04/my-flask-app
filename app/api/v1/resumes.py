from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.resume import ResumeCreate, ResumeRead, ResumeUpdate
from app.services import resume as resume_service

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.get("", response_model=list[ResumeRead])
def list_resumes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    return resume_service.list_resumes(db, current_user.id, skip=skip, limit=limit)


@router.post("", response_model=ResumeRead, status_code=201)
def create_resume(
    payload: ResumeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> object:
    return resume_service.create_resume(db, current_user.id, payload)


@router.get("/{resume_id}", response_model=ResumeRead)
def get_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> object:
    return resume_service.get_resume(db, resume_id, user_id=current_user.id)


@router.patch("/{resume_id}", response_model=ResumeRead)
def update_resume(
    resume_id: int,
    payload: ResumeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> object:
    return resume_service.update_resume(db, resume_id, current_user.id, payload)


@router.post("/{resume_id}/activate", response_model=ResumeRead)
def activate_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> object:
    return resume_service.activate_resume(db, resume_id, current_user.id)


@router.delete("/{resume_id}", status_code=204)
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    resume_service.delete_resume(db, resume_id, current_user.id)
