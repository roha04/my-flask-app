from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.enums import ApplicationStage
from app.models.user import User
from app.schemas.analytics import SuggestActionResponse
from app.schemas.application import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationStageChange,
    ApplicationUpdate,
    StageHistoryRead,
)
from app.services import analytics as analytics_service
from app.services import application as application_service

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("", response_model=list[ApplicationRead])
def list_applications(
    stage: ApplicationStage | None = None,
    job_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    return application_service.list_applications(
        db,
        current_user.id,
        stage=stage,
        job_id=job_id,
        skip=skip,
        limit=limit,
    )


@router.post("", response_model=ApplicationRead, status_code=201)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> object:
    return application_service.create_application(db, current_user.id, payload)


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> object:
    return application_service.get_application(db, application_id, user_id=current_user.id)


@router.get("/{application_id}/history", response_model=list[StageHistoryRead])
def get_application_history(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    return application_service.list_stage_history(db, application_id, current_user.id)


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> object:
    return application_service.update_application(
        db, application_id, current_user.id, payload
    )


@router.patch("/{application_id}/stage", response_model=ApplicationRead)
def change_application_stage(
    application_id: int,
    payload: ApplicationStageChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> object:
    return application_service.change_stage(db, application_id, current_user.id, payload)


@router.delete("/{application_id}", status_code=204)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    application_service.delete_application(db, application_id, current_user.id)


@router.get("/{application_id}/suggest-action", response_model=SuggestActionResponse)
def suggest_application_action(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    return analytics_service.get_suggested_action(db, application_id, current_user.id)
