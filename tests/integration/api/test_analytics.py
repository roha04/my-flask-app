from app.models.enums import ApplicationStage, JobStatus
from tests.helpers import auth_client


def _seed_job_application(client):
    company = client.post("/api/v1/companies", json={"name": "Analytics Co"}).json()
    job = client.post(
        "/api/v1/jobs",
        json={
            "company_id": company["id"],
            "title": "Backend Engineer",
            "description": "Python FastAPI PostgreSQL Docker backend engineer",
            "salary_min": 90000,
            "salary_max": 120000,
            "status": JobStatus.OPEN.value,
        },
    ).json()
    resume = client.post(
        "/api/v1/resumes",
        json={
            "title": "Backend CV",
            "content": "Python FastAPI PostgreSQL Docker backend development",
            "is_active": True,
        },
    ).json()
    application = client.post(
        "/api/v1/applications",
        json={
            "job_id": job["id"],
            "resume_version_id": resume["id"],
            "stage": ApplicationStage.WISHLIST.value,
        },
    ).json()
    return job, application


def test_application_scores_are_computed_on_create(client):
    auth_client(client)
    _, application = _seed_job_application(client)

    assert application["match_score"] is not None
    assert application["match_score"] > 0.5
    assert application["priority_score"] is not None
    assert application["response_likelihood"] is not None


def test_match_endpoint(client):
    auth_client(client)
    response = client.post(
        "/api/v1/analytics/match",
        json={
            "resume_text": "Python FastAPI developer",
            "jd_text": "Python FastAPI backend engineer",
        },
    )
    assert response.status_code == 200
    assert response.json()["match_score"] > 0.3


def test_extract_keywords_endpoint(client):
    auth_client(client)
    response = client.post(
        "/api/v1/analytics/extract-keywords",
        json={"jd_text": "Python FastAPI PostgreSQL engineer", "top_n": 3},
    )
    assert response.status_code == 200
    keywords = response.json()["keywords"]
    assert len(keywords) == 3
    assert "fastapi" in keywords


def test_suggest_action_endpoint(client):
    auth_client(client)
    _, application = _seed_job_application(client)

    response = client.get(f"/api/v1/applications/{application['id']}/suggest-action")
    assert response.status_code == 200
    data = response.json()
    assert data["action"]
    assert "days_in_stage" in data


def test_pipeline_and_stale_analytics(client):
    auth_client(client)
    _, application = _seed_job_application(client)

    client.patch(
        f"/api/v1/applications/{application['id']}/stage",
        json={"stage": ApplicationStage.APPLIED.value},
    )

    pipeline = client.get("/api/v1/analytics/pipeline")
    assert pipeline.status_code == 200
    assert pipeline.json()["transitions_count"] >= 2

    stale = client.get("/api/v1/analytics/stale")
    assert stale.status_code == 200
    assert "stale_application_ids" in stale.json()


def test_salary_benchmark_endpoint(client):
    auth_client(client)
    client.post(
        "/api/v1/jobs",
        json={
            "company_id": client.post("/api/v1/companies", json={"name": "Pay Co"}).json()["id"],
            "title": "Engineer",
            "description": "Python",
            "salary_min": 80000,
            "salary_max": 100000,
        },
    )

    response = client.get("/api/v1/analytics/salary-benchmark", params={"salary": 90000})
    assert response.status_code == 200
    data = response.json()
    assert data["salary"] == 90000
    assert data["count"] >= 1
