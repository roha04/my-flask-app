from sqlalchemy.orm import Session

from app.models.enums import JobStatus
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate
from app.services.company import get_company
from app.services.exceptions import NotFoundError, ValidationError


def list_jobs(
    db: Session,
    company_id: int | None = None,
    status: JobStatus | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Job]:
    query = db.query(Job)
    if company_id is not None:
        query = query.filter(Job.company_id == company_id)
    if status is not None:
        query = query.filter(Job.status == status)
    return query.order_by(Job.created_at.desc()).offset(skip).limit(limit).all()


def get_job(db: Session, job_id: int) -> Job:
    job = db.query(Job).filter(Job.id == job_id).one_or_none()
    if job is None:
        raise NotFoundError("Job not found")
    return job


def _validate_salary(job_data: dict) -> None:
    salary_min = job_data.get("salary_min")
    salary_max = job_data.get("salary_max")
    if salary_min is not None and salary_max is not None and salary_min > salary_max:
        raise ValidationError("salary_min cannot be greater than salary_max")


def create_job(db: Session, payload: JobCreate) -> Job:
    get_company(db, payload.company_id)
    data = payload.model_dump()
    if data.get("url") is not None:
        data["url"] = str(data["url"])
    _validate_salary(data)
    job = Job(**data)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_job(db: Session, job_id: int, payload: JobUpdate) -> Job:
    job = get_job(db, job_id)
    data = payload.model_dump(exclude_unset=True)
    if "company_id" in data and data["company_id"] is not None:
        get_company(db, data["company_id"])
    if "url" in data and data["url"] is not None:
        data["url"] = str(data["url"])
    merged = {
        "salary_min": data.get("salary_min", job.salary_min),
        "salary_max": data.get("salary_max", job.salary_max),
    }
    _validate_salary(merged)
    for field, value in data.items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job


def delete_job(db: Session, job_id: int) -> None:
    job = get_job(db, job_id)
    db.delete(job)
    db.commit()
