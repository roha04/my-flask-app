from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enums import ApplicationStage, NoteEntityType
from app.schemas.application import ApplicationCreate, ApplicationStageChange
from app.schemas.note import NoteCreate
from app.services import analytics as analytics_service
from app.services import application as application_service
from app.services import job as job_service
from app.services import note as note_service
from app.services import resume as resume_service
from app.web.deps import login_required, templates

router = APIRouter(prefix="/applications", tags=["web-applications"])

KANBAN_STAGES = [
    ApplicationStage.WISHLIST,
    ApplicationStage.APPLIED,
    ApplicationStage.PHONE_SCREEN,
    ApplicationStage.TECHNICAL,
    ApplicationStage.ONSITE,
    ApplicationStage.OFFER,
    ApplicationStage.REJECTED,
    ApplicationStage.WITHDRAWN,
]


def _ctx(request: Request, user, **kwargs):
    return {
        "request": request,
        "user": user,
        "message": request.query_params.get("message"),
        "error": request.query_params.get("error"),
        **kwargs,
    }


@router.get("")
def applications_kanban(request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    applications = application_service.list_applications(db, auth.id, limit=500)
    columns = {stage: [] for stage in KANBAN_STAGES}
    for app in applications:
        columns[app.stage].append(app)
    return templates.TemplateResponse(
        "applications/kanban.html",
        _ctx(request, auth, stages=KANBAN_STAGES, columns=columns),
    )


@router.get("/new")
def application_new_page(
    request: Request,
    job_id: int | None = None,
    db: Session = Depends(get_db),
):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    jobs = job_service.list_jobs(db)
    if not jobs:
        return RedirectResponse("/jobs/new?error=Create+a+job+first", status_code=303)
    resumes = resume_service.list_resumes(db, auth.id)
    selected_job_id = job_id or jobs[0].id
    return templates.TemplateResponse(
        "applications/form.html",
        _ctx(
            request,
            auth,
            jobs=jobs,
            resumes=resumes,
            stages=KANBAN_STAGES,
            selected_job_id=selected_job_id,
        ),
    )


@router.post("/new")
def application_create(
    request: Request,
    job_id: int = Form(...),
    resume_version_id: str = Form(""),
    stage: str = Form(ApplicationStage.WISHLIST.value),
    db: Session = Depends(get_db),
):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    application = application_service.create_application(
        db,
        auth.id,
        ApplicationCreate(
            job_id=job_id,
            resume_version_id=int(resume_version_id) if resume_version_id else None,
            stage=ApplicationStage(stage),
        ),
    )
    return RedirectResponse(f"/applications/{application.id}", status_code=303)


@router.get("/{application_id}")
def application_detail(application_id: int, request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    application = application_service.get_application(db, application_id, user_id=auth.id)
    history = application_service.list_stage_history(db, application_id, auth.id)
    notes = note_service.list_notes(db, application_id=application_id)
    suggestion = analytics_service.get_suggested_action(db, application_id, auth.id)
    return templates.TemplateResponse(
        "applications/detail.html",
        _ctx(
            request,
            auth,
            application=application,
            history=history,
            notes=notes,
            suggestion=suggestion,
            stages=KANBAN_STAGES,
        ),
    )


@router.post("/{application_id}/stage")
def application_change_stage(
    application_id: int,
    request: Request,
    stage: str = Form(...),
    db: Session = Depends(get_db),
):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    application_service.change_stage(
        db,
        application_id,
        auth.id,
        ApplicationStageChange(stage=ApplicationStage(stage)),
    )
    referer = request.headers.get("referer", "/applications")
    return RedirectResponse(referer, status_code=303)


@router.post("/{application_id}/notes")
def application_add_note(
    application_id: int,
    request: Request,
    body: str = Form(...),
    db: Session = Depends(get_db),
):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    application_service.get_application(db, application_id, user_id=auth.id)
    note_service.create_note(
        db,
        NoteCreate(
            entity_type=NoteEntityType.APPLICATION,
            application_id=application_id,
            body=body,
        ),
    )
    return RedirectResponse(f"/applications/{application_id}?message=Note+added", status_code=303)
