from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.algorithms.keywords import extract_keywords
from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.analytics import (
    KeywordsRequest,
    KeywordsResponse,
    MatchRequest,
    MatchResponse,
    PipelineAnalyticsResponse,
    SalaryBenchmarkResponse,
    StaleApplicationsResponse,
)
from app.services import analytics as analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/pipeline", response_model=PipelineAnalyticsResponse)
def pipeline_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    return analytics_service.get_pipeline_analytics(db, current_user.id)


@router.get("/stale", response_model=StaleApplicationsResponse)
def stale_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    return analytics_service.get_stale_applications(db, current_user.id)


@router.get("/salary-benchmark", response_model=SalaryBenchmarkResponse)
def salary_benchmark_analytics(
    salary: float = Query(..., ge=0),
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
) -> dict:
    return analytics_service.get_salary_benchmark_analytics(db, salary)


@router.post("/match", response_model=MatchResponse)
def match_resume_to_job(
    payload: MatchRequest,
    _user: User = Depends(get_current_user),
) -> dict:
    return {"match_score": analytics_service.compute_match(payload.resume_text, payload.jd_text)}


@router.post("/extract-keywords", response_model=KeywordsResponse)
def extract_job_keywords(
    payload: KeywordsRequest,
    _user: User = Depends(get_current_user),
) -> dict:
    return {"keywords": extract_keywords(payload.jd_text, top_n=payload.top_n)}
