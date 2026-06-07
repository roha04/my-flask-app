from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import SESSION_USER_KEY, get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin, UserRead, UserRegister
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> User:
    return auth_service.register_user(db, payload)


@router.post("/login", response_model=UserRead)
def login(
    payload: UserLogin,
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    user = auth_service.authenticate_user(db, payload)
    request.session[SESSION_USER_KEY] = user.id
    return user


@router.post("/logout", status_code=204)
def logout(request: Request) -> None:
    request.session.clear()


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
