from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import ApplicationStage
from app.schemas.common import ORMModel


class ApplicationBase(BaseModel):
    job_id: int
    resume_version_id: int | None = None
    stage: ApplicationStage = ApplicationStage.WISHLIST
    applied_at: datetime | None = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    job_id: int | None = None
    resume_version_id: int | None = None
    stage: ApplicationStage | None = None
    applied_at: datetime | None = None
    match_score: float | None = Field(default=None, ge=0, le=1)
    priority_score: float | None = None
    response_likelihood: float | None = Field(default=None, ge=0, le=1)


class ApplicationStageChange(BaseModel):
    stage: ApplicationStage


class ApplicationRead(ApplicationBase, ORMModel):
    id: int
    user_id: int
    match_score: float | None
    priority_score: float | None
    response_likelihood: float | None
    created_at: datetime
    updated_at: datetime


class StageHistoryRead(ORMModel):
    id: int
    application_id: int
    from_stage: ApplicationStage | None
    to_stage: ApplicationStage
    changed_at: datetime
