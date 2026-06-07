from app.models.enums import ApplicationStage, JobStatus, NoteEntityType
from tests.helpers import auth_client


def test_company_crud(client):
    auth_client(client)

    response = client.post(
        "/api/v1/companies",
        json={"name": "Acme", "industry": "Tech", "website": "https://acme.example"},
    )
    assert response.status_code == 201
    company_id = response.json()["id"]

    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.patch(f"/api/v1/companies/{company_id}", json={"size": "50-200"})
    assert response.status_code == 200
    assert response.json()["size"] == "50-200"

    response = client.delete(f"/api/v1/companies/{company_id}")
    assert response.status_code == 204


def test_job_and_application_flow(client):
    auth_client(client)

    company = client.post("/api/v1/companies", json={"name": "Beta Corp"}).json()
    job = client.post(
        "/api/v1/jobs",
        json={
            "company_id": company["id"],
            "title": "Python Developer",
            "description": "FastAPI experience",
            "salary_min": 90000,
            "salary_max": 130000,
            "status": JobStatus.OPEN.value,
        },
    ).json()
    resume = client.post(
        "/api/v1/resumes",
        json={"title": "Main CV", "content": "Python FastAPI SQLAlchemy", "is_active": True},
    ).json()
    application = client.post(
        "/api/v1/applications",
        json={
            "job_id": job["id"],
            "resume_version_id": resume["id"],
            "stage": ApplicationStage.WISHLIST.value,
        },
    ).json()

    response = client.patch(
        f"/api/v1/applications/{application['id']}/stage",
        json={"stage": ApplicationStage.APPLIED.value},
    )
    assert response.status_code == 200
    assert response.json()["stage"] == ApplicationStage.APPLIED.value
    assert response.json()["applied_at"] is not None

    history = client.get(f"/api/v1/applications/{application['id']}/history").json()
    assert len(history) == 2
    assert history[-1]["to_stage"] == ApplicationStage.APPLIED.value


def test_contact_and_note(client):
    auth_client(client)

    company = client.post("/api/v1/companies", json={"name": "Gamma Inc"}).json()
    contact = client.post(
        "/api/v1/contacts",
        json={"company_id": company["id"], "name": "Jane Recruiter", "role": "HR"},
    ).json()
    assert contact["company_id"] == company["id"]

    note = client.post(
        "/api/v1/notes",
        json={
            "entity_type": NoteEntityType.COMPANY.value,
            "company_id": company["id"],
            "body": "Strong engineering culture",
        },
    ).json()
    assert note["body"].startswith("Strong")

    response = client.get("/api/v1/notes", params={"company_id": company["id"]})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_resume_activate(client):
    auth_client(client)

    first = client.post(
        "/api/v1/resumes",
        json={"title": "CV v1", "content": "v1", "is_active": True},
    ).json()
    second = client.post(
        "/api/v1/resumes",
        json={"title": "CV v2", "content": "v2", "is_active": False},
    ).json()

    response = client.post(f"/api/v1/resumes/{second['id']}/activate")
    assert response.status_code == 200
    assert response.json()["is_active"] is True

    resumes = client.get("/api/v1/resumes").json()
    active = [item for item in resumes if item["is_active"]]
    assert len(active) == 1
    assert active[0]["id"] == second["id"]
    assert first["id"] != active[0]["id"]
