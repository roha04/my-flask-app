from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.enums import ApplicationStage
from app.services import analytics as analytics_service
from app.services import application as application_service
from app.web.deps import login_required, templates

router = APIRouter(tags=["web-dashboard"])


def _ctx(request: Request, user, **kwargs):
    return {
        "request": request,
        "user": user,
        "message": request.query_params.get("message"),
        "error": request.query_params.get("error"),
        **kwargs,
    }


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    auth = login_required(request, db)
    if isinstance(auth, RedirectResponse):
        return auth
    user = auth

    applications = application_service.list_applications(db, user.id, limit=500)
    active_count = sum(
        1
        for app in applications
        if app.stage not in (ApplicationStage.REJECTED, ApplicationStage.WITHDRAWN)
    )
    match_scores = [app.match_score for app in applications if app.match_score is not None]
    avg_match_pct = (
        round(sum(match_scores) / len(match_scores) * 100, 1) if match_scores else 0.0
    )
    stale = analytics_service.get_stale_applications(db, user.id)
    pipeline = analytics_service.get_pipeline_analytics(db, user.id)

    return templates.TemplateResponse(
        "dashboard/index.html",
        _ctx(
            request,
            user,
            stats={
                "active_count": active_count,
                "stale_count": stale["count"],
                "avg_match_pct": avg_match_pct,
                "bottleneck": pipeline["bottleneck_stage"],
            },
            pipeline=pipeline,
        ),
    )
