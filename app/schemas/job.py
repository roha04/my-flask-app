from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

from app.models.enums import JobStatus
from app.schemas.common import ORMModel


class JobBase(BaseModel):
    company_id: int
    title: str = Field(min_length=1, max_length=255)
    description: str = ""
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    currency: str = Field(default="USD", max_length=8)
    location: str | None = Field(default=None, max_length=255)
    url: HttpUrl | str | None = None
    status: JobStatus = JobStatus.OPEN


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    company_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    salary_min: int | None = Field(default=None, ge=0)
    salary_max: int | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, max_length=8)
    location: str | None = Field(default=None, max_length=255)
    url: HttpUrl | str | None = None
    status: JobStatus | None = None


class JobRead(JobBase, ORMModel):
    id: int
    created_at: datetime
    updated_at: datetime
