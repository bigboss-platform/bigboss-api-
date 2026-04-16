from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_model import TimestampedBase


class EndUser(TimestampedBase):
    __tablename__ = "end_users"

    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), default="")
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    consent_accepted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
