from pathlib import Path

from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.deps import SESSION_USER_KEY
from app.models.user import User
from app.services.auth import require_user
from app.services.exceptions import NotFoundError

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def get_web_user(request: Request, db: Session) -> User | None:
    user_id = request.session.get(SESSION_USER_KEY)
    if user_id is None:
        return None
    try:
        return require_user(db, user_id)
    except NotFoundError:
        request.session.clear()
        return None


def login_required(request: Request, db: Session) -> User | RedirectResponse:
    user = get_web_user(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    return user
