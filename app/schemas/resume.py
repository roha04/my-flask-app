from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class ResumeBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = ""


class ResumeCreate(ResumeBase):
    is_active: bool = False


class ResumeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None
    is_active: bool | None = None


class ResumeRead(ResumeBase, ORMModel):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
