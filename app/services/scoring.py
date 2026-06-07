from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.algorithms.likelihood import DEFAULT_STAGE_RATES, predict_response_likelihood
from app.algorithms.match import match_resume_to_jd
from app.algorithms.priority import score_application_priority
from app.models.application import Application
from app.services.job import get_job
from app.services.resume import get_resume


def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def days_since(value: datetime | None) -> int:
    if value is None:
        return 0
    return max((_ensure_utc(datetime.now(timezone.utc)) - _ensure_utc(value)).days, 0)


def days_in_current_stage(application: Application) -> int:
    if application.stage_history:
        return days_since(application.stage_history[-1].changed_at)
    return days_since(application.created_at)


def refresh_application_scores(db: Session, application: Application) -> Application:
    """Compute match, priority, and response likelihood for an application."""
    job = get_job(db, application.job_id)
    resume_text = ""
    if application.resume_version_id is not None:
        resume = get_resume(db, application.resume_version_id, user_id=application.user_id)
        resume_text = resume.content

    match_score = match_resume_to_jd(resume_text, job.description) if resume_text.strip() else None
    priority_score = score_application_priority(
        match_score or 0.0,
        days_since(application.applied_at),
        application.stage,
    )
    response_likelihood = predict_response_likelihood(application.stage, DEFAULT_STAGE_RATES)

    application.match_score = match_score
    application.priority_score = priority_score
    application.response_likelihood = response_likelihood
    return application
