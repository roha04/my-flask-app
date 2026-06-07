from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.enums import JobStatus
from app.models.user import User
from app.schemas.job import JobCreate, JobRead, JobUpdate
from app.services import job as job_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[JobRead])
def list_jobs(
    company_id: int | None = None,
    status: JobStatus | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> list:
    return job_service.list_jobs(
        db, company_id=company_id, status=status, skip=skip, limit=limit
    )


@router.post("", response_model=JobRead, status_code=201)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> object:
    return job_service.create_job(db, payload)


@router.get("/{job_id}", response_model=JobRead)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> object:
    return job_service.get_job(db, job_id)


@router.patch("/{job_id}", response_model=JobRead)
def update_job(
    job_id: int,
    payload: JobUpdate,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> object:
    return job_service.update_job(db, job_id, payload)


@router.delete("/{job_id}", status_code=204)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> None:
    job_service.delete_job(db, job_id)
