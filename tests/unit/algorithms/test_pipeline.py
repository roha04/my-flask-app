from datetime import datetime, timedelta, timezone

from app.algorithms.pipeline import pipeline_velocity
from app.algorithms.types import StageTransition
from app.models.enums import ApplicationStage


def _at(days: int) -> datetime:
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return base + timedelta(days=days)


def test_pipeline_velocity_average_days():
    history = [
        StageTransition(None, ApplicationStage.WISHLIST, _at(0)),
        StageTransition(ApplicationStage.WISHLIST, ApplicationStage.APPLIED, _at(5)),
        StageTransition(ApplicationStage.APPLIED, ApplicationStage.TECHNICAL, _at(8)),
    ]
    result = pipeline_velocity(history)
    assert result["avg_days_by_stage"]["Wishlist"] == 5.0
    assert result["avg_days_by_stage"]["Applied"] == 3.0
    assert result["transitions_count"] == 3


def test_bottleneck_is_slowest_stage():
    history = [
        StageTransition(None, ApplicationStage.WISHLIST, _at(0)),
        StageTransition(ApplicationStage.WISHLIST, ApplicationStage.APPLIED, _at(2)),
        StageTransition(ApplicationStage.APPLIED, ApplicationStage.TECHNICAL, _at(12)),
    ]
    result = pipeline_velocity(history)
    assert result["bottleneck_stage"] == "Applied"


def test_empty_history_returns_defaults():
    result = pipeline_velocity([])
    assert result["avg_days_by_stage"] == {}
    assert result["bottleneck_stage"] is None
    assert result["transitions_count"] == 0


def test_single_transition_has_no_averages():
    history = [StageTransition(None, ApplicationStage.WISHLIST, _at(0))]
    result = pipeline_velocity(history)
    assert result["avg_days_by_stage"] == {}
    assert result["transitions_count"] == 1
