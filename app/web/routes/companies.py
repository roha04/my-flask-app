from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.company import CompanyCreate, CompanyUpdate
from app.services import company as company_service
from app.web.deps import login_required, templates

router = APIRouter(prefix="/companies", tags=["web-companies"])


def _ctx(request: Request, user, **kwargs):
    return {
        "request": request,
        "user": user,
        "message": request.query_params.get("message"),
        "error": request.query_params.get("error"),
        **kwargs,
    }


@router.get("")
def companies_list(request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    companies = company_service.list_companies(db)
    return templates.TemplateResponse(
        "companies/list.html", _ctx(request, auth, companies=companies)
    )


@router.get("/new")
def company_new_page(request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    return templates.TemplateResponse(
        "companies/form.html", _ctx(request, auth, title="New company", company=None)
    )


@router.post("/new")
def company_create(
    request: Request,
    name: str = Form(...),
    industry: str = Form(""),
    size: str = Form(""),
    website: str = Form(""),
    db: Session = Depends(get_db),
):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    company_service.create_company(
        db,
        CompanyCreate(
            name=name,
            industry=industry or None,
            size=size or None,
            website=website or None,
        ),
    )
    return RedirectResponse("/companies?message=Company+created", status_code=303)


@router.get("/{company_id}/edit")
def company_edit_page(company_id: int, request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    company = company_service.get_company(db, company_id)
    return templates.TemplateResponse(
        "companies/form.html", _ctx(request, auth, title="Edit company", company=company)
    )


@router.post("/{company_id}/edit")
def company_update(
    company_id: int,
    request: Request,
    name: str = Form(...),
    industry: str = Form(""),
    size: str = Form(""),
    website: str = Form(""),
    db: Session = Depends(get_db),
):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    company_service.update_company(
        db,
        company_id,
        CompanyUpdate(
            name=name,
            industry=industry or None,
            size=size or None,
            website=website or None,
        ),
    )
    return RedirectResponse("/companies?message=Company+updated", status_code=303)


@router.post("/{company_id}/delete")
def company_delete(company_id: int, request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    company_service.delete_company(db, company_id)
    return RedirectResponse("/companies?message=Company+deleted", status_code=303)
