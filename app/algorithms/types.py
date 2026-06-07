from dataclasses import dataclass
from datetime import datetime

from app.models.enums import ApplicationStage


@dataclass(frozen=True)
class ApplicationActivity:
    id: int
    stage: ApplicationStage
    applied_at: datetime | None
    last_stage_change_at: datetime | None
    last_note_at: datetime | None


@dataclass(frozen=True)
class StageTransition:
    from_stage: ApplicationStage | None
    to_stage: ApplicationStage
    changed_at: datetime


@dataclass(frozen=True)
class JobSalary:
    salary_min: int | None
    salary_max: int | None
