from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str


class MatchResponse(BaseModel):
    match_score: float = Field(ge=0, le=1)


class KeywordsRequest(BaseModel):
    jd_text: str
    top_n: int = Field(default=10, ge=1, le=50)


class KeywordsResponse(BaseModel):
    keywords: list[str]


class SuggestActionResponse(BaseModel):
    action: str
    days_in_stage: int
    match_score: float | None = Field(default=None, ge=0, le=1)


class PipelineAnalyticsResponse(BaseModel):
    avg_days_by_stage: dict[str, float]
    bottleneck_stage: str | None
    transitions_count: int


class StaleApplicationsResponse(BaseModel):
    stale_application_ids: list[int]
    count: int


class SalaryBenchmarkResponse(BaseModel):
    percentile: float | None
    median: float | None
    p25: float | None
    p75: float | None
    count: int
    salary: float
