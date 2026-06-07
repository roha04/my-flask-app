from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.algorithms.keywords import extract_keywords
from app.database import get_db
from app.models.enums import JobStatus
from app.schemas.job import JobCreate, JobUpdate
from app.services import company as company_service
from app.services import job as job_service
from app.web.deps import login_required, templates

router = APIRouter(prefix="/jobs", tags=["web-jobs"])


def _ctx(request: Request, user, **kwargs):
    return {
        "request": request,
        "user": user,
        "message": request.query_params.get("message"),
        "error": request.query_params.get("error"),
        **kwargs,
    }


@router.get("")
def jobs_list(request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    jobs = job_service.list_jobs(db)
    return templates.TemplateResponse("jobs/list.html", _ctx(request, auth, jobs=jobs))


@router.get("/new")
def job_new_page(request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    companies = company_service.list_companies(db)
    if not companies:
        return RedirectResponse("/companies/new?error=Create+a+company+first", status_code=303)
    return templates.TemplateResponse(
        "jobs/form.html",
        _ctx(
            request,
            auth,
            title="New job",
            job=None,
            companies=companies,
            job_statuses=list(JobStatus),
        ),
    )


@router.post("/new")
def job_create(
    request: Request,
    company_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(""),
    salary_min: str = Form(""),
    salary_max: str = Form(""),
    currency: str = Form("USD"),
    location: str = Form(""),
    url: str = Form(""),
    status: str = Form(JobStatus.OPEN.value),
    db: Session = Depends(get_db),
):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    job_service.create_job(
        db,
        JobCreate(
            company_id=company_id,
            title=title,
            description=description,
            salary_min=int(salary_min) if salary_min else None,
            salary_max=int(salary_max) if salary_max else None,
            currency=currency,
            location=location or None,
            url=url or None,
            status=JobStatus(status),
        ),
    )
    return RedirectResponse("/jobs?message=Job+created", status_code=303)


@router.get("/{job_id}")
def job_detail(job_id: int, request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    job = job_service.get_job(db, job_id)
    keywords = extract_keywords(job.description, top_n=10)
    return templates.TemplateResponse(
        "jobs/detail.html", _ctx(request, auth, job=job, keywords=keywords)
    )


@router.get("/{job_id}/edit")
def job_edit_page(job_id: int, request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    job = job_service.get_job(db, job_id)
    companies = company_service.list_companies(db)
    return templates.TemplateResponse(
        "jobs/form.html",
        _ctx(
            request,
            auth,
            title="Edit job",
            job=job,
            companies=companies,
            job_statuses=list(JobStatus),
        ),
    )


@router.post("/{job_id}/edit")
def job_update(
    job_id: int,
    request: Request,
    company_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(""),
    salary_min: str = Form(""),
    salary_max: str = Form(""),
    currency: str = Form("USD"),
    location: str = Form(""),
    url: str = Form(""),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    job_service.update_job(
        db,
        job_id,
        JobUpdate(
            company_id=company_id,
            title=title,
            description=description,
            salary_min=int(salary_min) if salary_min else None,
            salary_max=int(salary_max) if salary_max else None,
            currency=currency,
            location=location or None,
            url=url or None,
            status=JobStatus(status),
        ),
    )
    return RedirectResponse(f"/jobs/{job_id}?message=Job+updated", status_code=303)
