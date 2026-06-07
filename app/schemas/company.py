from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class CompanyBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    website: str | None = Field(default=None, max_length=512)
    industry: str | None = Field(default=None, max_length=255)
    size: str | None = Field(default=None, max_length=64)


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    website: str | None = Field(default=None, max_length=512)
    industry: str | None = Field(default=None, max_length=255)
    size: str | None = Field(default=None, max_length=64)


class CompanyRead(CompanyBase, ORMModel):
    id: int
    created_at: datetime
    updated_at: datetime
