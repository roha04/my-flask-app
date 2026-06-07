"""Seed demo data for staging/production demos."""

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.enums import ApplicationStage, JobStatus
from app.schemas.application import ApplicationCreate
from app.schemas.company import CompanyCreate
from app.schemas.job import JobCreate
from app.schemas.resume import ResumeCreate
from app.schemas.user import UserRegister
from app.services import application as application_service
from app.services import company as company_service
from app.services import job as job_service
from app.services import resume as resume_service
from app.services.auth import get_user_by_email, register_user

DEMO_EMAIL = "demo@jobcrm.dev"
DEMO_PASSWORD = "demo12345"


def seed(db: Session | None = None) -> None:
    close_session = db is None
    db = db or SessionLocal()
    try:
        if company_service.list_companies(db):
            print("Database already contains data; skipping seed.")
            return

        user = get_user_by_email(db, DEMO_EMAIL)
        if user is None:
            user = register_user(
                db,
                UserRegister(email=DEMO_EMAIL, password=DEMO_PASSWORD, name="Demo User"),
            )
            print(f"Created demo user: {DEMO_EMAIL}")

        acme = company_service.create_company(
            db,
            CompanyCreate(
                name="Acme Tech",
                industry="Software",
                size="200-500",
                website="https://acme.example",
            ),
        )
        company_service.create_company(
            db,
            CompanyCreate(name="DataFlow", industry="Analytics", size="50-200"),
        )

        backend_job = job_service.create_job(
            db,
            JobCreate(
                company_id=acme.id,
                title="Senior Python Engineer",
                description=(
                    "Build APIs with Python, FastAPI, PostgreSQL, Docker, and CI/CD pipelines. "
                    "Experience with SQLAlchemy and automated testing required."
                ),
                salary_min=90000,
                salary_max=130000,
                location="Remote",
                status=JobStatus.OPEN,
            ),
        )
        job_service.create_job(
            db,
            JobCreate(
                company_id=acme.id,
                title="Backend Developer",
                description="Python backend services, REST APIs, pytest, GitHub Actions.",
                salary_min=70000,
                salary_max=95000,
                location="Kyiv",
                status=JobStatus.OPEN,
            ),
        )

        resume = resume_service.create_resume(
            db,
            user.id,
            ResumeCreate(
                title="Backend CV",
                content=(
                    "Python developer with FastAPI, Flask, SQLAlchemy, PostgreSQL, Docker, "
                    "pytest, GitHub Actions, and REST API design."
                ),
                is_active=True,
            ),
        )

        application_service.create_application(
            db,
            user.id,
            ApplicationCreate(
                job_id=backend_job.id,
                resume_version_id=resume.id,
                stage=ApplicationStage.APPLIED,
            ),
        )
        print("Demo data seeded successfully.")
        print(f"Login: {DEMO_EMAIL} / {DEMO_PASSWORD}")
    finally:
        if close_session:
            db.close()


if __name__ == "__main__":
    seed()
