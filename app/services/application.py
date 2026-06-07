from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.enums import ApplicationStage
from app.models.stage_history import ApplicationStageHistory
from app.schemas.application import ApplicationCreate, ApplicationStageChange, ApplicationUpdate
from app.services.exceptions import NotFoundError, ValidationError
from app.services.job import get_job
from app.services.resume import get_resume
from app.services.scoring import refresh_application_scores


def list_applications(
    db: Session,
    user_id: int,
    stage: ApplicationStage | None = None,
    job_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Application]:
    query = db.query(Application).filter(Application.user_id == user_id)
    if stage is not None:
        query = query.filter(Application.stage == stage)
    if job_id is not None:
        query = query.filter(Application.job_id == job_id)
    return query.order_by(Application.updated_at.desc()).offset(skip).limit(limit).all()


def get_application(db: Session, application_id: int, user_id: int | None = None) -> Application:
    query = db.query(Application).filter(Application.id == application_id)
    if user_id is not None:
        query = query.filter(Application.user_id == user_id)
    application = query.one_or_none()
    if application is None:
        raise NotFoundError("Application not found")
    return application


def list_stage_history(
    db: Session, application_id: int, user_id: int
) -> list[ApplicationStageHistory]:
    application = get_application(db, application_id, user_id=user_id)
    return list(application.stage_history)


def _validate_resume(db: Session, user_id: int, resume_version_id: int | None) -> None:
    if resume_version_id is not None:
        get_resume(db, resume_version_id, user_id=user_id)


def create_application(db: Session, user_id: int, payload: ApplicationCreate) -> Application:
    get_job(db, payload.job_id)
    _validate_resume(db, user_id, payload.resume_version_id)
    data = payload.model_dump()
    if data["stage"] == ApplicationStage.APPLIED and data.get("applied_at") is None:
        data["applied_at"] = datetime.now(timezone.utc)
    application = Application(user_id=user_id, **data)
    db.add(application)
    db.flush()
    _record_stage_change(db, application, None, application.stage)
    refresh_application_scores(db, application)
    db.commit()
    db.refresh(application)
    return application


def update_application(
    db: Session, application_id: int, user_id: int, payload: ApplicationUpdate
) -> Application:
    application = get_application(db, application_id, user_id=user_id)
    data = payload.model_dump(exclude_unset=True)
    if "job_id" in data and data["job_id"] is not None:
        get_job(db, data["job_id"])
    if "resume_version_id" in data:
        _validate_resume(db, user_id, data["resume_version_id"])
    if "stage" in data and data["stage"] is not None and data["stage"] != application.stage:
        raise ValidationError("Use change_stage to update application stage")
    score_fields = {"match_score", "priority_score", "response_likelihood"}
    for field, value in data.items():
        if field not in score_fields:
            setattr(application, field, value)
    refresh_application_scores(db, application)
    db.commit()
    db.refresh(application)
    return application


def change_stage(
    db: Session, application_id: int, user_id: int, payload: ApplicationStageChange
) -> Application:
    application = get_application(db, application_id, user_id=user_id)
    if payload.stage == application.stage:
        return application
    previous = application.stage
    application.stage = payload.stage
    if payload.stage == ApplicationStage.APPLIED and application.applied_at is None:
        application.applied_at = datetime.now(timezone.utc)
    _record_stage_change(db, application, previous, payload.stage)
    refresh_application_scores(db, application)
    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, application_id: int, user_id: int) -> None:
    application = get_application(db, application_id, user_id=user_id)
    db.delete(application)
    db.commit()


def _record_stage_change(
    db: Session,
    application: Application,
    from_stage: ApplicationStage | None,
    to_stage: ApplicationStage,
) -> None:
    history = ApplicationStageHistory(
        application_id=application.id,
        from_stage=from_stage,
        to_stage=to_stage,
    )
    db.add(history)
