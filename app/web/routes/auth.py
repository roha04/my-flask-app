from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.deps import SESSION_USER_KEY
from app.database import get_db
from app.schemas.user import UserLogin, UserRegister
from app.services import auth as auth_service
from app.services.exceptions import ConflictError, UnauthorizedError
from app.web.deps import get_web_user, templates

router = APIRouter(tags=["web-auth"])


def _ctx(request: Request, **kwargs):
    return {
        "request": request,
        "user": kwargs.pop("user", None),
        "message": request.query_params.get("message"),
        "error": request.query_params.get("error"),
        **kwargs,
    }


@router.get("/login")
def login_page(request: Request, db: Session = Depends(get_db)):
    user = get_web_user(request, db)
    if user:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("auth/login.html", _ctx(request))


@router.post("/login")
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user = auth_service.authenticate_user(db, UserLogin(email=email, password=password))
    except UnauthorizedError:
        return RedirectResponse("/login?error=Invalid+email+or+password", status_code=303)
    request.session[SESSION_USER_KEY] = user.id
    return RedirectResponse("/", status_code=303)


@router.get("/register")
def register_page(request: Request, db: Session = Depends(get_db)):
    user = get_web_user(request, db)
    if user:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("auth/register.html", _ctx(request))


@router.post("/register")
def register_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user = auth_service.register_user(
            db, UserRegister(email=email, password=password, name=name)
        )
    except ConflictError:
        return RedirectResponse("/register?error=Email+already+registered", status_code=303)
    request.session[SESSION_USER_KEY] = user.id
    return RedirectResponse("/", status_code=303)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)
