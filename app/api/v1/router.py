from fastapi import APIRouter

from app.api.v1 import (
    applications,
    auth,
    companies,
    contacts,
    jobs,
    notes,
    resumes,
)

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(companies.router)
api_router.include_router(contacts.router)
api_router.include_router(jobs.router)
api_router.include_router(resumes.router)
api_router.include_router(applications.router)
api_router.include_router(notes.router)
