from app.algorithms.actions import suggest_next_action
from app.models.enums import ApplicationStage


def test_applied_follow_up_after_seven_days():
    action = suggest_next_action(ApplicationStage.APPLIED, days_in_stage=7, match_score=0.5)
    assert "follow up" in action.lower()


def test_wishlist_low_match_suggests_resume_improvement():
    action = suggest_next_action(ApplicationStage.WISHLIST, days_in_stage=1, match_score=0.2)
    assert "resume keywords" in action.lower()


def test_applied_high_match_suggests_skill_highlight():
    action = suggest_next_action(ApplicationStage.APPLIED, days_in_stage=6, match_score=0.9)
    assert "skill match" in action.lower()


def test_rejected_stage_has_closure_action():
    action = suggest_next_action(ApplicationStage.REJECTED, days_in_stage=0, match_score=0.4)
    assert "feedback" in action.lower()
