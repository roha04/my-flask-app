from datetime import datetime, timezone

from app.algorithms.types import ApplicationActivity
from app.models.enums import ApplicationStage

DEFAULT_SLA_DAYS: dict[ApplicationStage, int] = {
    ApplicationStage.WISHLIST: 14,
    ApplicationStage.APPLIED: 7,
    ApplicationStage.PHONE_SCREEN: 5,
    ApplicationStage.TECHNICAL: 5,
    ApplicationStage.ONSITE: 4,
    ApplicationStage.OFFER: 3,
    ApplicationStage.REJECTED: 30,
    ApplicationStage.WITHDRAWN: 30,
}


def _last_activity(application: ApplicationActivity) -> datetime | None:
    timestamps = [
        application.applied_at,
        application.last_stage_change_at,
        application.last_note_at,
    ]
    valid = [item for item in timestamps if item is not None]
    if not valid:
        return None
    return max(valid)


def detect_stale_applications(
    applications: list[ApplicationActivity],
    sla_days_by_stage: dict[ApplicationStage, int] | None = None,
    now: datetime | None = None,
) -> list[int]:
    """Return application IDs with no activity beyond the SLA for their stage."""
    sla = sla_days_by_stage or DEFAULT_SLA_DAYS
    current_time = now or datetime.now(timezone.utc)
    stale_ids: list[int] = []

    for application in applications:
        last_activity = _last_activity(application)
        if last_activity is None:
            continue
        if last_activity.tzinfo is None:
            last_activity = last_activity.replace(tzinfo=timezone.utc)
        days_idle = (current_time - last_activity).days
        threshold = sla.get(application.stage, 7)
        if days_idle > threshold:
            stale_ids.append(application.id)
    return stale_ids
