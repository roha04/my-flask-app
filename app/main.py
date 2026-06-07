from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from app.api.errors import register_exception_handlers
from app.api.v1.router import api_router
from app.config import get_settings
from app.database import get_db
from app.version import __version__

settings = get_settings()

app = FastAPI(
    title="Job Hunt CRM",
    description="Application tracker with resume-to-JD match scoring",
    version=__version__,
    debug=settings.debug,
)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, session_cookie="session")
register_exception_handlers(app)
app.include_router(api_router)


@app.get("/health")
def health(db: Session = Depends(get_db)) -> dict:
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"
    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "version": __version__,
        "db": db_status,
        "env": settings.env,
    }


@app.get("/version")
def version() -> dict:
    return {"version": __version__}
