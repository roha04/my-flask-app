from app.models.enums import ApplicationStage

STAGE_ACTIONS: dict[ApplicationStage, list[tuple[int, str]]] = {
    ApplicationStage.WISHLIST: [
        (7, "Finalize resume and submit the application"),
        (14, "Review job requirements and decide whether to apply"),
    ],
    ApplicationStage.APPLIED: [
        (3, "Check application portal for confirmation"),
        (7, "Follow up with recruiter"),
        (14, "Send a polite follow-up email"),
    ],
    ApplicationStage.PHONE_SCREEN: [
        (2, "Prepare elevator pitch and company research"),
        (5, "Send thank-you note after the screen"),
    ],
    ApplicationStage.TECHNICAL: [
        (2, "Practice coding problems related to the stack"),
        (5, "Review feedback and send follow-up"),
    ],
    ApplicationStage.ONSITE: [
        (1, "Prepare interview stories and questions for the team"),
        (3, "Send thank-you notes to interviewers"),
    ],
    ApplicationStage.OFFER: [
        (1, "Review compensation and negotiate if needed"),
        (3, "Confirm acceptance deadline with the company"),
    ],
    ApplicationStage.REJECTED: [
        (0, "Request feedback and archive the application"),
    ],
    ApplicationStage.WITHDRAWN: [
        (0, "Document learnings and close the application"),
    ],
}


def suggest_next_action(stage: ApplicationStage, days_in_stage: int, match_score: float) -> str:
    """Rule engine recommending the next action for an application stage."""
    rules = STAGE_ACTIONS.get(stage, [])
    if not rules:
        return "Review application status"

    selected = rules[0][1]
    for threshold, action in rules:
        if days_in_stage >= threshold:
            selected = action

    if match_score >= 0.75 and stage == ApplicationStage.APPLIED and days_in_stage >= 5:
        return "Highlight strong skill match in follow-up outreach"
    if match_score < 0.35 and stage == ApplicationStage.WISHLIST:
        return "Improve resume keywords to better match the job description"
    return selected
