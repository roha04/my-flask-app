from datetime import datetime, timedelta, timezone

from app.algorithms.stale import detect_stale_applications
from app.algorithms.types import ApplicationActivity
from app.models.enums import ApplicationStage


def _activity(
    app_id: int,
    stage: ApplicationStage,
    days_ago: int,
) -> ApplicationActivity:
    timestamp = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return ApplicationActivity(
        id=app_id,
        stage=stage,
        applied_at=timestamp,
        last_stage_change_at=timestamp,
        last_note_at=None,
    )


def test_detects_stale_applied_application():
    applications = [_activity(1, ApplicationStage.APPLIED, days_ago=10)]
    assert detect_stale_applications(applications) == [1]


def test_recent_application_is_not_stale():
    applications = [_activity(2, ApplicationStage.APPLIED, days_ago=2)]
    assert detect_stale_applications(applications) == []


def test_respects_custom_sla():
    applications = [_activity(3, ApplicationStage.APPLIED, days_ago=4)]
    sla = {ApplicationStage.APPLIED: 3}
    assert detect_stale_applications(applications, sla_days_by_stage=sla) == [3]


def test_returns_multiple_stale_ids():
    applications = [
        _activity(4, ApplicationStage.APPLIED, days_ago=8),
        _activity(5, ApplicationStage.TECHNICAL, days_ago=2),
        _activity(6, ApplicationStage.PHONE_SCREEN, days_ago=10),
    ]
    stale = detect_stale_applications(applications)
    assert 4 in stale
    assert 6 in stale
    assert 5 not in stale
