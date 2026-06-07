from app.models import Application, Company, Job, User
from app.models.enums import ApplicationStage, JobStatus, NoteEntityType


def test_create_core_models(db_session):
    user = User(email="dev@example.com", password_hash="hash", name="Dev User")
    db_session.add(user)
    db_session.flush()

    company = Company(name="Acme Corp", industry="Tech")
    db_session.add(company)
    db_session.flush()

    job = Job(
        company_id=company.id,
        title="Backend Engineer",
        description="Python FastAPI developer needed",
        salary_min=80000,
        salary_max=120000,
        status=JobStatus.OPEN,
    )
    db_session.add(job)
    db_session.flush()

    application = Application(
        user_id=user.id,
        job_id=job.id,
        stage=ApplicationStage.APPLIED,
    )
    db_session.add(application)
    db_session.commit()

    assert application.id is not None
    assert job.company.name == "Acme Corp"
    assert NoteEntityType.JOB.value == "job"
