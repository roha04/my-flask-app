from app.algorithms.likelihood import predict_response_likelihood
from app.models.enums import ApplicationStage


def test_offer_stage_has_highest_default_likelihood():
    offer = predict_response_likelihood(ApplicationStage.OFFER)
    applied = predict_response_likelihood(ApplicationStage.APPLIED)
    assert offer > applied


def test_rejected_stage_has_zero_default_likelihood():
    assert predict_response_likelihood(ApplicationStage.REJECTED) == 0.0


def test_custom_historical_stats_are_used():
    stats = {
        ApplicationStage.APPLIED: 0.9,
        ApplicationStage.REJECTED: 0.0,
        ApplicationStage.WISHLIST: 0.0,
        ApplicationStage.PHONE_SCREEN: 0.0,
        ApplicationStage.TECHNICAL: 0.0,
        ApplicationStage.ONSITE: 0.0,
        ApplicationStage.OFFER: 0.0,
        ApplicationStage.WITHDRAWN: 0.0,
    }
    assert predict_response_likelihood(ApplicationStage.APPLIED, stats) > 0.9


def test_result_is_within_zero_one_range():
    for stage in ApplicationStage:
        likelihood = predict_response_likelihood(stage)
        assert 0.0 <= likelihood <= 1.0
