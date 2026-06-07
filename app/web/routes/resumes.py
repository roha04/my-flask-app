from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.resume import ResumeCreate, ResumeUpdate
from app.services import resume as resume_service
from app.web.deps import login_required, templates

router = APIRouter(prefix="/resumes", tags=["web-resumes"])


def _ctx(request: Request, user, **kwargs):
    return {
        "request": request,
        "user": user,
        "message": request.query_params.get("message"),
        "error": request.query_params.get("error"),
        **kwargs,
    }


@router.get("")
def resumes_list(request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    resumes = resume_service.list_resumes(db, auth.id)
    return templates.TemplateResponse("resumes/list.html", _ctx(request, auth, resumes=resumes))


@router.get("/new")
def resume_new_page(request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    return templates.TemplateResponse(
        "resumes/form.html", _ctx(request, auth, title="New resume", resume=None)
    )


@router.post("/new")
def resume_create(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    is_active: str = Form(""),
    db: Session = Depends(get_db),
):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    resume_service.create_resume(
        db,
        auth.id,
        ResumeCreate(title=title, content=content, is_active=bool(is_active)),
    )
    return RedirectResponse("/resumes?message=Resume+created", status_code=303)


@router.get("/{resume_id}/edit")
def resume_edit_page(resume_id: int, request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    resume = resume_service.get_resume(db, resume_id, user_id=auth.id)
    return templates.TemplateResponse(
        "resumes/form.html", _ctx(request, auth, title="Edit resume", resume=resume)
    )


@router.post("/{resume_id}/edit")
def resume_update(
    resume_id: int,
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    is_active: str = Form(""),
    db: Session = Depends(get_db),
):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    resume_service.update_resume(
        db,
        resume_id,
        auth.id,
        ResumeUpdate(title=title, content=content, is_active=bool(is_active)),
    )
    return RedirectResponse("/resumes?message=Resume+updated", status_code=303)


@router.post("/{resume_id}/activate")
def resume_activate(resume_id: int, request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    resume_service.activate_resume(db, resume_id, auth.id)
    return RedirectResponse("/resumes?message=Resume+activated", status_code=303)


@router.post("/{resume_id}/delete")
def resume_delete(resume_id: int, request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    resume_service.delete_resume(db, resume_id, auth.id)
    return RedirectResponse("/resumes?message=Resume+deleted", status_code=303)
