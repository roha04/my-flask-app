from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth import require_user
from app.services.exceptions import UnauthorizedError

SESSION_USER_KEY = "user_id"


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> User | None:
    user_id = request.session.get(SESSION_USER_KEY)
    if user_id is None:
        return None
    return require_user(db, user_id)


def get_current_user(user: User | None = Depends(get_optional_user)) -> User:
    if user is None:
        raise UnauthorizedError("Not authenticated")
    return user
