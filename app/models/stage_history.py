from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import ApplicationStage


class ApplicationStageHistory(Base):
    __tablename__ = "application_stage_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id", ondelete="CASCADE"), index=True
    )
    from_stage: Mapped[ApplicationStage | None] = mapped_column(
        Enum(ApplicationStage), nullable=True
    )
    to_stage: Mapped[ApplicationStage] = mapped_column(Enum(ApplicationStage))
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    application: Mapped[Application] = relationship(back_populates="stage_history")
