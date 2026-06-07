from app.models.enums import ApplicationStage

STAGE_WEIGHTS: dict[ApplicationStage, float] = {
    ApplicationStage.WISHLIST: 1.0,
    ApplicationStage.APPLIED: 3.0,
    ApplicationStage.PHONE_SCREEN: 5.0,
    ApplicationStage.TECHNICAL: 7.0,
    ApplicationStage.ONSITE: 8.0,
    ApplicationStage.OFFER: 10.0,
    ApplicationStage.REJECTED: 0.0,
    ApplicationStage.WITHDRAWN: 0.0,
}


def score_application_priority(
    match_pct: float,
    days_since_apply: int,
    stage: ApplicationStage,
) -> float:
    """Weighted priority score combining match, stage urgency, and recency."""
    normalized_match = max(0.0, min(1.0, match_pct))
    stage_component = STAGE_WEIGHTS.get(stage, 1.0) / 10.0
    recency_component = max(0.0, 1.0 - max(days_since_apply, 0) / 30.0)
    score = 0.5 * normalized_match + 0.3 * stage_component + 0.2 * recency_component
    return max(0.0, min(1.0, score))
