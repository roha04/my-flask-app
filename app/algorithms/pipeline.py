from collections import defaultdict
from datetime import datetime, timezone

from app.algorithms.types import StageTransition
from app.models.enums import ApplicationStage


def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def pipeline_velocity(stage_history: list[StageTransition]) -> dict:
    """Compute average days spent in each stage and identify bottlenecks."""
    if not stage_history:
        return {
            "avg_days_by_stage": {},
            "bottleneck_stage": None,
            "transitions_count": 0,
        }

    ordered = sorted(stage_history, key=lambda item: item.changed_at)
    durations: dict[ApplicationStage, list[float]] = defaultdict(list)

    for index in range(1, len(ordered)):
        previous = ordered[index - 1]
        current = ordered[index]
        if current.from_stage is None:
            continue
        start = _ensure_utc(previous.changed_at)
        end = _ensure_utc(current.changed_at)
        days = max((end - start).total_seconds() / 86400.0, 0.0)
        durations[current.from_stage].append(days)

    avg_days_by_stage = {
        stage.value: round(sum(values) / len(values), 2)
        for stage, values in durations.items()
        if values
    }
    bottleneck_stage = None
    if avg_days_by_stage:
        bottleneck_stage = max(avg_days_by_stage, key=avg_days_by_stage.get)

    return {
        "avg_days_by_stage": avg_days_by_stage,
        "bottleneck_stage": bottleneck_stage,
        "transitions_count": len(ordered),
    }
