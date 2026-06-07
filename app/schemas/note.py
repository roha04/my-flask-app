from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.models.enums import NoteEntityType
from app.schemas.common import ORMModel


class NoteBase(BaseModel):
    entity_type: NoteEntityType
    company_id: int | None = None
    job_id: int | None = None
    application_id: int | None = None
    body: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_entity_reference(self):
        refs = {
            NoteEntityType.COMPANY: self.company_id,
            NoteEntityType.JOB: self.job_id,
            NoteEntityType.APPLICATION: self.application_id,
        }
        if refs[self.entity_type] is None:
            entity = self.entity_type.value
            msg = f"{entity}_id is required for entity_type={entity}"
            raise ValueError(msg)
        return self


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    body: str | None = Field(default=None, min_length=1)


class NoteRead(NoteBase, ORMModel):
    id: int
    created_at: datetime
    updated_at: datetime
