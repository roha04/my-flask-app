import math

from app.models.enums import ApplicationStage

DEFAULT_STAGE_RATES: dict[ApplicationStage, float] = {
    ApplicationStage.WISHLIST: 0.05,
    ApplicationStage.APPLIED: 0.15,
    ApplicationStage.PHONE_SCREEN: 0.35,
    ApplicationStage.TECHNICAL: 0.45,
    ApplicationStage.ONSITE: 0.60,
    ApplicationStage.OFFER: 0.85,
    ApplicationStage.REJECTED: 0.0,
    ApplicationStage.WITHDRAWN: 0.0,
}


def predict_response_likelihood(
    stage: ApplicationStage,
    historical_stats: dict[ApplicationStage, float] | None = None,
) -> float:
    """Estimate response likelihood using stage base rates and a logistic transform."""
    stats = historical_stats or DEFAULT_STAGE_RATES
    base_rate = stats.get(stage, 0.1)
    if base_rate <= 0:
        return 0.0
    if base_rate >= 1:
        return 1.0
    x = base_rate * 10.0 - 5.0
    likelihood = 1.0 / (1.0 + math.exp(-x))
    return max(0.0, min(1.0, likelihood))
