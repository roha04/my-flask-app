from fastapi import APIRouter

from app.web.routes import applications, auth, companies, dashboard, jobs, resumes

web_router = APIRouter()
web_router.include_router(auth.router)
web_router.include_router(dashboard.router)
web_router.include_router(companies.router)
web_router.include_router(jobs.router)
web_router.include_router(applications.router)
web_router.include_router(resumes.router)
