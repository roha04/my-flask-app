from sqlalchemy import func
from sqlalchemy.orm import Session

from app.algorithms.actions import suggest_next_action
from app.algorithms.match import match_resume_to_jd
from app.algorithms.pipeline import pipeline_velocity
from app.algorithms.salary import salary_benchmark
from app.algorithms.stale import detect_stale_applications
from app.algorithms.types import ApplicationActivity, JobSalary, StageTransition
from app.models.application import Application
from app.models.job import Job
from app.models.note import Note
from app.models.stage_history import ApplicationStageHistory
from app.services.application import get_application, list_applications
from app.services.scoring import days_in_current_stage


def get_suggested_action(db: Session, application_id: int, user_id: int) -> dict:
    application = get_application(db, application_id, user_id=user_id)
    stage_days = days_in_current_stage(application)
    action = suggest_next_action(
        application.stage,
        stage_days,
        application.match_score or 0.0,
    )
    return {
        "action": action,
        "days_in_stage": stage_days,
        "match_score": application.match_score,
    }


def get_pipeline_analytics(db: Session, user_id: int) -> dict:
    history_rows = (
        db.query(ApplicationStageHistory)
        .join(Application, Application.id == ApplicationStageHistory.application_id)
        .filter(Application.user_id == user_id)
        .order_by(ApplicationStageHistory.changed_at)
        .all()
    )
    transitions = [
        StageTransition(row.from_stage, row.to_stage, row.changed_at) for row in history_rows
    ]
    return pipeline_velocity(transitions)


def _last_note_at(db: Session, application_id: int):
    return (
        db.query(func.max(Note.created_at))
        .filter(Note.application_id == application_id)
        .scalar()
    )


def get_stale_applications(db: Session, user_id: int) -> dict:
    applications = list_applications(db, user_id, limit=500)
    activities: list[ApplicationActivity] = []
    for application in applications:
        last_stage_change = (
            application.stage_history[-1].changed_at if application.stage_history else None
        )
        activities.append(
            ApplicationActivity(
                id=application.id,
                stage=application.stage,
                applied_at=application.applied_at,
                last_stage_change_at=last_stage_change,
                last_note_at=_last_note_at(db, application.id),
            )
        )
    stale_ids = detect_stale_applications(activities)
    return {"stale_application_ids": stale_ids, "count": len(stale_ids)}


def get_salary_benchmark_analytics(db: Session, salary: float) -> dict:
    jobs = db.query(Job).all()
    job_salaries = [
        JobSalary(salary_min=job.salary_min, salary_max=job.salary_max) for job in jobs
    ]
    result = salary_benchmark(salary, job_salaries)
    result["salary"] = salary
    return result


def compute_match(resume_text: str, jd_text: str) -> float:
    return match_resume_to_jd(resume_text, jd_text)
