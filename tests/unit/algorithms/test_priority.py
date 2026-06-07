from app.algorithms.priority import score_application_priority
from app.models.enums import ApplicationStage


def test_higher_match_increases_priority():
    low = score_application_priority(0.2, 2, ApplicationStage.APPLIED)
    high = score_application_priority(0.9, 2, ApplicationStage.APPLIED)
    assert high > low


def test_later_stage_increases_priority():
    applied = score_application_priority(0.5, 2, ApplicationStage.APPLIED)
    onsite = score_application_priority(0.5, 2, ApplicationStage.ONSITE)
    assert onsite > applied


def test_recent_application_scores_higher():
    recent = score_application_priority(0.5, 1, ApplicationStage.APPLIED)
    old = score_application_priority(0.5, 25, ApplicationStage.APPLIED)
    assert recent > old


def test_score_is_bounded_between_zero_and_one():
    score = score_application_priority(1.5, -3, ApplicationStage.OFFER)
    assert 0.0 <= score <= 1.0
