from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import ORMModel


class ContactBase(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr | None = None
    role: str | None = Field(default=None, max_length=255)
    linkedin: str | None = Field(default=None, max_length=512)


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    company_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: EmailStr | None = None
    role: str | None = Field(default=None, max_length=255)
    linkedin: str | None = Field(default=None, max_length=512)


class ContactRead(ContactBase, ORMModel):
    id: int
    created_at: datetime
